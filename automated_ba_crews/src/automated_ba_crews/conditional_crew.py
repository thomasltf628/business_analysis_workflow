from crewai import Task, Crew, Process
import json
from ba_agents import BaAgents
from ba_tasks import BaTasks

class CustomWorkflow:
    def __init__(self, agents: BaAgents, tasks: BaTasks):
        self.agents = agents
        self.tasks = tasks
        self.max_iterations = 3  # Prevent infinite loops
        
        
    def create_iterative_workflow(self, raw_requirement_text):
        """Create the iterative workflow based on the flowchart"""
        
        # Initial sequential flow
        initial_tasks = [
            self.tasks.parse_requirement(),
            self.tasks.generate_stories(),
            self.tasks.add_acceptance_criteria(),
            self.tasks.classify_stories(),
            self.tasks.validate_artifacts()
        ]
        
        # Create initial crew for first pass
        initial_crew = Crew(
            agents=[
                self.agents.requirement_parser(),
                self.agents.user_story_generator(),
                self.agents.acceptance_criteria_generator(),
                self.agents.requirement_classifier(),
                self.agents.validator_and_refiner()
            ],
            tasks=initial_tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Execute initial flow
        print("Starting initial requirements processing...")
        initial_result = initial_crew.kickoff(inputs={
            'raw_requirement_text': raw_requirement_text
        })
        
        # Check validation result and handle iterations
        return self._handle_validation_iterations(initial_result, raw_requirement_text)
    
    def _handle_validation_iterations(self, initial_result, raw_requirement_text):
        """Handle the iterative refinement process"""
        iteration_count = 0
        
        while iteration_count < self.max_iterations:
            iteration_count += 1
            print(f"\n🔄 Iteration {iteration_count}")
            
            # Parse the validation result
            validation_result = self._parse_validation_result(initial_result)
            
            if validation_result.get('status') == 'APPROVED':
                print("✅ Validation passed! Formatting final output...")
                return self._create_final_output(initial_result)
            else:
                print("⚠️  Validation issues found. Routing for refinement...")
                refinement_agent = self._determine_refinement_agent(validation_result)
                initial_result = self._execute_refinement(
                    refinement_agent, initial_result, raw_requirement_text
                )
        
        print("❌ Maximum iterations reached. Returning current state.")
        return self._create_final_output(initial_result)
    
    def _parse_validation_result(self, validation_output):
        """Parse the validation output to determine status and issues"""
        try:
            # Try to parse as JSON first
            if isinstance(validation_output, str):
                return json.loads(validation_output)
            else:
                return validation_output
        except:
            # Fallback: simple text analysis
            if 'APPROVED' in str(validation_output).upper():
                return {'status': 'APPROVED', 'feedback': 'All checks passed.'}
            else:
                return {
                    'status': 'REVISION_NEEDED', 
                    'feedback': str(validation_output)
                }
    
    def _determine_refinement_agent(self, validation_result):
        """Determine which agent needs to refine based on validation feedback"""
        feedback = validation_result.get('feedback', '').lower()
        
        if any(term in feedback for term in ['user story', 'story', 'as a']):
            print("🔄 Routing to User Story Generator for refinement")
            return self.agents.user_story_generator()
        elif any(term in feedback for term in ['acceptance criteria', 'criteria', 'given when then']):
            print("🔄 Routing to Acceptance Criteria Generator for refinement")
            return self.agents.acceptance_criteria_generator()
        elif any(term in feedback for term in ['classification', 'functional', 'non-functional']):
            print("🔄 Routing to Requirement Classifier for refinement")
            return self.agents.requirement_classifier()
        else:
            print("🔄 Routing to Requirement Parser for refinement")
            return self.agents.requirement_parser()
    
    def _execute_refinement(self, refinement_agent, previous_result, raw_requirement_text):
        """Execute refinement with the specified agent"""
        # Create refinement task based on the agent type
        if refinement_agent.role == "User Story Generator":
            refinement_task = Task(
                description=f"""
                Refine the user stories based on the following feedback:
                {previous_result}
                
                Original requirement: {raw_requirement_text}
                """,
                expected_output="Refined user stories in proper format",
                agent=refinement_agent
            )
        elif refinement_agent.role == "Acceptance Criteria Generator":
            refinement_task = Task(
                description=f"""
                Refine the acceptance criteria based on the following feedback:
                {previous_result}
                """,
                expected_output="Refined acceptance criteria",
                agent=refinement_agent
            )
        elif refinement_agent.role == "Requirement Classifier":
            refinement_task = Task(
                description=f"""
                Refine the requirement classifications based on the following feedback:
                {previous_result}
                """,
                expected_output="Refined classifications",
                agent=refinement_agent
            )
        else:  # Requirement Parser
            refinement_task = Task(
                description=f"""
                Re-analyze and refine the requirement parsing based on the following feedback:
                {previous_result}
                
                Original requirement: {raw_requirement_text}
                """,
                expected_output="Refined requirement parsing",
                agent=refinement_agent
            )
        
        # Execute refinement
        refinement_crew = Crew(
            agents=[refinement_agent],
            tasks=[refinement_task],
            process=Process.sequential,
            verbose=True
        )
        
        return refinement_crew.kickoff()
    
    def _create_final_output(self, final_result):
        """Create the final formatted output"""
        print("📦 Creating final formatted output...")
        
        final_format_task = Task(
            description=f"""
            Format the following finalized user stories and all associated data into a clean, structured JSON format:
            {final_result}
            """,
            expected_output="A single JSON string representing a list of user story objects",
            agent=self.agents.output_formatter()
        )
        
        final_crew = Crew(
            agents=[self.agents.output_formatter()],
            tasks=[final_format_task],
            process=Process.sequential,
            verbose=True
        )
        
        return final_crew.kickoff()