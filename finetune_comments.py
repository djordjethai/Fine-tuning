# ne korastiti ovaj kod, vec koristiti noviji, za Chat Modele
# Import necessary libraries
import my_functions
import openai
import os
import sys
sys.path.insert(0, r'C:\Users\djordje\PythonGPT3Tutorial')


# Read OpenAI API key from file
openai.api_key = my_functions.open_file('openaiapikey.txt')
open_ai_api_key = os.getenv(openai.api_key)

# Get user input for model name
ft_model = input("Unesi ime modela: ")

# Upload file and finetune model
resp = my_functions.file_upload('plots.jsonl')
my_functions.finetune_model(resp['id'], ft_model, 'davinci')

# List all finetuned models
print(my_functions.finetune_list())

# Get user input for finetuned model ID
ft_id = input("Unesi ID finetune-a: ")

# Get events for finetuned model
print(my_functions.finetune_events(ft_id))

# Get details for finetuned model
print(my_functions.finetune_get(ft_id))
