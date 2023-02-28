"""ログクラス."""


class AbstractLogger:
    """ログ抽象クラス."""

    def __init__(self) -> None:
        pass

    @property
    def length(self) -> int:
        """ログの長さ."""
        pass

    def add(self, log: str) -> None:
        """ログを追加する"""
        pass

    def clear(self) -> None:
        """ログをクリアする."""
        pass

    def __str__(self) -> str:
        pass


class ListLogger(AbstractLogger):
    """リスト管理ログクラス"""

    def __init__(self) -> None:
        self._logs = []

    @property
    def length(self) -> int:
        """(override)ログの長さ."""
        return len(self._logs)

    def add(self, log: str) -> None:
        """ログを追加する.

        :param log: ログ
        """
        self._logs.append(log)

    def clear(self) -> None:
        """ログをクリアする."""
        self._logs.clear()

    def __str__(self) -> str:
        log = ''
        for l in self._logs:
            log += f'{l}\n'
        return log


class NullLogger(AbstractLogger):
    """何もしないログクラス."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def length(self) -> int:
        return 0

    def add(self, log) -> None:
        return

    def clear(self) -> None:
        return

    def __str__(self) -> str:
        return ''
