"""ドラクエ風ターンバトルシステム."""
from __future__ import annotations

import typing as tp
from collections.abc import Collection

import logger

log = logger.NullLogger()


class Character:
    """キャラクター.

    :param hp: 初期 HP
    :param atk: 攻撃力
    :param def_: 防御力
    :param name: 名前
    """

    _DEFAULT_HP = 100
    _DEFAULT_ATK = 20
    _DEFAULT_DEF = 20
    _DEFAULT_NAME = 'name'

    def __init__(
            self,
            hp=_DEFAULT_HP,
            atk=_DEFAULT_ATK,
            def_=_DEFAULT_DEF,
            name=_DEFAULT_NAME) -> None:
        self._hp = hp
        self._atk = atk
        self._def = def_
        self._name = name

    @property
    def hp(self) -> int:
        """HP."""
        return self._hp

    @property
    def name(self) -> str:
        """名前."""
        return self._name

    def is_dead(self) -> bool:
        """死亡しているか？"""
        return self.hp <= 0

    def attack(self, target: Character) -> int:
        """攻撃する.

        :param target: 攻撃相手
        :return: 与えたダメージ
        """
        point = target.damage(self._atk)
        return point

    def damage(self, atk) -> int:
        """ダメージを受ける.

        :param atk: 攻撃力
        :return: 受けたダメージ
        """
        point = max(int(atk - self._def / 2), 0)
        self._hp = max(self._hp - point, 0)
        return point

    def select_target(self, targets: Collection[Character]) -> tp.Optional[Character]:
        """攻撃相手を選ぶ.

        :param targets: 候補
        :return: 選ばれたキャラクター
        """
        if len(targets) == 0:
            return None
        return list(targets)[0]


class Action:
    """行動.

    :param actor: 行動者
    :param target: ターゲット
    """

    def __init__(self, actor: Character, target: Character) -> None:
        self._actor = actor
        self._target = target

    def exec(self) -> None:
        """アクションを実行する."""
        actor = self._actor
        target = self._target

        if actor.is_dead():
            return

        log.add(f'{actor.name}の攻撃！')
        point = actor.attack(target)
        log.add(f' {target.name} に {point} のダメージ！(残りHP: {target.hp})')

        if target.is_dead():
            log.add(f'  {target.name} は倒れた。')


class Turn:
    """ターン.

    :param characters: ターン参加者
    """

    def __init__(self, characters: Collection[Character]) -> None:
        self._characters = characters
        self._actions = self._create_actions()

    def _create_actions(self) -> list[Action]:
        """アクションを生成する.

        :return: 生成したアクションのリスト
        """
        actions = []
        for actor in self._characters:
            targets = set(self._characters) - {actor}  # 自分以外
            target = actor.select_target(targets)
            action = Action(actor, target)
            actions.append(action)
        return actions

    def exec(self) -> list[Character]:
        """ターンを実行する.

        :return: 生き残っているキャラクターのリスト
        """
        for a in self._actions:
            a.exec()
        self._update_dead()
        return list(self._characters)

    def _update_dead(self) -> None:
        """キャラクターたちの死亡状態を更新する."""
        self._characters = {c for c in self._characters if not c.is_dead()}


class Battle:
    """戦闘.

    :param characters: 戦闘参加者
    """

    def __init__(self, characters: Collection[Character]) -> None:
        assert 0 < len(characters)
        self._characters = characters
        self._turn_num = 1

        self._log_appear()

    def _log_appear(self) -> None:
        """戦闘開始時のログを出す."""
        log.add('【Battle Start】')
        for c in self._characters:
            log.add(f'{c.name} があらわれた！')

    def exec(self) -> Character:
        """戦闘を実行する.

        :return: 勝者
        """
        while 1 < len(self._characters):
            log.add(f'■ {self._turn_num} ターン')
            turn = Turn(self._characters)
            self._characters = turn.exec()
            self._turn_num += 1
        winner = self._characters[0]
        log.add(f'--{winner.name} の勝ち--')

        print(log)
        log.clear()

        return winner
