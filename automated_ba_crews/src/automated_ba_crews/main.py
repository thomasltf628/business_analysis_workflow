import os
import json
from conditional_crew import CustomWorkflow
from dotenv import load_dotenv
load_dotenv()


def main():

    # --- Input Requirement ---
    # This is the raw business requirement text that will be processed.
    raw_requirement_text =  """
    We need a mobile app for food delivery that allows users to:
    - Browse restaurants by cuisine type
    - Place orders with custom instructions
    - Track delivery in real-time
    - Rate and review their experience
    - Save favorite restaurants for quick reordering
    """

    print("===============================================")
    print("      Automated Business Analyst Agent      ")
    print("===============================================")
    print("\nProcessing the following requirement:\n")
    print(raw_requirement_text)
    print("-----------------------------------------------")

    # --- Execute Workflow ---

    workflow = CustomWorkflow()
    final_result_str = workflow.run(raw_requirement_text)

    # --- Display Final Output ---
    print("\n\n===============================================")
    print("          ✅ Workflow Complete ✅          ")
    print("===============================================")
    print("Final JSON Output:")

    try:
        # Try to parse and pretty-print the JSON
        final_json = json.loads(final_result_str)
        print(json.dumps(final_json, indent=2))
    except (json.JSONDecodeError, TypeError):
        print("Could not parse the final output as JSON. Displaying raw output:")
        print(final_result_str)

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

    """
    We are building a new feature for our e-commerce platform called "Wishlist".
    A user should be able to add products to their personal wishlist.
    They should also be able to view their wishlist and remove items from it.
    The wishlist needs to be saved to their account so they can see it
    when they log in again later. We also want to eventually add a "share wishlist"
    feature, but that's for a future release. For now, just focus on the core
    add, view, and remove functionality. The system must also be secure and
    ensure that users can only see their own wishlists.
    """