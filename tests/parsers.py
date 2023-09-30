import unittest

from core.parsers import parse_condition


class TestConditionParser(unittest.TestCase):
	def test_output(self):
		self.assertError(parse_condition(r'[lala| hahha]->[after|good job]'))

	def assertError(self, expr, msg=None):
		try:
			self.assertTrue(expr, msg)
		except:
			self.failureException(msg)
