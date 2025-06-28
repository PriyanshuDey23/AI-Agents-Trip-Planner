from crewai import Agent, Task, Crew, LLM
from WorkFlow.Tools import duckduckgo_search,fetch_article
import os
from dotenv import load_dotenv



# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM model
Model = LLM(model='gemini/gemini-2.0-flash', api_key=GOOGLE_API_KEY)


# Tool for web search and article search
search_tool = duckduckgo_search
fetch_tool=fetch_article



# ----------- TripAgents Class -----------
class TripAgents:
    def __init__(self):
        self.llm = Model

    # City Selection Agent
    def city_selector_agent(self):
        return Agent(
            role="City Selection Expert",
            goal="Identify the best cities to visit based on user preferences",
            backstory=(
                "A seasoned Travel Geographer known for sustainable and offbeat destinations, "
                "with in-depth knowledge of cultural, historical, and entertainment aspects."
            ),
            llm=self.llm,
            reasoning=True,
            tools=[search_tool,fetch_tool],
            verbose=True
        )

    # Local Expert Agent
    def local_expert_agent(self):
        return Agent(
            role="Local Destination Expert",
            goal="Provide detailed insights about selected cities, including top attractions, local customs, and hidden gems",
            backstory=(
                "A multilingual local guide renowned for curating immersive experiences "
                "and uncovering secret spots known only to locals."
            ),
            llm=self.llm,
            reasoning=True,
            tools=[search_tool,fetch_tool],
            verbose=True
        )

    # Travel Planner Agent
    def travel_planner_agent(self):
        return Agent(
            role="Professional Travel Planner",
            goal="Design perfect, personalized itineraries with seamless logistics and local flavor.",
            backstory=(
                "A detail-oriented travel planner famous for crafting balanced, stress-free, "
                "and unforgettable itineraries for travelers of all styles."
            ),
            llm=self.llm,
            reasoning=True,
            tools=[search_tool,fetch_tool],
            verbose=True
        )

    # Budget Manager Agent
    def budget_manager_agent(self):
        return Agent(
            role="Travel Budget Manager",
            goal="Help users create realistic, cost-effective budgets while ensuring quality experiences.",
            backstory=(
                "A travel finance expert adept at finding the perfect balance between affordability "
                "and unforgettable experiences."
            ),
            llm=self.llm,
            reasoning=True,
            tools=[search_tool,fetch_tool],
            verbose=True
        )


# ----------- TripTasks Class -----------
class TripTasks:
    def __init__(self):
        pass

    # City Selection Task
    def city_selection_task(self, agent, inputs):
        return Task(
            name="City Selection",
            description=(
                "Analyze the user's preferences to recommend the most suitable travel destinations by following these steps:\n"
                "1. Identify cities that are ideal to visit in the given season.\n"
                "2. Cross-reference those cities with the specified travel type and user interests.\n"
                "3. Prioritize cities offering a good balance of cultural, recreational, and unique experiences.\n"
                f"- Travel Type: {inputs['travel_type']}\n"
                f"- Interests: {inputs['interests']}\n"
                f"- Season: {inputs['season']}\n\n"

            ),
            agent=agent,
            expected_output="Bulleted list of cities with a short rationale for each recommendation.",
        )

    # City Research Task
    def city_research_task(self, agent, city):
        return Task(
            name="City Research",
            description=(
                f"Conduct in-depth, structured research on {city} using the following format:\n"
                "1. List top attractions and must-visit landmarks.\n"
                "2. Highlight popular local dishes and cuisine specialties.\n"
                "3. Summarize important cultural norms, etiquette, and local customs.\n"
                "4. Recommend safe, well-located areas for accommodation.\n"
                "5. Provide transportation tips including local travel hacks.\n"
                "6. Include hidden gems or lesser-known experiences that locals enjoy.\n\n"
                "Output: Organize findings into clear, titled sections with bullet points for each topic."
            ),
            agent=agent,
            expected_output="Organized sections with clear headings and bullet points covering each topic.",
        )

    # Itinerary Creation Task
    def itinerary_creation_task(self, agent, city, inputs):
        return Task(
            name="Itinerary Creation",
            description=(
                f"Plan a detailed {inputs['duration']}-day itinerary for {city}, ensuring it is well-paced and enjoyable.\n"
                "1. Break each day into time slots.\n"
                "2. Sequence attractions and activities logically to minimize travel time.\n"
                "3. Include transportation options and estimated travel durations between locations.\n"
                "4. Suggest meal options (breakfast, lunch, dinner) with location recommendations.\n"
                "5. Ensure a good mix of sightseeing, leisure, dining, and hidden experiences.\n\n"
                "Output: A structured, day-by-day table including time slots, activity descriptions, transport notes, and meal suggestions."
            ),
            agent=agent,
            expected_output="A clear, day-by-day table format itinerary with time slots, activities, transport details, and meal suggestions.",
        )

    # Budget Planning Task
    def budget_planning_task(self, agent, inputs, itinerary):
        return Task(
            name="Budget Planning",
            description=(
                f"Based on the provided itinerary and selected budget category ({inputs['budget']}), create a comprehensive budget plan covering:\n"
                "1. Accommodation costs per night and total for the trip.\n"
                "2. Transportation expenses (local and intercity as needed).\n"
                "3. Attraction and activity fees based on itinerary items.\n"
                "4. Meal budget estimates for breakfast, lunch, and dinner per day.\n"
                "5. A recommended emergency fund allowance.\n"
                "6. Optional extras or tips if budget allows.\n\n"
                "Output: Present an itemized budget table with category-wise cost estimates and a total cost analysis."
            ),
            agent=agent,
            context=[itinerary],
            expected_output="An itemized budget table with detailed cost breakdown and total cost analysis.",
        )



