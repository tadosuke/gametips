"""battlestatus モジュールの使用サンプル."""

from battlestatus.character import Character
from battlestatus.condition import ConditionId
from battlestatus.equipment import ItemName, Equipment, BaseData
from battlestatus.parameters import Parameters, ParameterId, ParameterValue
from battlestatus.skill import SkillId


def _create_copper_sword() -> Equipment:
    params = Parameters()
    params.set(ParameterId.ATK, ParameterValue(5))
    base_data = BaseData(
        name=ItemName('銅の剣'),
        params=params)
    eq = Equipment(base_data)
    return eq


def _create_steel_sword() -> Equipment:
    params = Parameters()
    params.set(ParameterId.ATK, ParameterValue(20))
    base_data = BaseData(
        name=ItemName('鋼の剣'),
        params=params)
    eq = Equipment(base_data)
    return eq


def _create_default_character():
    param = Parameters()
    param.set(ParameterId.ATK, ParameterValue(10))
    c = Character(param)
    return c


def main():
    """."""
    print('')
    print('[BattleStatus]')

    chara = _create_default_character()
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    eq = _create_copper_sword()
    chara.equipments.set(eq)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, 武器={eq.name}(Lv.{eq.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    eq = _create_copper_sword()
    eq.set_level(3)
    chara.equipments.set(eq)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, 武器={eq.name}(Lv.{eq.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    chara.condition.add(ConditionId.ATK_UP)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, 状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    chara.condition.add(ConditionId.ATK_DOWN)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, 状態={ConditionId.ATK_DOWN.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    skill_level = 1
    chara.skills.add(SkillId.ATK_UP, skill_level)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    skill_level = 4
    chara.skills.add(SkillId.ATK_UP, skill_level)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    eq = _create_steel_sword()
    eq.set_level(10)
    chara.equipments.set(eq)
    chara.condition.add(ConditionId.ATK_UP)
    skill_level = 5
    chara.skills.add(SkillId.ATK_UP, skill_level)
    atk = chara.params.get(ParameterId.ATK).value
    print(f'力={atk}, '
          f'武器={eq.name}(Lv.{eq.level}), '
          f'スキル={SkillId.ATK_UP.name}(Lv.{skill_level}), '
          f'状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')


if __name__ == '__main__':
    main()
