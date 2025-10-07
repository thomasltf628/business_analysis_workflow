from crewai import Agent
import yaml

agent_config_path = r"C:\Users\super\OneDrive - Durham College\skills_lab\IntactAIdev\automated_ba_crews\src\automated_ba_crews\config\agents.yaml"

with open(r'automated_ba_crews\src\automated_ba_crews\config\agents.yaml', 'r') as file:
    config = yaml.safe_load(file)

class BaAgents():
    def get_agent(self, agent_name):
        if agent_name in config:
            return Agent(
                role=config[agent_name]['role'],
                goal=config[agent_name]['goal'],
                backstory=config[agent_name]['backstory'],
                allow_delegation=config[agent_name]['allow_delegation'],
                verbose=config[agent_name]['verbose']
            )
        else:
            raise ValueError(f"Agent '{agent_name}' not found in configuration")
    
    # Keep individual methods for convenience
    def requirement_parser(self):
        return self.get_agent('requirement_parser')
    
    def user_story_generator(self):
        return self.get_agent('user_story_generator')
    
    def acceptance_criteria_generator(self):
        return self.get_agent('acceptance_criteria_generator')
    
    def requirement_classifier(self):
        return self.get_agent('requirement_classifier')
    
    def validator_and_refiner(self):
        return self.get_agent('validator_and_refiner')
    
    def workflow_router(self):
        return self.get_agent('workflow_router')
    
    def output_formatter(self):
        return self.get_agent('output_formatter')
