import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# Load your .env file
load_dotenv()

# Map OpenRouter key to what CrewAI expects
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")

os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# --- User Input ---
topic = input("Enter a topic for idea generation: ")

# --- Define Agents ---
idea_generator = Agent(
    role="Idea Generator",
    goal=f"Generate creative and innovative ideas related to {topic}",
    backstory="An imaginative AI expert at brainstorming unique concepts and solutions."
)

evaluator = Agent(
    role="Evaluator",
    goal=f"Assess and critique the generated ideas about {topic} for feasibility and potential",
    backstory="A critical thinker skilled in analyzing ideas, highlighting strengths, weaknesses, and practical implications."
)

# --- Define Tasks ---
task1 = Task(
    description=f"Brainstorm and list out 5-7 creative ideas or concepts related to {topic}. Provide brief descriptions for each.",
    expected_output="A numbered list of ideas with short explanations.",
    agent=idea_generator
)

task2 = Task(
    description=f"Evaluate the generated ideas about {topic}. For each idea, discuss pros, cons, feasibility, and overall potential.",
    expected_output="A structured evaluation for each idea, including pros, cons, and a feasibility score (e.g., 1-10).",
    agent=evaluator
)

# --- Create and Run the Crew ---
crew = Crew(
    agents=[idea_generator, evaluator],
    tasks=[task1, task2],
    verbose=True
)

result = crew.kickoff()

print("\n--- Final Output ---\n")
print(result)
