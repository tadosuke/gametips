"""battlestatus モジュールの使用サンプル."""

from battlestatus.character import Character
from battlestatus.condition import ConditionId
from battlestatus.skill import SkillId
from battlestatus.weapon import Weapon, WeaponId


def main():
    """."""
    print('')
    print('[BattleStatus]')

    chara = Character(10)
    print(f'力={chara.atk}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    w = Weapon(WeaponId.COPPER_SWORD, 1)
    chara.equip(w)
    print(f'力={chara.atk}, 武器={w.id.name}(Lv.{w.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    w = Weapon(WeaponId.COPPER_SWORD, 5)
    chara.equip(w)
    print(f'力={chara.atk}, 武器={w.id.name}(Lv.{w.level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    chara.condition.add(ConditionId.ATK_UP)
    print(f'力={chara.atk}, 状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    chara.condition.add(ConditionId.ATK_DOWN)
    print(f'力={chara.atk}, 状態={ConditionId.ATK_DOWN.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    skill_level = 1
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    skill_level = 4
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, スキル={SkillId.ATK_UP.name}(Lv.{skill_level})')
    print(f'　→ 総攻撃力={chara.calc_atk()}')

    chara = Character(10)
    w = Weapon(WeaponId.STEEL_SWORD, 5)
    chara.equip(w)
    chara.condition.add(ConditionId.ATK_UP)
    skill_level = 5
    chara.skills.add(SkillId.ATK_UP, skill_level)
    print(f'力={chara.atk}, '
          f'武器={w.id.name}(Lv.{w.level}), '
          f'スキル={SkillId.ATK_UP.name}(Lv.{skill_level}), '
          f'状態={ConditionId.ATK_UP.name}')
    print(f'　→ 総攻撃力={chara.calc_atk()}')


if __name__ == '__main__':
    main()