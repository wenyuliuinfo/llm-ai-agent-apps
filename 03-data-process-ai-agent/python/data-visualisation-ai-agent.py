# Import libraries
import os
import re
import sys
import io
import contextlib
import warnings
import base64
import streamlit as st
import pandas as pd
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO
from openai import OpenAI
from e2b_code_interpreter import Sandbox
from typing import Optional, List, Any, Tuple

# Load env variable for API Key
load_dotenv()

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
pattern = re.compile(r"```python\n(.*?)\n```", re.DOTALL)

# Define function for code interpreter
def code_interpret(e2b_code_interpreter: Sandbox, code: str) -> Optional[List[Any]]:
    with st.spinner("Executing code in E2B Sandbox..."):
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture), contextlib.redirect_stderr(stderr_capture):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                exec = e2b_code_interpreter.run_code(code)

        if stderr_capture.getvalue():
            print("[Code Interpreter Warnings/Errors]", file=sys.stderr)
            print(stderr_capture.getvalue(), file=sys.stderr)

        if stdout_capture.getvalue():
            print("[Code Interpreter Output]", file=sys.stdout)
            print(stdout_capture.getvalue(), file=sys.stdout)

        if exec.error:
            print(f"[Code Interpreter Error] {exec.error}", file=sys.stderr)
            return None
        return exec.results

# Define function to match LLM response
def match_code_blocks(llm_response: str) -> str:
    match = pattern.search(llm_response)
    if match:
        code = match.group(1)
        return code
    return ""

# Define function to start conversation with LLM
def chat_with_llm(e2b_code_interpreter: Sandbox, user_message: str, dataset_path: str) -> Tuple[Optional[List[Any]], str]:
    # Update system prompt to include dataset path information
    system_prompt = f"""
    You are a Python data scientist and data visualization expert. 
    You are given a dataset at path '{dataset_path}' and also the user's query.
    You need to analyze the dataset and answer the user's query with a response and you run Python code to solve them.
    
    IMPORTANT: Always use the dataset path variable '{dataset_path}' in your code when reading CSV file.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    model_id = "deepseek-v4-pro"
    with st.spinner("Getting response from DeepSeek LLM Model..."):
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
        )

        response_message = response.choices[0].message
        python_code = match_code_blocks(response_message.content)

        if python_code:
            code_interpret_results = code_interpret(e2b_code_interpreter, python_code)
            return code_interpret_results, response_message.content
        else:
            st.warning(f"Failed to match any Python code in LLM response.")
            return None, response_message.content

# Define function to upload dataset
def upload_dataset(code_interpreter: Sandbox, uploaded_file) -> str:
    dataset_path = f"./{uploaded_file.name}"
    try:
        code_interpreter.files.write(dataset_path, uploaded_file)
        return dataset_path
    except Exception as error:
        st.error(f"Error during file upload: {error}")
        raise error

# Define main function
def main():
    st.title("AI Data Visualization Agent")
    st.write("Upload your dataset and ask questions about it!")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        # Display dataset with toggle
        df = pd.read_csv(uploaded_file)
        st.write("Dataset: ")
        show_full = st.checkbox("Show full dataset")
        if show_full:
            st.dataframe(df)
        else:
            st.write("Preview (top 5 rows): ")
            st.dataframe(df.head())
             
        query = st.text_input("What would you like to know about your data?")
        col1 = st.columns(1)

        with col1[0]:
            if st.button("Analyze"):
                with Sandbox() as code_interpreter:
                    # Upload the dataset
                    dataset_path = upload_dataset(code_interpreter, uploaded_file)
                
                    # Pass dataset_path to chat_with_llm
                    code_results, llm_response = chat_with_llm(code_interpreter, query, dataset_path)
            
                    # Display LLM Response
                    st.write("AI Response: ")
                    st.write(llm_response)

                    # Display visualisation
                    if code_results:
                        for result in code_results:
                            if hasattr(result, 'png') and result.png:
                                # Convert PNG data to image and display it
                                png_data = base64.b64decode(result.png)
                                image = Image.open(BytesIO(png_data))
                                st.image(image, caption="Generated Visualization", use_container_width=False)
                            elif hasattr(result, 'figure'):
                                fig = result.figure
                                st.pyplot(fig)
                            elif hasattr(result, 'show'):
                                st.plotly_chart(result)
                            elif isinstance(result, (pd.DataFrame, pd.Series)):
                                st.dataframe(result)
                            else:
                                st.write(result)

if __name__ == "__main__":
    main()
