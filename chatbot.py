import os
from dotenv import load_dotenv
import openai

import time
import logging
from datetime import datetime

#Load environment
load_dotenv()
#Create the client to be used for user's interaction
client = openai.OpenAI()

#Retrieve assistant's ID
assis_id = os.getenv('ASSISTANT_ID')

#Create the user thread for current user interaction
thread = client.beta.threads.create()
thread_id = thread.id

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
        """
        Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
        :param thread_id: The ID of the thread.
        :param run_id: The ID of the run.
        :param sleep_interval: Time in seconds to wait between checks.
        """
        while True:
            try:
                run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
                if run.completed_at:
                    elapsed_time = run.completed_at - run.created_at
                    formatted_elapsed_time = time.strftime(
                        "%H:%M:%S", time.gmtime(elapsed_time)
                    )
                    print(f"Run completed in {formatted_elapsed_time}")
                    logging.info(f"Run completed in {formatted_elapsed_time}")
                    # Get messages here once Run is completed!
                    messages = client.beta.threads.messages.list(thread_id=thread_id)
                    last_message = messages.data[0]
                    response = last_message.content[0].text.value
                    print(f"Assistant Response: {response}")
                    break
            except Exception as e:
                logging.error(f"An error occurred while retrieving the run: {e}")
                break
            logging.info("Waiting for run to complete...")
            time.sleep(sleep_interval)

#Initial statement for user to respond to
print("Ask Margot Bot: Hi! Ask me anything about hospitals. Type 'exit' to quit.\n")

#Loop until user leaves or exits manually
while True:
    message = input("You: ").strip()
    print()

    #Allows user to exit
    if message == "exit" or message == "Exit":
        break

    #Message is created using user's input to send to the API
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    #Runs the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assis_id,
        instructions=""
    )

    wait_for_run_completion(client=client,
                            thread_id=thread_id,
                            run_id=run.id)
