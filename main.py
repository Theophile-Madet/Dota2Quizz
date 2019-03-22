import json
import random
import time
import abilities
import heroes
import attributes
import answers_generator
import numpy
from question_types import QuestionType


def main():
    print('Welcome to Théo\'s Dota 2 Quizz!\n\n')

    all_heroes = heroes.get_and_save_all_heroes()
    valve_abilities = abilities.get_and_save_all_abilities()
    all_abilities = abilities.valve_to_custom_format(valve_abilities)
    valid_abilities = abilities.get_valid_abilities(all_abilities)
    abilities.compress_constant_attributes(valid_abilities)

    destination_file = open('abilities_custom_format.json', 'w+')
    destination_file.write(json.dumps(valid_abilities, indent=4, sort_keys=True))

    # test_all_questions(valid_abilities, all_heroes)
    ask_random_questions(valid_abilities, all_heroes)


def ask_random_questions(valid_abilities, all_heroes):
    while True:
        question_type = random.choice(list(QuestionType.__members__.values()))
        question_type = QuestionType.HERO_ATTACK_DAMAGE_LVL1

        if is_ability_question(question_type):
            attribute = attributes.get_corresponding_attribute(question_type)
            possible_answers = abilities.get_abilities_with_attribute(valid_abilities, attribute)
            ability_answer = random.choice(possible_answers)
        elif is_hero_question(question_type):
            attribute = heroes.get_corresponding_attribute(question_type)
            possible_answers = [hero for hero in all_heroes.values()]
            if question_type == QuestionType.HERO_PROJECTILE_SPEED:
                possible_answers = [hero for hero in all_heroes.values() if
                                    hero["AttackCapabilities"][0] == "DOTA_UNIT_CAP_RANGED_ATTACK"]
            ability_answer = random.choice(possible_answers)

        wrong_answers = answers_generator.generate_wrong_answers(possible_answers, attribute, ability_answer)
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
              " ".join([str(round(value, 2)) for value in ability_answer[attribute]]))

        print_stats_if_appropriate(possible_answers, attribute, ability_answer[attribute])

        print("\n\n")
        time.sleep(1)


def test_all_questions(valid_abilities, all_heroes):
    invalid_combinations = []
    question_types = list(QuestionType.__members__.values())
    for question_type in question_types:
        valid_question_count = 0

        if is_ability_question(question_type):
            attribute = attributes.get_corresponding_attribute(question_type)
            possible_answers = abilities.get_abilities_with_attribute(valid_abilities, attribute)
        elif is_hero_question(question_type):
            attribute = heroes.get_corresponding_attribute(question_type)
            possible_answers = [hero for hero in all_heroes.values()]
            if question_type == QuestionType.HERO_PROJECTILE_SPEED:
                possible_answers = [hero for hero in all_heroes.values() if
                                    hero["AttackCapabilities"][0] == "DOTA_UNIT_CAP_RANGED_ATTACK"]

        debug_abilities = []
        for possible_answer in possible_answers:
            try:
                answers_generator.generate_wrong_answers(possible_answers, attribute, possible_answer)
                valid_question_count += 1
                debug_abilities.append(possible_answer["name"])
            except Exception as error:
                print(error)
                combination = dict()
                combination["AbilityName"] = possible_answer["name"]
                combination["AttributeName"] = attribute
                combination["AttributeValue"] = possible_answer[attribute]
                invalid_combinations.append(combination)
        print(str(question_type) + " has " + str(valid_question_count) + " valid questions")
        # print(debug_abilities)
    print(invalid_combinations)


def is_ability_question(question_type):
    ability_question_types = [QuestionType.ABILITY_MANA_COST, QuestionType.ABILITY_DAMAGE,
                              QuestionType.ABILITY_CAST_POINT, QuestionType.ABILITY_COOLDOWN,
                              QuestionType.ABILITY_RANGE]
    return question_type in ability_question_types


def is_hero_question(question_type):
    hero_question_types = [QuestionType.HERO_STARTING_STATS, QuestionType.HERO_STAT_GAIN, QuestionType.HERO_TURN_RATE,
                           QuestionType.HERO_ATTACK_RANGE, QuestionType.HERO_VISION_RANGE,
                           QuestionType.HERO_PROJECTILE_SPEED, QuestionType.HERO_HP_LVL1, QuestionType.HERO_MANA_LVL1,
                           QuestionType.HERO_ARMOR_LVL1, QuestionType.HERO_HP_REGEN_LVL1,
                           QuestionType.HERO_MANA_REGEN_LVL1, QuestionType.HERO_MAGIC_RES_LVL1,
                           QuestionType.HERO_ATTACK_DAMAGE_LVL1]
    return question_type in hero_question_types


def print_stats_if_appropriate(possible_answers, attribute, answer):
    values = [x[attribute] for x in possible_answers]
    if not all(len(value) == 1 for value in values):
        return

    values = [value[0] for value in values]

    print("\tAverage : " + str(round(numpy.mean(values), 2)))
    print("\tMedian : " + str(numpy.median(values)))
    print("\tMinimum : " + str(numpy.min(values)))
    print("\tMaximum : " + str(numpy.max(values)))
    rank = len([value for value in values if value > answer[0]]) + 1
    print("\tRanked " + str(rank) + " out of " + str(len(values)))


if __name__ == '__main__':
    main()
