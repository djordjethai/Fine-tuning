import json
import openai
import os
import streamlit as st
from mojafunkcja import open_file, st_style, init_cond_llm, positive_login

st.set_page_config(
    page_title="Fine Tuning",
    page_icon="👋",
    layout="wide"
)
st_style()

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


def main():
    st.subheader('Fine Tuning')  # Setting the title for Streamlit application
    st.info(
        'Aplikacija priprema Fine Tuning podatke za GPT-3.5 Turbo model. Za vise informacija pogledajte dokumentaciju.')
    st.caption("Prvi korak je kreiranje pitanja. To smo radili pomocu besplatnog CHATGPT modela. Iz svake oblasti (ili iz dokumenta) zamolimo CHATGPT da kreira relevantna pitanja. Drugi korak je bio da u fajlu input.txt rucno odgovorimo na sva pitanja. ili da se odgovori izvuku iz dokumenta. Trece faza je da se dodatni odgovori kreiraju u ovom programu.")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    model, temp = init_cond_llm()
    with st.sidebar:
        input_file_path = st.file_uploader(
            "Izaberite fajl sa pitanjima", key="upload_pitanja", type='txt')

        source_file_path = st.file_uploader(
            "Izaberite fajl sa izvorom (ako postoji)", key="upload_izvor", type='txt')

        if input_file_path is not None:
            # Loading text from the file
            pitanje = open_file(input_file_path.name)
        if source_file_path is not None:
            # Loading text from the file
            prompt_source = open_file(source_file_path.name)
        else:
            prompt_source = ""

    col1, col2 = st.columns(2)
    with col1:
        with st.form(key='my_form'):
            system_message = st.text_area("Unesite sistemsku poruku: ")
            izvor = st.text_input("Unesite naziv FT modela:")
            output_file_path = st.text_input(
                "Unesite puno ime fajla za odgovore:")
            submit_button = st.form_submit_button(label='Submit')

    with col2:
        final_placeholder = st.empty()
        placeholder = st.empty()
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
                            f"Obradjujem {current_question_number}. od ukupno {total_questions} pitanja")
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

                    # Read user and assistant contents from files
                    with open(input_file_path.name, "r", encoding='utf-8') as user_file:
                        user_contents = user_file.read().splitlines()

                    with open(output_file_path, "r", encoding='utf-8') as assistant_file:
                        assistant_contents = assistant_file.read().splitlines()

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
                        f"Obrada je zavrsena, kreiran je fajl {jsonl_file.name}")


name, authentication_status, username = positive_login(main, "03.09.23")