import openai
import csv
import sys
sys.path.insert(0, r'C:\Users\djordje\PythonGPT3Tutorial')
import my_functions


# Read OpenAI API key from file
openai.api_key = my_functions.open_file('openaiapikey.txt')

# Define a function to generate a question from a text prompt
def generate_question(prompt):
            response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0 )
 
            return response.choices[0].text
      

# Open the input CSV file
with open("input.csv", encoding="utf-8") as input_file:
    reader = csv.reader(input_file)

# Create a new CSV file for the questions
with open("input.csv", "r", newline="", encoding="utf-8") as input_file:
    reader = csv.reader(input_file)

    # Initialize a counter variable for the file suffix
    file_counter = 1

    # Loop through each row in the input CSV file
    for row in reader:
        # Loop through each cell in the row
        print(f'obradjujem red {row}')
        for cell in row:
            # Generate a question based on the cell contents
            question = generate_question(f'Summarize this text in a form of a question. Do it in the Serbian language:{cell}')

            # Write the question to a separate text file with a suffix based on the file_counter variable
            with open(f"prompts\pitanja_{file_counter}.txt", "w", encoding="utf-8") as output_file:
                output_file.write(question)

            # Increment the file_counter variable for the next iteration
                file_counter += 1

            print(question)

# writes each csv line in separate txt file must have the same name for matching in fine-tuning
file_counter = 1       

with open("input.csv", "r", newline="", encoding="utf-8") as input_file:
    reader = csv.reader(input_file)
    for row_number, row in enumerate(reader, start=1):
        for cell_number, cell in enumerate(row, start=1):
            with open(f"completions\pitanja_{file_counter}.txt", "w", encoding="utf-8") as output_file:
                output_file.write(cell)
                file_counter += 1
