import json
import random
import time
import abilities
import heroes
import attributes
import answers_generator
from question_types import QuestionType


def main():
    print('Welcome to Théo\'s Dota 2 Quizz!\n\n')

    heroes_list = heroes.get_and_save_all_heroes()
    valve_abilities = abilities.get_and_save_all_abilities()
    all_abilities = abilities.valve_to_custom_format(valve_abilities)
    valid_abilities = abilities.get_valid_abilities(all_abilities)
    abilities.compress_constant_attributes(valid_abilities)

    destination_file = open('abilities_custom_format.json', 'w+')
    destination_file.write(json.dumps(valid_abilities, indent=4, sort_keys=True))

    test_all_questions(valid_abilities)
    # ask_random_questions(valid_abilities)


def ask_random_questions(valid_abilities):
    while True:
        question_type = random.choice(list(QuestionType.__members__.values()))
        attribute = attributes.get_corresponding_attribute(question_type)
        possible_abilities = abilities.get_abilities_with_attribute(valid_abilities, attribute)
        ability_answer = random.choice(possible_abilities)
        wrong_answers = attributes.generate_wrong_answers(possible_abilities, attribute, ability_answer)

        all_answers = wrong_answers.copy()
        correct_index = random.randint(0, 3)
        all_answers.insert(correct_index, ability_answer[attribute])

        print("Question about : " + attribute)
        print("ability is : " + ability_answer["name"])
        for index, answer in enumerate(all_answers):
            print("\t" + str(index + 1) + ") " + " ".join([str(value) for value in answer]))

        user_answer = -1
        while user_answer != correct_index:
            user_answer = int(input("Your answer : ")) - 1
            if user_answer != correct_index:
                print("Wrong!")
        print("\n\nCorrect! " + attribute + " for " + ability_answer["name"] + " is " +
              " ".join([str(round(value, 2)) for value in ability_answer[attribute]]) + "\n\n")
        time.sleep(1)


def test_all_questions(valid_abilities):
    invalid_combinations = []
    question_types = list(QuestionType.__members__.values())
    for question_type in question_types:
        valid_question_count = 0
        attribute = attributes.get_corresponding_attribute(question_type)
        possible_abilities = abilities.get_abilities_with_attribute(valid_abilities, attribute)
        debug_abilities = []
        for ability_answer in possible_abilities:
            try:
                answers_generator.generate_wrong_answers(possible_abilities, attribute, ability_answer)
                valid_question_count += 1
                debug_abilities.append(ability_answer["name"])
            except Exception as error:
                print(error)
                combination = dict()
                combination["AbilityName"] = ability_answer["name"]
                combination["AttributeName"] = attribute
                combination["AttributeValue"] = ability_answer[attribute]
                invalid_combinations.append(combination)
        print(str(question_type) + " has " + str(valid_question_count) + " valid questions")
        # print(debug_abilities)
    print(invalid_combinations)


if __name__ == '__main__':
    main()
