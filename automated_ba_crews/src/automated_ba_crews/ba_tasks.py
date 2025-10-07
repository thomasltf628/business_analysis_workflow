from crewai import Task
from ba_agents import BaAgents
import yaml

with open(r'automated_ba_crews\src\automated_ba_crews\config\tasks.yaml', 'r') as file:
    config = yaml.safe_load(file)

ba_agents = BaAgents()

class BaTasks():
    def get_task(self, task_name):
        """Generic method to get any task by name"""
        if task_name in config:
            task_config = config[task_name]
            task = Task(
                description=task_config['description'],
                expected_output=task_config['expected_output'],
                agent=getattr(ba_agents, task_config['agent'])()
            )
            
            # Add context if specified
            if 'context' in task_config:
                context_tasks = [getattr(self, ctx)() for ctx in task_config['context']]
                task.context = context_tasks
                
            return task
        else:
            raise ValueError(f"Task '{task_name}' not found in configuration")
    
    # Individual task methods for convenience
    def parse_requirement(self):
        return self.get_task('parse_requirement')
    
    def generate_stories(self):
        return self.get_task('generate_stories')
    
    def add_acceptance_criteria(self):
        return self.get_task('add_acceptance_criteria')
    
    def classify_stories(self):
        return self.get_task('classify_stories')
    
    def validate_artifacts(self):
        return self.get_task('validate_artifacts')
    
    def format_final_output(self):
        return self.get_task('format_final_output')
    
