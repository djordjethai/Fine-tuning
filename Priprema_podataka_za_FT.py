import json
import openai
import streamlit as st
from myfunc.mojafunkcija import open_file, init_cond_llm

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 400px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def pripremaft():
    with st.sidebar:
        model, temp = init_cond_llm()
    
    final_placeholder = st.empty()
    placeholder = st.empty()

    with placeholder.container():
        input_file_path = st.file_uploader(
            "Izaberite fajl sa pitanjima", key="upload_pitanja", type='txt', help="Pitanja koja ste sastavili u prethodnom koraku.")

        source_file_path = st.file_uploader(
            "Izaberite fajl sa izvorom (ako postoji)", key="upload_izvor", type='txt', help="Fajl koje želite da vam bude izvor informacija za odgovore.")

        if input_file_path is not None:
            # Loading text from the file
            pitanje = open_file(input_file_path.name)

        if source_file_path is not None:
            # Loading text from the file
            prompt_source = open_file(source_file_path.name)
        else:
            prompt_source = ""
        with st.form(key='my_form'):
            system_message = st.text_area(
                "Unesite sistemsku poruku: ", help="Opišite ponašanje i stil modela. Uključite i ime")
            izvor = st.text_input("Unesite naziv FT modela:",
                                help="Dajte ime modelu koji kreirate")
            output_file_path = f"{izvor}_odg.txt"
            submit_button = st.form_submit_button(label='Submit')


   
    
    if submit_button:
        with st.spinner('Kreiram odgovore...'):

            # source_file_path za odgovore koji se baziraju na specificnom tekstu, obuhvata prefirx kao "Based on this text",
            # zatim sam text i na kraju sufix kao "Answer this question in your writing style:"
            # ako nije potrebno ucitava se empty.txt

            # Read questions from the input file
            qa_answers = []
            questions = pitanje.splitlines()
            total_questions = len(questions)
            # Generate answers for each question, model and temp can be adjusted
            # Iterate through questions with index
            for idx, question in enumerate(questions, 1):
                current_question_number = idx  # Get the current question number

                prompt = prompt_source + question

                response = openai.ChatCompletion.create(
                    model=model,
                    temperature=temp,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ]
                )

                answer = response.choices[0].message["content"].strip().replace(
                    '\n', '')

                qa_answers.append(answer)

                with placeholder.container():
                    st.subheader(
                        f"Obrađujem {current_question_number}. od ukupno {total_questions} pitanja")
                    st.info(f"Pitanje: {question}")
                    st.success(f"Odgovor: {answer}")
            # Save only answer to the output file

            with open(output_file_path, "w", encoding='utf-8') as output_file:
                for answer in qa_answers:
                    output_file.write(f"{answer}\n")
            placeholder.empty()

            with final_placeholder.container():
                st.subheader(f"Kreiran je fajl {output_file_path}")
                izv = f"{izvor}.JSONL"
                # promeniti u string
                # Read user and assistant contents from files
                with open(input_file_path.name, "r", encoding='utf-8') as user_file:
                    user_contents = user_file.read().splitlines()

                with open(output_file_path, "r", encoding='utf-8') as assistant_file:
                    assistant_contents = assistant_file.read().splitlines()

                # promeniti u string
                # Create the JSONL file
                with open(izv, "w", encoding='utf-8') as jsonl_file:
                    for user_content, assistant_content in zip(user_contents, assistant_contents):
                        user_msg = {"role": "user",
                                    "content": user_content}
                        assistant_msg = {"role": "assistant",
                                        "content": assistant_content}
                        messages = [system_message,
                                    user_msg, assistant_msg]
                        json.dump({"messages": messages},
                                jsonl_file, ensure_ascii=False)
                        jsonl_file.write("\n")

                st.subheader(
                    f"Obrada je završena, kreiran je fajl {jsonl_file.name}")




