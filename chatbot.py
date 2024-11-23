import openai
from dotenv import find_dotenv, load_dotenv

load_dotenv()
#openai.api_key = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()

model = "gpt-4o-mini"

# # --Creating the Assistant--

# ask_margot_assistant = client.beta.assistants.create(
#     name='Ask Margot Bot',
#     instructions='You are Margot, a friendly travel nurse assistant. Provide short, conversational responses based on hospital reviews, summarizing ratings as sentiments (e.g., 5 = excellent). Avoid detailed attributes unless asked, focusing on the user’s needs with empathetic, tailored replies. Match their tone and guide the conversation with clarifying questions. If data is missing, suggest alternatives or offer further help. Keep it engaging and helpful.',
#     model=model
# )

# --Create the Thread--
thread = client.beta.threads.create(
    messages=[
        {
            'role':'user',
            'content': 'Show me hospitals in San Francisco'
        }
    ]
)

# --Hardcode the ID's--
assistant_id = "asst_q3EwkoYBplNvgf6IRrwx5eOZ"
thread_id = "thread_b41xDR2sMjHbzkzaV5aXxNoX"

msg = 'Show the best hospitals for pay in San Francisco?'
msg = client.beta.threads.messages.create(
    thread_id=thread_id,
    role='user',
    content=msg
)

# --Run our Assistant--
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions=""
)

# -- Retrieve the Assistant's Response --
run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
messages = client.beta.threads.messages.list(thread_id=thread_id)

assistant_responses = []

# Check if there are any messages in the thread
if messages.data:
    # Iterate over all messages to extract assistant responses
    for message in messages.data:
        if message.role == 'assistant':  # Filter for assistant messages
            for content_block in message.content:
                if content_block.type == 'text':  # Ensure it's a text content block
                    assistant_responses.append(content_block.text.value)

# Print all extracted assistant responses
print(assistant_responses[-1])
