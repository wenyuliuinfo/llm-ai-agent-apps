# Import libraries
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.deepseek import DeepSeek
from agno.tools.yfinance import YFinanceTools
from agno.workflow import Step, Workflow
from agno.tools.file import FileTools

# Load env variable for API Key
load_dotenv()

def create_db():
    # Storage Configuration
    Path("temp").mkdir(exist_ok=True)
    workflow_db = SqliteDb(db_file="temp/stock_agents.db")
    return workflow_db

# Define function to gather the raw data
def data_gatherer(workflow_db, use_pro: bool=True):
    
    model_id = "deepseek-v4-pro" if use_pro else "deepseek-v4-flash"
    
    # Configure tools for real-time data processing
    tools = [
        YFinanceTools()
    ]

    # Step 1: Data Gatherer - Fetches raw market data
    data_agent = Agent(
        name="Data Gatherer",
        model=DeepSeek(id=model_id),
        tools=tools,
        instructions="""\
You are a data gathering agent. Your job is to fetch comprehensive market data.

For the requested stock, gather:
- Current price and daily change
- Market cap and volume
- P/E ratio, EPS, and other key ratios
- 52-week high and low price
- Recent price trends
- Company latest news

Present the raw data clearly. Don't analyze - just gather and organize. \
""",
        db=workflow_db,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
    )

    data_step = Step(
        name="Data Gathering",
        agent=data_agent,
        description="Fetch comprehensive market data for the stock"
    )

    return data_step

# Define function to analyze the data
def data_analyst(workflow_db, use_pro: bool=True):
    model_id = "deepseek-v4-pro" if use_pro else "deepseek-v4-flash"

    # Step 2: Analyst - Interprets the data
    analyst_agent = Agent(
        name="Analyst",
        model=DeepSeek(id=model_id),
        instructions="""\
You are a financial analyst. You receive raw market data from the data team.

Your job is to :
- Interpret the key metrics (is the P/E high or low for this sector?)
- Identify strengths and weaknesses
- Note any red flags or positive signals
- Compare to typical industry benchmarks

Provide analysis, not recommendations. Be objective and data-driven. \
""",
        db=workflow_db,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
    )
    
    analysis_step = Step(
        name="Analysis",
        agent=analyst_agent,
        description="Analyze the market data and identify key insights."
    )

    return analysis_step

# Define function to write report
def report_writer(workflow_db, use_pro: bool=True):
    model_id = "deepseek-v4-pro" if use_pro else "deepseek-v4-flash"

    # Step 3: Report writer - produces final output
    report_agent = Agent(
        name="Report Writer",
        model=DeepSeek(id=model_id),
        instructions="""\
You are a report writer. You receive analysis from the research team.

IMPORTANT: At the end of your response, use the save_file tool to \
save this report to a file named "{stock_symbol}_investment_report.md".

Your job is to:
- Synthesize the analysis into a clear investment brief
- Lead with a one-line summary
- Include a recommendation (Buy/Hold/Sell) with rationale
- Keep it concise - max 300 words
- End with key metrics in a small table

Write for a busy investor who wants the bottom line fast. \
""",
        db=workflow_db,
        add_datetime_to_context=True,
        add_history_to_context=True,
        num_history_runs=5,
        markdown=True
    )

    report_step = Step(
        name="Report Writing",
        agent=report_agent,
        description="Produce a concise investment brief"
    )

    return report_step

# Define function to create the workflow
def create_workflow():
    workflow_db = create_db()
    data_step = data_gatherer(workflow_db)
    analysis_step = data_analyst(workflow_db)
    report_step = report_writer(workflow_db)
    
    sequential_workflow = Workflow(
        name="Sequential Workflow",
        description="Three-step research pipeline: Data -> Analysis -> Report",
        steps=[
            data_step,
            analysis_step,
            report_step
        ]
    )
    return sequential_workflow

# Define function to save the report to a markdown file
def save_report_to_markdown(user_query: str, response_content: str):
    reports_dir = Path("./reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = reports_dir / f"investment_report_{timestamp}.md"

    # Write the report with proper formatting
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"# Investment Analysis Report\n\n")
        f.write(f"**Request: ** {user_query}\n\n")
        f.write(f"**Analysis Date: ** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(response_content)
        f.write("---\n\n")
        f.write(f"*Report generated by AI Investment Analysis Pipeline* \n")
    return filename


# Run the workflow
if __name__ == "__main__":
    print("\n" + "="*80)
    print("STOCK INVESTMENT ANALYSIS PIPELINE")
    print("="*80)
    print("\nThis pipeline will:")
    print("1. Gather real-time market data")
    print("2. Analyze the data for insights")
    print("3. Generate an investment report")
    print("\nType 'quit', 'exit', or 'q' to stop\n")

    print("\nInitializing workflow and database...")
    workflow = create_workflow()
    print("Workflow ready!\n")

    while True:
        user_query = input("\n" + "="*80 + "\nPlease enter your request: ")
        if user_query.lower() in ["quit", "exit", "q"]:
            print("\nThank you for using the Investment Analysis Pipeline. Goodbye!")
            break
        
        try: 
            print("Running analysis pipeline...\n")
            response = workflow.run(user_query)
            if response and response.content:
                saved_file = save_report_to_markdown(
                    user_query, response.content
                )
                print(f"\nInvestment report saved to: {saved_file}")
        except Exception as e:
            print(f"\nError during analysis: {str(e)}")
            print(f"Please check your API key and try again.")