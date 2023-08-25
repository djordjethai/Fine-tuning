# program izdvaja pitanja i odgovore iz jedneog txt fajla i razdvaja ih u dva fajla
# u zavisnosti ot vrste ulaznog fajla korigovati kod za duzinu i pocetni string
# u ovom slucaju je ulazni fajl input.txt koji ne sme da ima prazne linije

def split_qa(input_file, questions_file, answers_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    questions = []
    answers = []

    # pripremiti fajl tako da pitanja pocinju
    for line in lines:
        if line.startswith('Q: '):
            questions.append(line[3:])
        elif line.startswith('A: '):
            answers.append(line[3:])

    with open(questions_file, 'w', encoding='utf-8') as qf:
        for question in questions:
            qf.write(question)

    with open(answers_file, 'w', encoding='utf-8') as af:
        for answer in answers:
            af.write(answer)


# Execute the function
izvor = input("Unesi izvorni fajl bez nastavka txt: ")
izv = f"{izvor}.txt"
questions = f"{izvor}_q.txt"
answers = f"{izvor}_a.txt"
split_qa(izv, questions, answers)
