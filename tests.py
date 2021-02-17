import unittest
import sympy as sp

from economy import Economy, make_ellipsoid_ppf
from symbols import *

class TestEconomy(unittest.TestCase):
    def setUp(self):
        self.e = Economy(
            'Honolulu',
            'pv', 'wine',
            qy ** sp.Rational(1,2) * qx ** (sp.Rational(1,2)),
            make_ellipsoid_ppf(170,170),
            [0.2, 0.2, 0.2]
        )

    def test_rp_rq(self): 
        test = self.e.rp_implied_rq.subs({rp: self.e.rq_implied_rp})
        for v in [sp.Rational(4,5), sp.Rational(1, 1), sp.Rational(6,5)]:
            self.assertTrue(sp.Equality(test.subs({rq: v}), v))

if __name__ == '__main__': 
    unittest.main()