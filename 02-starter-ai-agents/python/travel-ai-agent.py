# Import libraries
import os
import re
import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from agno.agent import Agent
from agno.run.agent import RunOutput
from agno.tools.serpapi import SerpApiTools
from agno.models.deepseek import DeepSeek
from agno.tools.file import FileTools

# Load env variable for API Key
load_dotenv()

# Define function to generate ICS calendar file
def generate_ics_content(plan_text: str, start_date: datetime = None) -> bytes:
    
    cal = Calendar()
    cal.add("prodid", "-//AI Travel Planner//")
    cal.add("version", "2.0")
    
    if start_date is None:
        start_date = datetime.today()

    # Split the plan into days
    day_pattern = re.compile(r"Day (\d+)[:\s]+(.*?)(?=Day \d+|$)", re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days:
        # If no days pattern found, create a single all day event
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add('dtstamp', datetime.now())
        cal.add_component(event)
    else:
        # Process each day event
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num-1)
            
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add('dtstamp', datetime.now())
            cal.add_component(event)
    
    return cal.to_ical()


# Define function to set up Streamlit App
def setup_streamlit_app():
    st.title("AI Travel Planner")
    st.caption("Plan your next adventure with AI Travel Planner by researching and planning a personalized itinerary")

    # Initialize session state to store the generated itinerary
    if "itinerary" not in st.session_state:
        st.session_state.itinerary = None

    
# Define function for Travel agent
def research_travel_agent(use_pro: bool=True):
    
    model_id = "deepseek-v4-pro" if use_pro else "deepseek-v4-flash"
    
    # Step 1: Research the destination 
    researcher = Agent(
        name="Researcher",
        role="Searches for travel destination, activities, and accommodations based on user preference",
        model=DeepSeek(id=model_id),
        description=dedent("""\
        You are a world-class travel researcher. Given a travel destination and the number of traveling days,
        generate a list of search terms for finding relevant travel activities and accommodations.
        Then search the web for each term, analyze the results, and return the 10 most relevant results.
        """),
        instructions=[
            "Given a travel destination and the number of days the user wants to travel for, first generate a list of 3 search terms related to that destination and the number of days.",
            "For each search term, `search_google` and analyze the results."
            "From the results of all searches, return the 10 most relevant results to the user's preferences.",
            "Remember: the quality of the results is important.",
        ],
        tools=[SerpApiTools()],
        add_datetime_to_context=True
    )
    return researcher

# Define function for Travel agent
def plan_travel_agent(use_pro: bool=True):
    
    model_id = "deepseek-v4-pro" if use_pro else "deepseek-v4-flash"
    
    # Step 2: Plan the travel calendar based on research results
    planner = Agent(
        name="Planner",
        role="Generates a draft itinerary based on user preferences and research results",
        model=DeepSeek(id=model_id),
        description=dedent("""\
        You are a senior travel planner. Given a travel destination, the number of days the user wants to travel for, and a list of research results,
        your goal is to generate a draft itinerary that meets the user's needs and preferences.
        """),
        instructions=[
            "Given a travel destination, the number of days the user wants to travel for, and a list of research results "
            "generate a draft itinerary that includes suggested activities and accommodations.",
            "Ensure the itinerary is well-structured, informative, and engaging.",
            "Ensure you provide a nuanced and balanced itinerary, quoting facts where possible.",
            "Remember: the quality of the itinerary is important.",
            "Focus on clarity, coherence and overall quality.",
            "Never make up facts or plagiarize. Always provide proper attribution."
        ],
        add_datetime_to_context=True
    )
    return planner

# Run the travel agent
if __name__ == "__main__":
    
    setup_streamlit_app()

    destination = st.text_input("Where do you want to go?")
    num_days = st.number_input("How many days do you want to travel for?", min_value=1, max_value=30, value=7)
    col1, col2 = st.columns(2)

    # Generate the itinerary based on user input
    with col1:
        if st.button("Generate Itinerary"):
            with st.spinner("Researching your destination..."):
                research_results: RunOutput = research_travel_agent().run(f"Research {destination} for a {num_days} day trip", stream=False)
                st.write("Research completed")
            
            with st.spinner("Creating your personalized itinerary..."):
                prompt = f"""
                    Destination: {destination}
                    Duration: {num_days} days
                    Research Results: {research_results.content}
    
                    Please create a detailed itinerary based on this research.
                """
                planner_results: RunOutput = plan_travel_agent().run(prompt, stream=False)
                st.session_state.itinerary = planner_results.content
                st.write(planner_results.content)

    # Only show download button if there's an itinerary
    with col2:
        if st.session_state.itinerary:
            ics_content = generate_ics_content(st.session_state.itinerary)
            st.download_button(
                label="Download Itinerary as Calendar (.ics)",
                data=ics_content,
                file_name="travel_itinerary.ics",
                mime="text/calendar"
            )