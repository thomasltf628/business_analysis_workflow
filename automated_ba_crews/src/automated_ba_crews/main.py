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
    - Track delivery in real-time
    - Rate and review their experience
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





"""
    We need a mobile app for food delivery that allows users to:
    - Browse restaurants by cuisine type
    - Place orders with custom instructions
    - Track delivery in real-time
    - Rate and review their experience
    - Save favorite restaurants for quick reordering
    """