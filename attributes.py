from question_types import QuestionType


def attribute_allows_negative_upgrade(attribute):
    forbid_list = ["AbilityDamage"]
    if attribute in forbid_list:
        return False
    else:
        return True


def attribute_allows_flip_multiple_of_5(attribute):
    forbid_list = ["Custom_HpLvl1", "ItemCost"]
    if attribute in forbid_list:
        return False
    else:
        return True


def attribute_allows_value_count_flip(attribute):
    forbid_list = ["Custom_HpLvl1", "Custom_ManaLvl1", "Custom_ArmorLvl1", "ProjectileSpeed", "VisionDaytimeRange",
                   "VisionNighttimeRange", "AttackRange", "MovementTurnRate", "AttributeStrengthGain",
                   "AttributeAgilityGain", "AttributeIntelligenceGain", "AttributeBaseStrength", "AttributeBaseAgility",
                   "AttributeBaseIntelligence", "Custom_HpRegenLvl1", "Custom_ManaRegenLvl1",
                   "Custom_MagicResistanceLvl1", "Custom_AttackDamageLvl1", "ItemCost"]
    if attribute in forbid_list:
        return False
    else:
        return True


def get_corresponding_attribute(question_type):
    if question_type == QuestionType.ABILITY_DAMAGE:
        return "AbilityDamage"
    if question_type == QuestionType.ABILITY_MANA_COST:
        return "AbilityManaCost"
    if question_type == QuestionType.ABILITY_COOLDOWN:
        return "AbilityCooldown"
    if question_type == QuestionType.ABILITY_CAST_POINT:
        return "AbilityCastPoint"
    if question_type == QuestionType.ABILITY_RANGE:
        return "AbilityCastRange"


def get_valid_attributes(abilities):
    valid_attributes = []

    exclude_list = ["ID", "AbilitySound", "HasScepterUpgrade", "FightRecapLevel", "MaxLevel", "IsGrantedByScepter",
                    "AbilityDraftPreAbility", "HotKeyOverride", "DisplayAdditionalHeroes", "AbilityTextureName",
                    "precache", "Modelscale", "AbilitySharedCooldown", "AbilityChannelAnimation",
                    "AbilityUnitTargetTeam", "AbilityCastAnimation", "AbilityType", "RequiredLevel",
                    "AbilityCastGestureSlot", "AbilitySpecial", "OnCastbar", "LinkedAbility", "OnLearnbar",
                    "AbilityBehavior"]
    exclude_substring = []

    for ability_name in abilities:
        for attribute_name in abilities[ability_name]:
            if attribute_name in valid_attributes:
                continue
            if attribute_name in exclude_list:
                continue
            excluded = False
            for substring in exclude_substring:
                if substring in ability_name:
                    excluded = True
                    break
            if excluded:
                continue
            valid_attributes.append(attribute_name)

    return valid_attributes
