from crewai import Agent

# Initialize the LLM you'll use for the agents

class BaAgents():
    """
    This class defines all the Business Analyst agents for the workflow.
    Each method returns a CrewAI Agent instance with a specific role, goal, and backstory.
    """
    def requirement_parser(self):
        return Agent(
            role='Requirement Parser',
            goal='To meticulously break down raw business requirements into a structured, understandable format.',
            backstory='An expert in systems analysis with a keen eye for detail, able to translate ambiguous business needs into clear, actionable points.',
            allow_delegation=False,
            verbose=True
        )

    def user_story_generator(self):
        return Agent(
            role='User Story Generator',
            goal='To create well-formed user stories from structured requirements, following the "As a [user], I want [goal], so that [reason]" format.',
            backstory='A seasoned Agile practitioner who excels at stepping into the user\'s shoes to articulate their needs and motivations clearly.',
            allow_delegation=False,
            verbose=True
        )

    def acceptance_criteria_generator(self):
        return Agent(
            role='Acceptance Criteria Generator',
            goal='To define clear, testable acceptance criteria for each user story using the "Given-When-Then" format.',
            backstory='A Quality Assurance specialist with a knack for identifying edge cases and defining precise conditions of satisfaction for development tasks.',
            allow_delegation=False,
            verbose=True
        )

    def requirement_classifier(self):
        return Agent(
            role='Requirement Classifier',
            goal='To classify user stories into functional and non-functional requirements to aid in planning and architecture.',
            backstory='A solutions architect who understands the importance of distinguishing between what a system does (functional) and how it performs (non-functional).',

            allow_delegation=False,
            verbose=True
        )

    def validator_and_refiner(self):
        return Agent(
            role='Validator and Refiner',
            goal='To critically review all generated artifacts (user stories, criteria, classifications) for clarity, consistency, and completeness, and provide actionable feedback for refinement.',
            backstory='A lead business analyst with years of experience, acting as the final quality gate. This agent ensures that the requirements are coherent and ready for the development team.',

            allow_delegation=False,
            verbose=True
        )

    def output_formatter(self):
        return Agent(
            role='Output Formatter',
            goal='To consolidate all the approved and refined information into a single, clean, and well-structured JSON output.',
            backstory='A data specialist who creates clean, machine-readable outputs, ensuring the final product is easy to parse and integrate with other systems like Jira or Azure DevOps.',

            allow_delegation=False,
            verbose=True
        )
