"""logger モジュールのテスト."""

import unittest

from logger import Logger, NullLogger


class TestLogger(unittest.TestCase):
	
	def test_case(self):
		logger = Logger()
		self.assertEqual(0, logger.length)
		logger.add('log1')
		self.assertEqual(1, logger.length)
		logger.add('log2')
		self.assertEqual(2, logger.length)
		log = str(logger)
		self.assertTrue(log)
		logger.clear()
		self.assertEqual(0, logger.length)

		
class TestNullLogger(unittest.TestCase):
	
	def test_case(self):
		logger = NullLogger()
		self.assertEqual(0, logger.length)
		logger.add('log1')
		self.assertEqual(0, logger.length)
		log = str(logger)
		self.assertFalse(log)
		logger.clear()
		self.assertEqual(0, logger.length)
		
		
if __name__ == '__main__':
	unittest.main()
