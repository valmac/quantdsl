import unittest

from quantdsl.application.with_multiprocessing_and_sqlalchemy import QuantDslApplicationWithMultiprocessingAndSQLAlchemy
from quantdsl.test_application_with_singlethread_and_pythonobjects import ApplicationTestCase


class TestQuantDslApplicationWithMultiprocessingAndSQLAlchemy(ApplicationTestCase):

    PATH_COUNT = 4000
    NUMBER_WORKERS = 4

    def setup_application(self):
        self.app = QuantDslApplicationWithMultiprocessingAndSQLAlchemy(
            num_workers=self.NUMBER_WORKERS,
            db_uri='sqlite:////Users/john/tmp-quantdsl2.db'
        )

    def test_generate_valuation_swing_option(self):
        specification = """
def Swing(start_date, end_date, underlying, quantity):
    if (quantity != 0) and (start_date < end_date):
        return Choice(
            Swing(start_date + TimeDelta('1d'), end_date, underlying, quantity-1) + Fixing(start_date, underlying),
            Swing(start_date + TimeDelta('1d'), end_date, underlying, quantity)
        )
    else:
        return 0

Swing(Date('2011-01-01'), Date('2011-01-05'), Market('NBP'), 3)
"""
        self.assert_contract_value(specification, 30.2051, expected_call_count=15)


if __name__ == '__main__':
    unittest.main()


