"""
MCP Context Gatherer for Business Analyst Agents, fetching external information using MCP tools before requirement processing
"""
import os
import json
from typing import Dict, List, Optional
import anthropic

#Gathers contextual information using Claude's MCP tools
class MCPContextGatherer:
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.model = "claude-sonnet-4-20250514"
        
    def analyze_requirement_for_context_needs(self, raw_requirement: str) -> Dict:
        """
        First pass: Identify what external information is needed
        Returns a structured list of information gathering tasks
        """
        analysis_prompt = f"""
                            You are a Business Analyst assistant. Analyze this raw requirement and identify what external information should be gathered before writing user stories.

                            Raw Requirement:
                            ---
                            {raw_requirement}
                            ---

                            Identify if the requirement needs:
                            1. Web searches for industry standards, best practices, or regulatory information
                            2. API calls to fetch current data (exchange rates, compliance thresholds, etc.)
                            3. Reading internal documentation files
                            4. Current news or recent changes in relevant domains

                            Respond with a JSON object with this structure:
                            {{
                            "needs_web_search": true/false,
                            "web_search_queries": ["query1", "query2"],
                            "needs_api_data": true/false,
                            "api_endpoints": ["description of data needed"],
                            "needs_file_reading": true/false,
                            "file_hints": ["type of files to look for"],
                            "needs_current_news": true/false,
                            "news_topics": ["topic1", "topic2"],
                            "reasoning": "explanation of why this information is needed"
                            }}

                            Only include queries/endpoints that are genuinely needed for writing accurate requirements.
                            """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        # Extract JSON from response
        content = response.content[0].text
        try:
            # Find JSON in response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            return json.loads(json_str)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not parse context analysis: {e}")
            return {"needs_web_search": False}
    
    def gather_context(self, raw_requirement: str) -> str:
        """
        Main method: Analyzes requirement and gathers all necessary context
        Returns enriched context string to pass to BA agents
        """
        print("\n Analyzing requirement for context needs")
        context_needs = self.analyze_requirement_for_context_needs(raw_requirement)
        
        print(f"Context Needs Identified:")
        print(f"  - Web Search: {context_needs.get('needs_web_search', False)}") # If No json return then False
        print(f"  - API Data: {context_needs.get('needs_api_data', False)}")
        print(f"  - File Reading: {context_needs.get('needs_file_reading', False)}")
        print(f"  - Current News: {context_needs.get('needs_current_news', False)}")
        
        # Now use MCP tools to gather the actual information
        gathered_info = self._execute_information_gathering(
            raw_requirement, 
            context_needs
        )
        
        # Format the enriched context
        enriched_context = self._format_enriched_context(
            raw_requirement,
            context_needs,
            gathered_info
        )
        
        return enriched_context
    
    def _execute_information_gathering(
        self, 
        raw_requirement: str, 
        context_needs: Dict
    ) -> Dict:
        """
        Uses Claude with MCP tools to actually gather the information
        """
        print("\n Gathering external information using MCP tools")
        
        # Build a prompt that tells Claude to use MCP tools
        gathering_prompt = f"""
                            You have access to web search and other tools. Use them to gather information for this business requirement.

                            Raw Requirement:
                            ---
                            {raw_requirement}
                            ---

                            Information Needed:
                            {json.dumps(context_needs, indent=2)}

                            Please:
                            1. Search the web for any regulatory, compliance, or industry standard information mentioned
                            2. Find current best practices for similar systems
                            3. Look up any technical specifications or data formats that should be used
                            4. Check for recent changes or updates in relevant domains

                            Provide a comprehensive summary of all findings that would help a BA write accurate user stories.
                            """
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=4000,
            messages=[{"role": "user", "content": gathering_prompt}]
        )
        
        gathered_text = response.content[0].text
        
        return {
            "gathered_information": gathered_text,
            "sources_consulted": "MCP web search and tools"
        }
    
    def _format_enriched_context(
        self,
        original_requirement: str,
        context_needs: Dict,
        gathered_info: Dict
    ) -> str:
        """
        Formats the original requirement with gathered context
        """
        enriched = f"""
                    # ENRICHED BUSINESS REQUIREMENT

                    ## Original Requirement
                    {original_requirement}

                    ## Additional Context Gathered
                    {gathered_info.get('gathered_information', 'No additional information gathered')}

                    ## Context Analysis
                    Reasoning: {context_needs.get('reasoning', 'N/A')}

                    ---
                    The above context should inform all user stories, acceptance criteria, and classifications.
                    """
        return enriched


class MCPAwareAgent:
    """
    Extension methods for BA agents to request additional MCP queries during processing
    """
    
    @staticmethod
    def request_additional_context(query: str) -> str:
        """
        Allows an agent to request additional information mid-workflow
        """
        client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
        
        prompt = f"""
                A Business Analyst agent needs additional information:

                Query: {query}

                Please search for and provide the requested information.
                """
        
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
