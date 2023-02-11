from dotenv import load_dotenv
import os
from halo import Halo
import logging
import pickle
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

backup_dir = './backup'
export_dir = './export'

os.makedirs(backup_dir,exist_ok=True)
os.makedirs(export_dir,exist_ok=True)

def push_in_queue(item): 
    global queue, current_prompt_tokens, max_prompt_tokens
    queue.append(item) 
    current_prompt_tokens += item[1]
    while current_prompt_tokens > max_prompt_tokens:
        current_prompt_tokens -= queue[0][1]
        queue.pop(0)

header_color = '\033[1;30;47m'
text_color = '\033[0;36m'
prompt_color = '\033[0;35m'

os.system('clear')

print(header_color + '\n Welcome to DeepChat! ' + '\033[0m')
print(text_color + '\n DeepChat is a simple command-line chatbot powered by OpenAI. ' + '\033[0m')
print(text_color + ' You can ask DeepChat any question and it will do its best to provide a relevant answer.' + '\033[0m')

print(header_color + '\n Instructions: ' + '\033[0m')
print(text_color + '\n 1. Type in your question. ' + '\033[0m')
print(text_color + ' 2. Press enter to send. ' + '\033[0m')
print(text_color + ' 3. Type "help" to see the available commands' + '\033[0m')
print(text_color + ' 4. Type "exit" to quit the program.\n' + '\033[0m')

print(text_color + ' Let\'s get started!\n' + '\033[0m')

while True:
    prompt = input(prompt_color + "Prompt: \033[0m")
    if prompt == 'exit':
        print(header_color + '\n Thank you for using DeepChat! Have a great day. ' + '\033[0m')
        print("")
        break
    elif prompt == 'new':
        queue = []
        current_prompt_tokens = 0
        print(header_color + '\n New conversation started. ' + '\033[0m')
        print("")
        continue
    elif prompt == 'export':
        filename = input(prompt_color + "\nFilename: \033[0m")
        filename = os.path.join(export_dir,filename) + '.txt'
        with open(filename, 'w') as f:
            f.write("\n".join([x[0] for x in queue]))
        print(header_color + '\n Conversation exported to ' + filename + '\033[0m')
        print("")
        continue
    elif prompt == 'save':
        filename = input(prompt_color + "\nFilename: \033[0m")
        filename = os.path.join(backup_dir,filename) + '.pickle'
        with open(filename, 'wb') as f:
            pickle.dump(queue, f)
        print(header_color + '\n Conversation saved to ' + filename + '\033[0m')
        print("")
        continue
    elif prompt == 'list':
        chats = os.listdir(backup_dir)
        print(header_color + '\n Chats: ' + '\033[0m' + '\n')
        for chat in enumerate(chats):
            msg = f"{chat[0]+1}. {chat[1].split('.')[0]}"
            print(text_color + msg + '\033[0m')
        print("")
        continue
    elif prompt == 'load':
        filename = input(prompt_color + "\nFilename: \033[0m")
        filename = os.path.join(backup_dir,filename) + '.pickle'
        if not os.path.exists(filename):
            print(header_color + '\n File not found. ' + '\033[0m')
            continue
        with open(filename, 'rb') as f:
            queue = pickle.load(f)
        current_prompt_tokens = sum([x[1] for x in queue])
        print(header_color + '\n Conversation loaded from ' + filename + '\033[0m')
        print("")
        continue
    elif prompt == 'help':
        print(header_color + '\n Commands: \n' + '\033[0m')
        print(text_color + ' new: Start a new conversation.' + '\033[0m')
        print(text_color + ' export: Export the conversation to a file.' + '\033[0m')
        print(text_color + ' save: Save the conversation to a file.' + '\033[0m')
        print(text_color + ' list: List all saved conversations.' + '\033[0m')
        print(text_color + ' load: Load a saved conversation.' + '\033[0m')
        print(text_color + ' exit: Exit the program.\n' + '\033[0m')
        continue
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

