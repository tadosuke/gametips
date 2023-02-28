"""タスクシステムモジュールのテスト."""

import unittest
from unittest import mock

from task.task import TaskBase


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
		self.assertFalse(a.is_exit())

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

	def test_add_child(self):
		a = TaskA()
		b = TaskB(a)
		self.assertTrue(a.has_child())
		self.assertFalse(b.has_child())

		c = TaskC(b)
		self.assertTrue(b.has_child())
		self.assertFalse(c.has_child())

	def test_exit(self):
		a = TaskA()

		with mock.patch.object(a, '_update') as mp_update:
			a.update(0)
			mp_update.assert_called_once_with(0)

		a.exit()
		self.assertTrue(a.is_exit())

		# 終了後の update は実行されない
		with mock.patch.object(a, '_update') as mp_update:
			a.update(0)
			mp_update.assert_not_called()

	def test_apply_exit_children(self):
		a = TaskA()
		b = TaskB(a)
		c = TaskC(a)

		# 終了している b を削除。c がまだ残っている
		b.exit()
		a._apply_exit_children()
		self.assertTrue(a.has_child())

		# c も終了したので削除。子タスクはいなくなる
		c.exit()
		a._apply_exit_children()
		self.assertFalse(a.has_child())


if __name__ == '__main__':
	unittest.main()
