from langchain_core.messages import HumanMessage, AIMessage

def human_review_agent(state: dict):
    post_content = state['messages'][-1]['content']
    print("\nHere's the generated LinkedIn post:")
    print(post_content)
    
    while True:
        decision = input("\nDo you approve this post? (yes/no): ").lower()
        if decision == 'yes':
            state['messages'].append(HumanMessage(content="Post approved."))
            break
        elif decision == 'no':
            feedback = input("Please provide feedback for improvement: ")
            state['messages'].append(HumanMessage(content=f"Post not approved. Feedback: {feedback}"))
            state['current_agent'] = 'post_writer'  # Send back to post_writer for revision
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    
    return state