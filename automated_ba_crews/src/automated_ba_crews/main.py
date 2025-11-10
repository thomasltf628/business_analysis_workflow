import sys
import json
from conditional_crew import CustomWorkflow
from mcp_context_gatherer import MCPContextGatherer
from dotenv import load_dotenv
load_dotenv()


def main():
    raw_requirement_text_file =  input("Please enter the file path: ") # raw business requirement
    try:
        with open(raw_requirement_text_file, 'r', encoding='utf-8') as file:
            raw_requirement_text = file.read()
    except FileNotFoundError:
        print("Error: File not found!")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    print("===============================================")
    print("      Automated Business Analyst Agent      ")
    print("===============================================")
    print("\nProcessing the following requirement:\n")
    print(raw_requirement_text)
    print("-----------------------------------------------")

    # MCP Context Gathering Phase
    print("\n")
    print("Starting MCP Context Gathering Phase")
    enable_mcp = input("Enable MCP context gathering? (y/n, default=y): ").strip().lower()
    
    if enable_mcp != 'n':
        try:
            mcp_gatherer = MCPContextGatherer()
            enriched_requirement = mcp_gatherer.gather_context(raw_requirement_text)
            print("\n Context gathering complete!")
            print("\n Enriched Requirement Preview:")
            print("=" * 50)
            #print(enriched_requirement[:500] + "..." if len(enriched_requirement) > 500 else enriched_requirement)
            print(enriched_requirement)
            print("=" * 50)
            
            # Use enriched requirement for workflow
            requirement_to_process = enriched_requirement
        except Exception as e:
            print(f"\n MCP context gathering failed: {e}")
            print("Continuing with original requirement...")
            requirement_to_process = raw_requirement_text
    else:
        print("Skipping MCP context gathering...")
        requirement_to_process = raw_requirement_text

    # --- Execute Workflow ---
    print("\n🤖 Starting CrewAI Agent Workflow...")
    workflow = CustomWorkflow()
    final_result_str = workflow.run(requirement_to_process)

    # --- Display Final Output ---
    print("\n\n===============================================")
    print("          ✅ Workflow Complete ✅          ")
    print("===============================================")
    print("Final JSON Output:")

    try:
        # Try to parse and pretty-print the JSON
        start_index = final_result_str.find('[') # Make sure the str start and end with []
        end_index = final_result_str.rfind(']')
        final_json_str_array = final_result_str[start_index:end_index + 1]

        final_json = json.loads(final_json_str_array)
        print(json.dumps(final_json, indent=2))
        with open('business_requirement.json', 'w') as f:
            json.dump(final_json, f, indent=2)
    except (json.JSONDecodeError, TypeError):
        print("Could not parse the final output as JSON. Displaying raw output:")
        print(final_result_str)
        with open('business_requirement.txt', 'w') as f:
            f.write(final_result_str)

if __name__ == "__main__":
    main()
