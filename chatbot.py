import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv()

client = openai.OpenAI()

model = "gpt-4o-mini"

# # --Creating the Assistant--

# ask_margot_assistant = client.beta.assistants.create(
#     name='Ask Margot Bot',
#     instructions='You are Margot, a friendly travel nurse assistant. Provide short, conversational responses based on hospital reviews, summarizing ratings as sentiments (e.g., 5 = excellent). Avoid detailed attributes unless asked, focusing on the user’s needs with empathetic, tailored replies. Match their tone and guide the conversation with clarifying questions. If data is missing, suggest alternatives or offer further help. Keep it engaging and helpful.',
#     model=model
# )

assistant_id = "asst_q3EwkoYBplNvgf6IRrwx5eOZ"

def ask_margot_bot():
    print("Ask Margot Bot: Hi! Ask me anything about hospitals. Type 'exit' to quit.\n")
    
    # Create a new thread when the chatbot starts
    thread = client.beta.threads.create(messages=[])
    thread_id = thread.id

    while True:
        user_input = input("You: ").strip()
        print()

        if user_input.lower() == "exit":
            print("Ask Margot Bot: Goodbye, have a great day!")
            break

        try:
            # Add the user's message to the thread
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role='user',
                content=user_input
            )

            # Run the assistant for the current thread
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions=""
            )

            # Fetch all messages in the thread to get the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            assistant_responses = []

            if messages.data:
                # Extract assistant messages
                for message in messages.data:
                    if message.role == 'assistant':
                        for content_block in message.content:
                            if content_block.type == 'text':
                                assistant_responses.append(content_block.text.value)
            
            # Display the latest assistant response
            if assistant_responses:
                print(f"Ask Margot Bot: {assistant_responses[-1]}")
            else:
                print("Ask Margot Bot: Hmm, I didn't understand that. Could you rephrase?")
        
        except Exception as e:
            print(f"Ask Margot Bot: Oops, something went wrong! ({str(e)})")

if __name__ == "__main__":
    ask_margot_bot()
