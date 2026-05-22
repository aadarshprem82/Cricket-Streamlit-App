import unittest
import pandas as pd

from utils.calculations import (
    calculate_run_rate,
    calculate_total_runs
)

from utils.helpers import (
    format_overs,
    overs_to_balls
)

# ==========================================
# TEST SCORING
# ==========================================

class TestScoringFunctions(
    unittest.TestCase
):

    # ======================================
    # RUN RATE
    # ======================================

    def test_run_rate(self):

        rr = calculate_run_rate(
            runs=60,
            legal_balls=36
        )

        self.assertEqual(
            rr,
            10.0
        )

    # ======================================
    # TOTAL RUNS
    # ======================================

    def test_total_runs(self):

        df = pd.DataFrame({

            "total_runs": [

                1, 4, 6, 2, 0
            ]
        })

        total = calculate_total_runs(
            df
        )

        self.assertEqual(
            total,
            13
        )

    # ======================================
    # FORMAT OVERS
    # ======================================

    def test_format_overs(self):

        overs = format_overs(17)

        self.assertEqual(
            overs,
            "2.5"
        )

    # ======================================
    # OVERS TO BALLS
    # ======================================

    def test_overs_to_balls(self):

        balls = overs_to_balls(
            "4.3"
        )

        self.assertEqual(
            balls,
            27
        )

    # ======================================
    # ZERO BALL RUN RATE
    # ======================================

    def test_zero_ball_run_rate(self):

        rr = calculate_run_rate(
            runs=0,
            legal_balls=0
        )

        self.assertEqual(
            rr,
            0
        )

    # ======================================
    # EMPTY TOTAL RUNS
    # ======================================

    def test_empty_total_runs(self):

        df = pd.DataFrame()

        total = calculate_total_runs(
            df
        )

        self.assertEqual(
            total,
            0
        )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    unittest.main()