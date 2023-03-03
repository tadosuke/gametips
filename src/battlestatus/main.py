"""battlestatus モジュールの使用サンプル."""

from enum import Enum, auto

from battlestatus.character import Character
from battlestatus.condition import ConditionId
from battlestatus.parameter import Parameter, ParameterId, ParameterValue
from battlestatus.skill import SkillId
from battlestatus.weapon import BaseParameter, BaseParameterDict, WeaponFactory


class WeaponId(Enum):
    """武器 ID."""

    COPPER_SWORD = auto()  # 銅の剣
    IRON_SWORD = auto()  # 鉄の剣
    STEEL_SWORD = auto()  # 鋼の剣


# 武器の能力辞書
_BASE_PARAMETER_DICT = {
    WeaponId.COPPER_SWORD:
        BaseParameter(name='銅の剣', atk=5),
    WeaponId.IRON_SWORD:
        BaseParameter(name='鉄の剣', atk=10),
    WeaponId.STEEL_SWORD:
        BaseParameter(name='鋼の剣', atk=15),
}
_param_dict = BaseParameterDict(_BASE_PARAMETER_DICT)
_factory = WeaponFactory(_param_dict)


def _create_default_character():
    param = Parameter()
    param.set(ParameterId.ATK, ParameterValue(10))
    c = Character(param)
    return c


def main():
    """."""
    print('')
    print('[BattleStatus]')

    chara = _create_default_character()
    print(f'力={chara.atk}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    w = _factory.create(WeaponId.COPPER_SWORD)
    chara.equip(w)
    print(f'力={chara.atk}, 武器={w.name}(Lv.{w.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    w = _factory.create(WeaponId.COPPER_SWORD, 5)
    chara.equip(w)
    print(f'力={chara.atk}, 武器={w.name}(Lv.{w.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    chara.condition.add(ConditionId.ATK_UP)
    print(f'力={chara.atk}, 状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    chara.condition.add(ConditionId.ATK_DOWN)
    print(f'力={chara.atk}, 状態={ConditionId.ATK_DOWN.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    skill_level = 1
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    skill_level = 4
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = _create_default_character()
    w = _factory.create(WeaponId.STEEL_SWORD, 5)
    chara.equip(w)
    chara.condition.add(ConditionId.ATK_UP)
    skill_level = 5
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, '
          f'武器={w.name}(Lv.{w.level}), '
          f'スキル={SkillId.ATK_UP.name}(Lv.{skill_level}), '
          f'状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')


if __name__ == '__main__':
    main()