# The idea of this program if for me to feed it a .docx file with multiple choice test questions,
# for it to extract the main body of the question and the choices, scramble them and output a
# number (input request) of already formatted (for the already developed open cv test corrector)
# versions of tests.
import random
import re

import docx
import docx2txt

number_of_tests = int(input('How many versions do you want?'))

text = docx2txt.process('C:\\Users\\Guilherme\\Desktop\\test scrambler.docx', "/tmp/img_dir")

separate_full_questions = re.split('---', text)

answer_key = []
full_test = []
file_version = 1


def shuffle_and_separate_questions(full_text):
    for full_question in separate_full_questions:

        splitting = re.split('__', full_question)
        question_to_object = splitting.pop(0)
        random.shuffle(splitting)
        temp_question = Question(question_to_object, [])
        option_counter = 1
        for option in splitting:
            temp_choice = Choice('', False)
            if '*' in option:
                temp_choice.choice_text = option.replace('*', '')
                temp_choice.correct = True
                answer_key.append(option_counter)
            else:
                temp_choice.choice_text = option
                temp_choice.correct = False

            option_counter += 1

            temp_question.choices.append(temp_choice)

        full_test.append(temp_question.ret_list())


class Choice:
    def __init__(self, choice_text, correct):
        self.choice_text = choice_text
        self.correct = correct

    def ret_list(self):
        return self.choice_text

    def is_correct(self):
        return self.correct


class Question:
    def __init__(self, question_text, choices: list):
        self.question_text = question_text
        self.choices = choices

    def ret_list(self):
        reordered_question = [self.question_text]
        for index, i in enumerate(self.choices):
            reordered_question.append(i.ret_list())

        return reordered_question


for i in range(number_of_tests):
    shuffle_and_separate_questions(text)
    my_doc = docx.Document(f'Versão {number_of_tests}')

