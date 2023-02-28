"""turnbattle.main モジュールのテスト."""

import unittest
from unittest import mock

import turnbattle.main
from turnbattle.main import Character, Action, Battle, Turn
from turnbattle.logger import ListLogger, NullLogger


class TestCharacter(unittest.TestCase):
	
	def test_init(self):
		c = Character(100, 20, 16, 'Hoge')
		self.assertEqual(100, c.hp)
		self.assertEqual(20, c._atk)
		self.assertEqual(16, c._def)
		self.assertEqual('Hoge', c.name)
	
	def test_attack(self):
		c1 = Character(atk=20)
		c2 = Character()
		with mock.patch.object(c2, 'damage', return_value=20) as mp_dmg:
			point = c1.attack(c2)
			self.assertEqual(20, point)
			mp_dmg.assert_called_once_with(20)
	
	def test_damage(self):
		c = Character(100, 20, 16)
		point = c.damage(20)
		self.assertEqual(12, point)
		self.assertEqual(88, c.hp)
		
		c = Character(100, 20, 16)
		point = c.damage(8)
		self.assertEqual(0, point)
		self.assertEqual(100, c.hp)
		
		c = Character(100, 20, 16)
		point = c.damage(4)
		self.assertEqual(0, point)
		self.assertEqual(100, c.hp)
		
		c = Character(100, 20, 16)
		point = c.damage(200)
		self.assertEqual(192, point)
		self.assertTrue(c.is_dead())
		
	def test_select_target(self):
		c1 = Character()
		c2 = Character()
		c3 = Character()
		targets = (c2, c3)
		self.assertEqual(c2, c1.select_target(targets))
	
		
class TestAction(unittest.TestCase):
	
	def test_case(self):
		c1 = Character()
		c2 = Character()
		act = Action(c1, c2)
		
		with mock.patch.object(c1, 'attack') as mp_atk:
			act.exec()
			mp_atk.assert_called_once_with(c2)
			
		c1 = Character(hp=0)
		c2 = Character()
		act = Action(c1, c2)
		with mock.patch.object(c1, 'attack') as mp_atk:
			act.exec()
			mp_atk.assert_not_called()
			
												
class TestTurn(unittest.TestCase):
	
	def test_case(self):
		c1 = Character()
		c2 = Character()
		
		turn = Turn({c1, c2})
		self.assertEqual(2, len(turn._actions))
		
		with mock.patch('turnbattle.Action.exec') as mp_act_exe:
			turn.exec()
			mp_act_exe.assert_called()
			
	def test_dead(self):
		c1 = Character(100, 50, 50)
		c2 = Character(10, 10, 10)
		turn = Turn({c1, c2})
		survivor = turn.exec()
		self.assertEqual(1, len(survivor))
	
													
class TestBattle(unittest.TestCase):
	
	def setUp(self):
		turnbattle.main.log = ListLogger()
		
	def tearDown(self):
		turnbattle.main.log = NullLogger()
	
	def test_two(self):
		c1 = Character(50, 20, 20, 'Hoge')
		c2 = Character(30, 16, 16, 'Piyo')
		characters = (c1, c2)
		battle = Battle(characters)
		self.assertEqual(1, battle._turn_num)
		self.assertEqual(2, len(battle._characters))
		winner = battle.exec()
		self.assertEqual(c1, winner)
		
		c1 = Character(30, 15, 15, 'Hoge')
		c2 = Character(60, 20, 20, 'Piyo')
		characters = (c1, c2)	
		battle = Battle(characters)
		winner = battle.exec()
		self.assertEqual(c2, winner)
		
	def test_three(self):
		c1 = Character(50, 20, 20, 'Hoge')
		c2 = Character(30, 16, 16, 'Piyo')
		c3 = Character(200, 30, 30, 'Fuga')
		characters = (c1, c2, c3)
		battle = Battle(characters)
		self.assertEqual(3, len(battle._characters))
		winner = battle.exec()
		self.assertEqual(c3, winner)
		
		
if __name__ == '__main__':
	unittest.main()
