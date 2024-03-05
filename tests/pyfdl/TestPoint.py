
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from pyforcedirectedlayout.Point import Point


class TestPoint(UnitTestBase):
    """
    Auto generated by the one and only:
        Gato Malo – Humberto A. Sanchez II
        Generated: 11 February 2024
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testSubtraction(self):
        currentPoint: Point = Point(x=100, y=100)
        midPoint:     Point = Point(x=500, y=500)

        self.logger.info(f'{currentPoint} {midPoint}')

        currentPoint -= midPoint
        self.logger.info(f'After subtraction: {currentPoint}')

        self.assertEqual(Point(x=400, y=400), currentPoint, 'Did not adjust correctly')

    def testSubtractionNegativePoint(self):
        currentPoint: Point = Point(x=-100, y=-100)
        midPoint:     Point = Point(x=500, y=500)

        self.logger.info(f'{currentPoint} {midPoint}')

        currentPoint -= midPoint
        self.logger.info(f'After subtraction: {currentPoint}')

        self.assertEqual(Point(x=600, y=600), currentPoint, 'Did not adjust correctly')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestPoint))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
