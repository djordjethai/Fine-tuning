# ft_id = input("Unesi ID finetune-a: ")
# print(finetune_events(ft_id))
# print(finetune_get(ft_id))

# Import necessary libraries
import requests
import openai
from pprint import pprint

# Read OpenAI API key from file
with open('openaiapikey.txt', 'r') as infile:
    open_ai_api_key = infile.read()
openai.api_key = open_ai_api_key

# Function to upload a file to OpenAI
def file_upload(filename, purpose='fine-tune'):
    resp = openai.File.create(purpose=purpose, file=open(filename))
    pprint(resp)
    return resp

# Function to list all files uploaded to OpenAI
def file_list():
    resp = openai.File.list()
    pprint(resp)

# Function to finetune a model
def finetune_model(fileid, suffix, model='davinci'):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    payload = {'training_file': fileid, 'model': model, 'suffix': suffix}
    resp = requests.request(method='POST', url='https://api.openai.com/v1/fine-tunes', json=payload, headers=header, timeout=45)
    pprint(resp.json())

# Function to list all finetuned models
def finetune_list():
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes', headers=header, timeout=45)
    pprint(resp.json())

# Function to get events for a finetuned model
def finetune_events(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s/events' % ftid, headers=header, timeout=45)    
    pprint(resp.json())

# Function to get details for a finetuned model
def finetune_get(ftid):
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % open_ai_api_key}
    resp = requests.request(method='GET', url='https://api.openai.com/v1/fine-tunes/%s' % ftid, headers=header, timeout=45)    
    pprint(resp.json())

# Get user input for model name
ft_model=input("Unesi ime modela: ")

# Upload file and finetune model
resp = file_upload('plots.jsonl')
finetune_model(resp['id'], ft_model, 'davinci')

# List all finetuned models
print(finetune_list())

# Get user input for finetuned model ID
# ft_id = input("Unesi ID finetune-a: ")

# Get events for finetuned model
# print(finetune_events(ft_id))

# Get details for finetuned model
# print(finetune_get(ft_id))