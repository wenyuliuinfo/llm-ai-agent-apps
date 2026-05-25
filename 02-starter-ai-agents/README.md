# AI Travel Agent

This Streamlit app is an AI-Powered travel agent that generates personalized travel itineraries using DeepSeek v4 Pro. It automates the process of researching, planning, and organizing your dream vacation, allowing you to explore exciting destinations with ease.


## Features
- Research and discover exciting travel destinations, activities, and accommodations
- Customize your itinerary based on the number of days you want to travel
- Utilize the power of DeepSeek v4 to generate intelligent and personalized travel plans
- Download your itinerary as a calendar (.ics) file to import into Apple Calendar, or other calendar apps
  

## How it Works
The AI Travel Agent has two main components:
1. **Researcher**: Responsible for generating search terms based on the user's destination and travel duration, and searching the web for relevant activities and accommodations using SerpAPI.
2. **Planner**: Takes the research results and user preferences to generate a personalized draft itinerary that includes suggested activities, dining options, and accommodations.

### Using the Calendar Download Feature
After generating your Travel itinerary:
1. Click the "Download Itinerary as Calendar (.ics)" button that appears next to the "Generate Itinerary" button
2. Save the .ics file to your computer
3. Import the file into your preferred calender application (Apple Calendar, Outlook, etc.)
4. Each day of your itinerary will appear as an all-day event in your calendar
5. The complete details for each day's activities are included in the event description

This feature makes it easy to keep track of your travel plans and have your itinerary available on your devices, even offline.


## How to Get Started
1. Clone the repository:
```bash
git clone https://github.com/wenyuliuinfo/llm-ai-agent-apps.git
cd 02-starter-ai-agents/python
```

2. Install the prerequisites:
```bash
pip install -U -r requirements.txt
```

3. Run the application:
```bash
streamlit run travel-ai-agent.py
```