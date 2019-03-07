import random
import abilities
import attributes
import theo_utils


def generate_wrong_answers(possible_abilities, attribute, ability_answer, allow_value_count_flip):
    wrong_answers = []
    tries = 0
    while len(wrong_answers) < 3:
        potential_answer = generate_wrong_answer(possible_abilities, attribute, ability_answer, allow_value_count_flip)
        if potential_answer in wrong_answers or ability_answer[attribute] == potential_answer:
            tries += 1
            if tries > 100:
                raise Exception(
                    "Can't generate answers for " + ability_answer["name"] + " " + attribute + " " + " ".join(
                        [str(value) for value in ability_answer[attribute]]))
            continue
        wrong_answers.append(potential_answer)
    return wrong_answers


def generate_wrong_answer(possible_abilities, attribute, ability_answer, allow_value_count_flip):
    value_source = random.choice(["generated"])
    # value_sources = random.choice(["from_other_ability", "generated"])
    # value_count = random.choice(["same", "different"])

    value = None
    if value_source == "generated":
        params = randomize_answer_parameters(allow_value_count_flip,
                                             attributes.attribute_allows_negative_upgrade(attribute))
        value = generate_similar_answer(ability_answer[attribute],
                                        params,
                                        abilities.is_ability_ultimate(ability_answer))
    return value


def generate_similar_answer(correct_answer, params, is_ultimate):
    # print("Generating from : " + correct_answer + " " + str(allow_negative_upgrade))

    all_values_multiple_of_5 = all([x % 5 == 0 and x >= 20 for x in correct_answer])
    # print("all_values_multiple_of_5 : " + str(all_values_multiple_of_5))
    if params["flip_multiple_of_5"]:
        all_values_multiple_of_5 = not all_values_multiple_of_5
        # print("Flip multiple of 5")

    all_values_integer = all([isinstance(value, int) or value.is_integer() and value > 1 for value in correct_answer])
    if params["flip_all_values_integer"]:
        all_values_integer = not all_values_integer
    if all_values_integer:
        random_function = theo_utils.randint_rounded
    else:
        random_function = theo_utils.randfloat

    generated_start_value = random_function(correct_answer[0] * 0.75, correct_answer[0] * 1.25)

    if all_values_multiple_of_5 and generated_start_value % 5 != 0:
        generated_start_value = round(generated_start_value / 5) * 5
    generated_answer = [generated_start_value]

    has_multiple_values = len(correct_answer) > 1
    # print("has_multiple_values : " + str(has_multiple_values))
    if params["flip_value_count"]:
        # print("Flip multiple values")
        has_multiple_values = not has_multiple_values

    target_value_count = len(correct_answer)
    if has_multiple_values and len(correct_answer) == 1:
        if is_ultimate:
            target_value_count = 3
        else:
            target_value_count = 4

    if has_multiple_values:
        if has_multiple_values and len(correct_answer) == 1:
            average_upgrade = random_function(-correct_answer[0] * 0.5, correct_answer[0] * 0.5)
            all_upgrade_equal = random.random() > 0.2
        else:
            upgrades = [correct_answer[i + 1] - correct_answer[i] for i in range(len(correct_answer) - 1)]
            average_upgrade = sum(upgrades) / len(upgrades)
            all_upgrade_equal = all([upgrade == average_upgrade for upgrade in upgrades])
            if params["flip_all_upgrade_equal"]:
                all_upgrade_equal = not all_upgrade_equal

        if all_upgrade_equal:
            lower_bound = round(average_upgrade * 0.75)
            if not params["allow_negative_upgrade"]:
                lower_bound = round(average_upgrade)
            bounds = [lower_bound, round(average_upgrade * 1.25)]
            generated_upgrade = random_function(min(bounds), max(bounds))

            if all_values_multiple_of_5:
                generated_upgrade = round(generated_upgrade / 5) * 5

            while len(generated_answer) < target_value_count:
                generated_answer.append(generated_answer[-1] + generated_upgrade)
        else:
            if not params["allow_negative_upgrade"]:
                upgrade_is_positive = True
            else:
                upgrade_is_positive = average_upgrade > 0
                if params["flip_upgrade_sign"]:
                    upgrade_is_positive = not upgrade_is_positive

            while len(generated_answer) < target_value_count:
                bounds = [round(average_upgrade * 0.75), round(average_upgrade * 1.25)]
                generated_upgrade = abs(random_function(min(bounds), max(bounds)))
                if not upgrade_is_positive:
                    generated_upgrade *= -1
                if all_values_multiple_of_5:
                    generated_upgrade = round(generated_upgrade / 5) * 5
                generated_answer.append(generated_answer[-1] + generated_upgrade)

    return generated_answer


def randomize_answer_parameters(allow_value_count_flip=True, allow_negative_upgrade=True):
    flip_multiple_of_5 = random.random() < 0.1
    flip_all_values_integer = random.random() < 0.1
    if allow_value_count_flip:
        flip_value_count = random.random() < 0.1
    else:
        flip_value_count = False
    flip_all_upgrade_equal = random.random() < 0.1
    flip_upgrade_sign = random.random() < 0.1
    allow_negative_upgrade = allow_negative_upgrade
    return build_manual_answer_parameters(flip_multiple_of_5=flip_multiple_of_5,
                                          flip_all_values_integer=flip_all_values_integer,
                                          flip_value_count=flip_value_count,
                                          flip_all_upgrade_equal=flip_all_upgrade_equal,
                                          allow_negative_upgrade=allow_negative_upgrade,
                                          flip_upgrade_sign=flip_upgrade_sign)


def build_manual_answer_parameters(flip_multiple_of_5, flip_all_values_integer, flip_value_count,
                                   flip_all_upgrade_equal, allow_negative_upgrade, flip_upgrade_sign):
    params = dict()
    params["flip_multiple_of_5"] = flip_multiple_of_5
    params["flip_all_values_integer"] = flip_all_values_integer
    params["flip_value_count"] = flip_value_count
    params["flip_all_upgrade_equal"] = flip_all_upgrade_equal
    params["flip_upgrade_sign"] = flip_upgrade_sign
    params["allow_negative_upgrade"] = allow_negative_upgrade
    return params
