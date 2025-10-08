from crewai import Task
import yaml
from ba_agents import BaAgents # Use relative import

class BaTasks():
    def __init__(self):
        # Correctly load the YAML config relative to the file's location if needed
        # For this example, assuming a flat structure or correct PYTHONPATH
        with open(r'automated_ba_crews/src/automated_ba_crews/config/tasks.yaml', 'r') as file:
            self.config = yaml.safe_load(file)
        self.agents = BaAgents()

    def _create_task(self, task_name, context, feedback=None):
        """
        A private helper method to create a Task instance from configuration.
        It dynamically injects context and feedback into the task description.
        """
        task_config = self.config[task_name]
        
        # Create a feedback section only if feedback is provided
        feedback_section = ""
        if feedback:
            feedback_section = f"""
            A previous attempt required refinement. Please address the following feedback:
            ---
            {feedback}
            ---
            """

        # Format the description with the provided context and feedback
        description = task_config['description'].format(
            context=context,
            feedback_section=feedback_section
        )

        return Task(
            description=description,
            expected_output=task_config['expected_output'],
            agent=getattr(self.agents, task_config['agent'])()
        )

    # Individual task methods now accept context and optional feedback
    def parse_requirement(self, context, feedback=None):
        return self._create_task('parse_requirement', context, feedback)
    
    def generate_stories(self, context, feedback=None):
        return self._create_task('generate_stories', context, feedback)
    
    def add_acceptance_criteria(self, context, feedback=None):
        return self._create_task('add_acceptance_criteria', context, feedback)
    
    def classify_stories(self, context, feedback=None):
        return self._create_task('classify_stories', context, feedback)
    
    def validate_artifacts(self, context):
        # Validation task doesn't need a feedback loop for itself
        return self._create_task('validate_artifacts', context)
    
    def format_final_output(self, context):
        return self._create_task('format_final_output', context)