# ------------- Trip Crew Manager -------------
class TripCrew:
    def __init__(self, inputs):
        self.inputs = inputs

    def run(self):
        # Initialize agent and task factories
        agent_factory = TripAgents()
        task_factory = TripTasks()

        # Create agents
        city_selector = agent_factory.city_selector_agent()
        local_expert = agent_factory.local_expert_agent()
        travel_planner = agent_factory.travel_planner_agent()
        budget_manager = agent_factory.budget_manager_agent()

        # Create tasks
        city_selection_task = task_factory.city_selection_task(city_selector, self.inputs)
        city_research_task = task_factory.city_research_task(local_expert, city_selection_task)
        create_itinerary_task = task_factory.itinerary_creation_task(travel_planner, city_selection_task, self.inputs)
        plan_budget_task = task_factory.budget_planning_task(budget_manager, self.inputs, create_itinerary_task)

        # Create Crew
        crew = Crew(
            agents=[city_selector, local_expert, travel_planner, budget_manager],
            tasks=[city_selection_task, city_research_task, create_itinerary_task, plan_budget_task],
            verbose=True
        )


        result = crew.kickoff()
        return result

# Function for  this use case
def display_trip_results(result):
    """
    Parse CrewAI trip planning results into a structured dictionary.

    Returns:
        dict: A dictionary where keys are task names (snake_case) and values are cleaned result text.
    """
    final_result = {}

    if hasattr(result, "tasks_output") and result.tasks_output:
        for task in result.tasks_output:
            task_name_key = task.name.lower().replace(" ", "_")
            cleaned_content = task.raw.strip("`") if task.raw else "No content available."
            final_result[task_name_key] = cleaned_content
    else:
        # Return empty result if no tasks or outputs
        final_result = {}

    return final_result



# Function to display trip results dynamically (Maximum use case)
# def display_trip_results(result):
#     """
#     Display CrewAI trip planning results dynamically in Streamlit.
#     """
#     if hasattr(result, "tasks_output") and result.tasks_output:
#         final_result = {}

#         # Build final_result dict dynamically based on task names
#         for task in result.tasks_output:
#             task_name_key = task.name.lower().replace(" ", "_")
#             final_result[task_name_key] = task.raw

#         # Display each result section in Streamlit
#         st.title("🗺️ Trip Planning Results")

#         for key, content in final_result.items():
#             section_title = key.replace("_", " ").title()
#             st.subheader(f"📌 {section_title}")

#             if content:
#                 # Clean up any extra triple backticks
#                 cleaned_content = content.strip("`")
#                 st.markdown(cleaned_content)
#             else:
#                 st.warning(f"❌ No result found for {section_title}.")

#         return final_result

#     else:
#         st.error("❌ No task outputs found in the Crew result.")
#         return {}
    










    






        


