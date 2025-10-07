#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from automated_ba_crews.crew import AutomatedBaCrews
from dotenv import load_dotenv
from automated_ba_crews.src.automated_ba_crews.ba_agents import BaAgents
from automated_ba_crews.src.automated_ba_crews.ba_tasks import BaTasks
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

class BaWorkflow:  
    def __init__(self):
        pass

    def run(self):
        agents = BaAgents()
        tasks = BaTasks()

        requirement_parser = agents.get_agent('requirement_parser')
        user_story_generator = agents.get_agent('user_story_generator')
        acceptance_criteria_generator = agents.get_agent('acceptance_criteria_generator')
        requirement_classifier = agents.get_agent('requirement_classifier')
        validator_and_refiner = agents.get_agent('validator_and_refiner')
        workflow_router = agents.get_agent('workflow_router')
        output_formatter = agents.get_agent('output_formatter')
        
        parse_requirement = tasks.get_task('parse_requirement')
        generate_stories =  tasks.get_task('generate_stories')
        add_acceptance_criteria = tasks.get_task('add_acceptance_criteria')
        classify_stories = tasks.get_task('classify_stories')
        validate_artifacts = tasks.get_task('validate_artifacts')
        format_final_output = tasks.get_task('format_final_output')

        
        """inputs = {
            'topic': 'AI LLMs',
            'current_year': str(datetime.now().year)
        }"""
        
        """try:
            AutomatedBaCrews().crew().kickoff(inputs=inputs)
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")"""






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