import json

# Define the system message
sis_message = input(
    "Unesi sistemsku poruku napr. Miljan je ekspert za Digitalnu Transformaciju itd...: ")
system_message = {"role": "system", "content": sis_message}
izvor = input("Unesi izvorni fajl bez nastavka JSONL: ")

izv = f"{izvor}.JSONL"
questions = f"{izvor}_q.txt"
answers = f"{izvor}_a.txt"

# Read user and assistant contents from files
with open(questions, "r", encoding='utf-8') as user_file:
    user_contents = user_file.read().splitlines()

with open(answers, "r", encoding='utf-8') as assistant_file:
    assistant_contents = assistant_file.read().splitlines()


# Create the JSONL file
with open(izv, "w", encoding='utf-8') as jsonl_file:
    for user_content, assistant_content in zip(user_contents, assistant_contents):
        user_msg = {"role": "user", "content": user_content}
        assistant_msg = {"role": "assistant", "content": assistant_content}
        messages = [system_message, user_msg, assistant_msg]
        json.dump({"messages": messages}, jsonl_file, ensure_ascii=False)
        jsonl_file.write("\n")
