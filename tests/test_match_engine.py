import unittest

from utils.result_engine import (
    get_match_result
)

from utils.helpers import (
    result_text
)

# ==========================================
# TEST MATCH ENGINE
# ==========================================

class TestMatchEngine(
    unittest.TestCase
):

    # ======================================
    # TEAM1 WIN
    # ======================================

    def test_team1_win(self):

        result = get_match_result(

            first_innings_score=180,

            second_innings_score=150,

            wickets_left=2,

            balls_remaining=0,

            batting_second_team="Titans",

            bowling_first_team="Warriors"
        )

        self.assertEqual(

            result["winner"],

            "Warriors"
        )

    # ======================================
    # TEAM2 WIN
    # ======================================

    def test_team2_win(self):

        result = get_match_result(

            first_innings_score=145,

            second_innings_score=146,

            wickets_left=5,

            balls_remaining=12,

            batting_second_team="Titans",

            bowling_first_team="Warriors"
        )

        self.assertEqual(

            result["winner"],

            "Titans"
        )

    # ======================================
    # TIE
    # ======================================

    def test_match_tie(self):

        result = get_match_result(

            first_innings_score=160,

            second_innings_score=160,

            wickets_left=0,

            balls_remaining=0,

            batting_second_team="Titans",

            bowling_first_team="Warriors"
        )

        self.assertEqual(

            result["result"],

            "Match Tied"
        )

    # ======================================
    # RESULT TEXT RUNS
    # ======================================

    def test_result_text_runs(self):

        text = result_text(

            winner="Warriors",

            margin=25,

            result_type="runs"
        )

        self.assertEqual(

            text,

            "Warriors won by 25 runs"
        )

    # ======================================
    # RESULT TEXT WICKETS
    # ======================================

    def test_result_text_wickets(self):

        text = result_text(

            winner="Titans",

            margin=5,

            result_type="wickets"
        )

        self.assertEqual(

            text,

            "Titans won by 5 wickets"
        )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    unittest.main()