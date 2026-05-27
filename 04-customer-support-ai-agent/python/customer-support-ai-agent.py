# Import libraries
import os
import json
import streamlit as st
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI
from datetime import datetime, timedelta

# Load env variable for API Key
load_dotenv()

class CustomerSupportAIAgent:
    def __init__(self):
        config = {
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "host": "localhost",
                    "port": 6333,
                }
            }
        }
        try:
            self.memory = Memory.from_config(config)
        except Exception as e:
            st.error(f"Failed to initialize memory: {e}")
            st.stop()

        # Setup LLM model details
        self.client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url=os.getenv("DEEPSEEK_BASE_URL")
        )
        self.app_id = "customer-support"

    # Define function to handle user query
    def handle_query(self, query, user_id=None):
        try:
            # Search for relevant memory
            relevant_memories = self.memory.search(query=query, filters={'user_id': user_id})
            
            # Build context from relevant memory
            context = "Relevant past information: \n"
            if relevant_memories and ("results" in relevant_memories):
                for memory in relevant_memories["results"]:
                    if "memory" in memory:
                        context += f"- {memory['memory']}\n"

            # Generate response using DeepSeek
            full_prompt = f"{context}\nCustomer: {query}\nSupport Agent:"
            model_id = "deepseek-v4-pro"
            messages = [
                {"role": "system", "content": "You are a customer support AI Agent"},
                {"role": "user", "content": full_prompt}
            ]
            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
            )
            answer = response.choices[0].message.content
            self.memory.add(query, user_id=user_id, metadata={"app_id": self.app_id, "role": "user"})
            self.memory.add(answer, user_id=user_id, metadata={"app_id": self.app_id, "role": "assistant"})
            
            return answer
        except Exception as e:
            st.error(f"Failed to handle user query: {e}")
            return "Sorry, encountered an error. Please try again later."

    # Define function to get past memory
    def get_memories(self, user_id=None):
        try:
            return self.memory.get_all(user_id=user_id)
        except Exception as e:
            st.error(f"Failed to retrieve memories: {e}")
            return None

    # Define function to generate customer data
    def generate_synthetic_data(self, user_id: str) -> dict | None:
        try:
            today = datetime.now()
            order_date = (today - timedelta(days=10)).strftime("%B %d, %Y")
            expected_delivery = (today + timedelta(days=2)).strftime("%B %d, %Y")
    
            prompt = f"""
            Generate a detailed customer profile and order history for TechGadgets.com, 
            an electronics store, with customer ID {user_id}.
            Include: 
            1. Customer name and basic info
            2. A recent order of high-end electronic device (placed on {order_date}, to be delivered by {expected_delivery})
            3. Order details (product, price, order number)
            4. Customer's shipping address
            5. 2-3 previous orders from the past year
            6. 2-3 customer service interactions related to these orders

            Format the output as a JSON object
            """

            model_id = "deepseek-v4-pro"
            messages = [
                {"role": "system", "content": "You are a data generation AI that creates realistic customer profiles and order histories. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ]
            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
            )
            customer_data = json.loads(response.choices[0].message.content)

            # Add generated data to memory
            for key, value in customer_data.items():
                if isinstance(value, list):
                    for item in value:
                        self.memory.add(
                            json.dumps(item),
                            user_id=user_id,
                            metadata={"app_id": self.app_id, "role": "system"}
                        )   
                else:
                    self.memory.add(
                        f"{key}: {json.dumps(value)}",
                        user_id=user_id,
                        metadata={"app_id": self.app_id, "role": "system"}
                    )

            return customer_data
        except Exception as e:
            st.error(f"Failed to generate synthetic data: {e}")
            return None
        

# Define main function
def main():
    st.title("AI Customer Support AI Agent with Memory 🛒")
    st.caption("Chat with a customer support assistant who remembers your past interactions.")

    # Initialize the CustomerSupportAIAgent
    support_agent = CustomerSupportAIAgent()

    # Sidebar for customer ID and memory view
    st.sidebar.title("Enter your Customer ID: ")
    previous_customer_id = st.session_state.get("previous_customer_id", None)
    customer_id = st.sidebar.text_input("Enter your Customer ID")

    if customer_id != previous_customer_id:
        st.session_state.messages = []
        st.session_state.previous_customer_id = customer_id
        st.session_state.customer_data = None

    # Add button to generate synthetic data
    if st.sidebar.button("Generate Synthetic Data"):
        if customer_id:
            with st.spinner("Generating customer data..."):
                st.session_state.customer_data = support_agent.generate_synthetic_data(customer_id)
            if st.session_state.customer_data:
                st.sidebar.success("Synthetic data generated successfully!")
            else:
                st.sidebar.error("Failed to generate synthetic data.")
        else:
            st.sidebar.error("Please enter an customer ID first.")

    # View customer profile
    if st.sidebar.button("View Customer Profile"):
        if st.session_state.customer_data:
            st.sidebar.json(st.session_state.customer_data)
        else:
            st.sidebar.info("No customer data generated yet. Please click 'Generate Synthetic Data' first.")

    # Initialize the Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the Chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    query = st.chat_input("How can I assist you today?")
    if query and customer_id:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        # Generate and display response
        with st.spinner("Generating response..."):
            answer = support_agent.handle_query(query, user_id=customer_id)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)
    elif not customer_id:
        st.error("Please enter a Customer ID to start the chat.")
    

if __name__ == "__main__":
    main()