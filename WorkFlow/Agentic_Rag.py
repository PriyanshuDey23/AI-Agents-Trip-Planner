from crewai import Agent, Task, Crew, LLM, Process
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM model
llm = LLM(model='gemini/gemini-2.0-flash', api_key=GOOGLE_API_KEY)

def setup_rag_system(content, question):
    agent = Agent(
        role="Travel Q&A Expert",
        goal="Answer detailed questions about the travel itinerary using available knowledge.",
        backstory="A top-tier assistant helping travelers understand their itinerary, logistics, and destination details.",
        verbose=True,
        reasoning=True,
        allow_delegation=False,
        llm=llm,
    )

    task = Task(
        description="Based on the following travel itinerary:\n{itinerary}\n\nAnswer the question: {question}",
        expected_output="A clear, specific and helpful answer based only on the provided itinerary.",
        agent=agent,
        
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True,
        process=Process.sequential,
    )

    result = crew.kickoff(inputs={"question": question, "itinerary": content})
    return result

# if __name__ == "__main__":
#     itinerary_text = """
#     Day 1: Arrive in Paris and check into the hotel near the Eiffel Tower.
#     Day 2: Visit the Louvre Museum, enjoy a Seine River cruise.
#     Day 3: Day trip to Versailles.
#     Day 4: Fly to Rome, check into hotel near Colosseum.
#     Day 5: Vatican City tour and Italian cooking class.
#     """

#     test_question = "What will I do on the second day in Paris?"
#     answer = setup_rag_system(itinerary_text, test_question)
#     print("Answer:\n", answer)


