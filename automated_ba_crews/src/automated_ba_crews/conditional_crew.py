from crewai import Crew, Process
import json
from ba_agents import BaAgents
from ba_tasks import BaTasks

class CustomWorkflow:
    def __init__(self):
        self.agents = BaAgents()
        self.tasks = BaTasks()
        self.max_iterations = 3

    def run(self, raw_requirement_text):
        print("🚀 Starting Business Analysis Workflow...")
        iteration_count = 0
        
        workflow_artifacts = {
            'raw_requirement_text': raw_requirement_text,
            'parsed_requirements': None,
            'user_stories': None,
            'stories_with_criteria': None,
            'classified_stories': None,
            'validation_feedback': None
        }

        while iteration_count < self.max_iterations:
            iteration_count += 1
            print(f"\n🔄 Iteration {iteration_count} of {self.max_iterations}")

            workflow_artifacts = self._execute_main_pipeline(workflow_artifacts)

            validation_result_str = self._execute_validation(workflow_artifacts['classified_stories'])
            workflow_artifacts['validation_feedback'] = validation_result_str
            
            try:
                validation_json = json.loads(validation_result_str)
                print(f"✅ Validation Result: {validation_json.get('status')}")

                if validation_json.get('status') == 'APPROVED':
                    print("✅ Validation Passed! Workflow complete.")
                    return self._create_final_output(workflow_artifacts['classified_stories'])
                else:
                    if iteration_count == self.max_iterations:
                        print("Maximum iterations reached, exit with refinement needed result")
                        break
                    print("⚠️ Validation issues found. Initiating refinement process...")
                    workflow_artifacts = self._execute_refinement_loop(validation_json, workflow_artifacts)

            except (json.JSONDecodeError, AttributeError) as e:
                print(f"❌ Error decoding validation JSON: {e}")
                print(f"Raw validation output received: {validation_result_str}")
                break
        
        print("🏁 Maximum iterations reached or unrecoverable error. Returning current artifacts.")
        return self._create_final_output(workflow_artifacts.get('classified_stories'))

    def _execute_main_pipeline(self, artifacts):
        if artifacts.get('parsed_requirements') is None:
             artifacts['parsed_requirements'] = self._execute_crew(
                "Parsing Requirements",
                [self.agents.requirement_parser()],
                [self.tasks.parse_requirement(context=artifacts['raw_requirement_text'])]
             )
        
        if artifacts.get('user_stories') is None:
            artifacts['user_stories'] = self._execute_crew(
                "Generating User Stories",
                [self.agents.user_story_generator()],
                [self.tasks.generate_stories(context=artifacts['parsed_requirements'])]
            )
        
        if artifacts.get('stories_with_criteria') is None:
            artifacts['stories_with_criteria'] = self._execute_crew(
                "Adding Acceptance Criteria",
                [self.agents.acceptance_criteria_generator()],
                [self.tasks.add_acceptance_criteria(context=artifacts['user_stories'])]
            )

        if artifacts.get('classified_stories') is None:
            artifacts['classified_stories'] = self._execute_crew(
                "Classifying Stories",
                [self.agents.requirement_classifier()],
                [self.tasks.classify_stories(context=artifacts['stories_with_criteria'])]
            )
        
        return artifacts

    def _execute_validation(self, classified_stories):
        return self._execute_crew(
            "Validating Artifacts",
            [self.agents.validator_and_refiner()],
            [self.tasks.validate_artifacts(context=classified_stories)]
        )

    def _execute_refinement_loop(self, validation_json, artifacts):
        feedback = validation_json.get('feedback', '')
        print(f"🔬 Refinement Feedback: {feedback}") # A list of dict
        feedback_str = ""
        try:
            for issue in feedback:
                temp_list_for_each_issue = ['{' + key + ':' + value + '}' for key,value in issue.items()]
                feedback_str += ",".join(temp_list_for_each_issue)
        except AttributeError as e:
            print(e, "attempting conversion to str")
            feedback_str = str(feedback)
            
        if any(term in feedback_str.lower() for term in ['user story', 'story', 'as a']):
            print("🔄 Routing to User Story Generator for refinement.")
            refined_stories = self._execute_crew(
                "Refining User Stories",
                [self.agents.user_story_generator()],
                [self.tasks.generate_stories(context=artifacts['parsed_requirements'], feedback=feedback)]
            )
            artifacts.update({
                'user_stories': refined_stories,
                'stories_with_criteria': None,
                'classified_stories': None
            })

        elif any(term in feedback_str.lower() for term in ['acceptance criteria', 'criteria']):
            print("🔄 Routing to Acceptance Criteria Generator for refinement.")
            refined_criteria = self._execute_crew(
                "Refining Acceptance Criteria",
                [self.agents.acceptance_criteria_generator()],
                [self.tasks.add_acceptance_criteria(context=artifacts['user_stories'], feedback=feedback)]
            )
            artifacts.update({
                'stories_with_criteria': refined_criteria,
                'classified_stories': None
            })
        
        else:
            print("🔄 Defaulting to Requirement Parser for refinement.")
            refined_parsing = self._execute_crew(
                "Refining Parsed Requirements",
                [self.agents.requirement_parser()],
                [self.tasks.parse_requirement(context=artifacts['raw_requirement_text'], feedback=feedback)]
            )
            artifacts.update({
                'parsed_requirements': refined_parsing,
                'user_stories': None,
                'stories_with_criteria': None,
                'classified_stories': None
            })

        return artifacts

    def _create_final_output(self, final_artifacts_str):
        if not final_artifacts_str:
            print("⚠️ No artifacts to format. Returning empty JSON.")
            return "{}"
            
        return self._execute_crew(
            "Formatting Final Output",
            [self.agents.output_formatter()],
            [self.tasks.format_final_output(context=final_artifacts_str)]
        )

    def _execute_crew(self, name, agents_list, tasks_list):
        print(f"\n--- Running Crew: {name} ---")
        crew = Crew(
            agents=agents_list,
            tasks=tasks_list,
            process=Process.sequential,
            verbose=True
        )
        result = crew.kickoff()
        return str(result)

