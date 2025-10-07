#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from crewai import Crew, Process
from ba_agents import BaAgents
from ba_tasks import BaTasks
from conditional_crew import CustomWorkflow
from dotenv import load_dotenv
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def main():
    # Initialize agents and tasks
    ba_agents = BaAgents()
    ba_tasks = BaTasks()
    
    # Create custom workflow
    workflow = CustomWorkflow(ba_agents, ba_tasks)
    
    # Your raw requirement text
    raw_requirement = """
    We need a mobile app for food delivery that allows users to:
    - Browse restaurants by cuisine type
    - Place orders with custom instructions
    - Track delivery in real-time
    - Rate and review their experience
    - Save favorite restaurants for quick reordering
    """
    
    # Execute the iterative workflow
    print("🎯 Starting NoteGPT Requirements Processing Workflow...")
    final_result = workflow.create_iterative_workflow(raw_requirement)
    
    print("\n🎉 FINAL RESULT:")
    print("=" * 50)
    print(final_result)
    print("=" * 50)

if __name__ == "__main__":
    main()






'''def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        AutomatedBaCrews().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AutomatedBaCrews().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        AutomatedBaCrews().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

'''

