"""タスクシステムモジュールのテスト."""

import unittest
from task import TaskBase


# 実行順を確認するための変数
_order = ''


class TaskA(TaskBase):

	def _update(self, delta_sec: float) -> None:
		global _order
		_order += 'a'


class TaskB(TaskBase):

	def _update(self, delta_sec: float) -> None:
		global _order
		_order += 'b'


class TaskC(TaskBase):

	def _update(self, delta_sec: float) -> None:
		global _order
		_order += 'c'


class TaskD(TaskBase):

	def _update(self, delta_sec: float) -> None:
		global _order
		_order += 'd'


class TestTask(unittest.TestCase):

	def test_init(self):
		a = TaskA()
		self.assertFalse(a.has_child())

	def test_add_child(self):
		a = TaskA()
		b = TaskB(a)
		self.assertTrue(a.has_child())
		self.assertFalse(b.has_child())

		c = TaskC(b)
		self.assertTrue(b.has_child())
		self.assertFalse(c.has_child())

	def test_update(self):
		global _order
		_order = ''

		# a
		# -b
		# --d
		# -c
		a = TaskA()
		b = TaskB(a)
		c = TaskC(a)
		d = TaskD(b)
		a.update(0)
		self.assertEqual('abdc', _order)


if __name__ == '__main__':
	unittest.main()
