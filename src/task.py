"""シンプルなタスクシステム.

同期実行のため、実行タイミングが明確でデバッグがしやすいのが特長です.
"""
from __future__ import annotations


class TaskBase:
	"""タスクの基底クラス."""
	
	def __init__(self, parent: TaskBase = None) -> None:
		self._children: list[TaskBase] = []

		if parent is not None:
			parent.add_child(self)

	def has_child(self) -> bool:
		"""子タスクを持っているか？"""

		return 0 < len(self._children)

	def update(self, delta_sec: float) -> None:
		"""更新.

		:param 前回更新からの経過時間（秒）
		"""

		self._update(delta_sec)

		for child in self._children:
			child.update(delta_sec)

	def _update(self, delta_sec: float) -> None:
		"""自分の更新."""

		pass

	def add_child(self, child: TaskBase) -> None:
		"""子タスクを追加する."""

		assert child not in self._children
		self._children.append(child)
