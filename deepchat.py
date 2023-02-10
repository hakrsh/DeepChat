from dotenv import load_dotenv
import os
from halo import Halo
import logging
logging.basicConfig(level=logging.ERROR,filename='deepchat.log',filemode='w',format='%(name)s - %(levelname)s - %(message)s')


load_dotenv()

if os.getenv("OPENAI_API_KEY") is None:
    print('OPENAI_API_KEY is not set. Please set the OPENAI_API_KEY environment variable.')
    exit()

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

queue = []
max_prompt_tokens = 3000
current_prompt_tokens = 0


def push_in_queue(item): 
    global queue, current_prompt_tokens, max_prompt_tokens
    queue.append(item) 
    current_prompt_tokens += item[1]
    while current_prompt_tokens > max_prompt_tokens:
        current_prompt_tokens -= queue[0][1]
        queue.pop(0)

header_color = '\033[1;30;47m'
text_color = '\033[0;36m'
prompt_color = '\033[0;34m'

os.system('clear')

print(header_color + '\n Welcome to DeepChat! ' + '\033[0m')
print(text_color + '\n DeepChat is a simple command-line chatbot powered by OpenAI. ' + '\033[0m')
print(text_color + ' You can ask DeepChat any question and it will do its best to provide a relevant answer.' + '\033[0m')

print(header_color + '\n Instructions: ' + '\033[0m')
print(text_color + '\n 1. Type in your question. ' + '\033[0m')
print(text_color + ' 2. Press enter to send. ' + '\033[0m')
print(text_color + ' 3. Type "exit" to quit the program.\n' + '\033[0m')

print(text_color + ' Let\'s get started!\n' + '\033[0m')

while True:
    prompt = input(prompt_color + "\nPrompt: \033[0m")
    if prompt == 'exit':
        print(header_color + '\n Thank you for using DeepChat! Have a great day. ' + '\033[0m')
        break
    print("")
    history = "\n".join([x[0] for x in queue])
    combined_prompt = f'{history}\n{prompt}\n'
    with Halo(text='Thinking...', spinner='dots'):
        try:
            completion = openai.Completion().create(engine='text-davinci-003',prompt=combined_prompt, max_tokens=1000)
            completion_tokens = completion.usage.completion_tokens
            answer = completion.choices[0].text
            print(f'\n{answer}')
            push_in_queue([f'Q: {prompt}\n{answer}\n', completion_tokens])
            print("")
        except Exception as e:
            print('Oops, something went wrong. Try again!')
            logging.error(e)
            logging.error(f'Prompt: {prompt}')
            logging.error(f'History: {history}')
            logging.error(f'Combined Prompt: {combined_prompt}')
            logging.error(f'Completion: {completion}')
            logging.error(f'Current Prompt Tokens: {current_prompt_tokens}')
            logging.error(f'Max Prompt Tokens: {max_prompt_tokens}')
            logging.error(f'Queue: {queue}')

