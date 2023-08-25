import openai
import os
import time

openai.api_key = os.getenv("OPENAI_API_KEY")

input_file_path = input("Unesi puno ime fajla sa pitanjima: ")
output_file_path = input("Unesi puno ime fajla za odgovore:")
system_message = input("Unesi sistemsku poruku: ")
source_file_path = input("Unesi puno ime fajla sa izvorom: ")

with open(source_file_path, "r", encoding='utf-8') as source_file:
    prompt_source = source_file.read()


# Read questions from the input file
with open(input_file_path, "r", encoding='utf-8') as input_file:
    questions = input_file.read().splitlines()

# Initialize a list to store Q&A pairsinput.txt
qa_pairs = []

# Generate answers for each question
for question in questions:

    prompt = prompt_source + question

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.6,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message["content"].strip()
    qa_pairs.append((question, answer))
    print(f"Q: {question}\nA: {answer}\n")

# Save Q&A pairs to the output file
with open(output_file_path, "w", encoding='utf-8') as output_file:
    for question, answer in qa_pairs:
        output_file.write(f"Q: {question}\nA: {answer}\n")
