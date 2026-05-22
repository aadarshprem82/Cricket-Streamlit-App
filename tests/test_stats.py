import unittest
import pandas as pd

from utils.player_stats import (
    batting_career_stats,
    bowling_career_stats
)

from utils.team_stats import (
    highest_team_score,
    lowest_team_score
)

# ==========================================
# TEST STATS
# ==========================================

class TestStats(
    unittest.TestCase
):

    # ======================================
    # SAMPLE BALL DATA
    # ======================================

    def sample_ball_df(self):

        data = [

            {

                "match_id": "M1",

                "striker": "Virat",

                "non_striker": "Rohit",

                "bowler": "Bumrah",

                "runs_off_bat": 4,

                "total_runs": 4,

                "extra_type": "",

                "wicket": "No",

                "player_out": "",

                "batting_team":
                "India",

                "innings": 1
            },

            {

                "match_id": "M1",

                "striker": "Virat",

                "non_striker": "Rohit",

                "bowler": "Bumrah",

                "runs_off_bat": 6,

                "total_runs": 6,

                "extra_type": "",

                "wicket": "No",

                "player_out": "",

                "batting_team":
                "India",

                "innings": 1
            },

            {

                "match_id": "M1",

                "striker": "Virat",

                "non_striker": "Rohit",

                "bowler": "Shami",

                "runs_off_bat": 0,

                "total_runs": 0,

                "extra_type": "",

                "wicket": "Yes",

                "player_out": "Virat",

                "batting_team":
                "India",

                "innings": 1
            }
        ]

        return pd.DataFrame(data)

    # ======================================
    # BATTING STATS
    # ======================================

    def test_batting_stats(self):

        df = self.sample_ball_df()

        batting = batting_career_stats(
            df
        )

        player = batting[
            batting["Player"]
            == "Virat"
        ].iloc[0]

        self.assertEqual(
            player["Runs"],
            10
        )

    # ======================================
    # BOWLING STATS
    # ======================================

    def test_bowling_stats(self):

        df = self.sample_ball_df()

        bowling = bowling_career_stats(
            df
        )

        bowler = bowling[
            bowling["Bowler"]
            == "Shami"
        ].iloc[0]

        self.assertEqual(
            bowler["Wickets"],
            1
        )

    # ======================================
    # HIGHEST TEAM SCORE
    # ======================================

    def test_highest_team_score(self):

        df = self.sample_ball_df()

        highest = highest_team_score(
            df,
            "India"
        )

        self.assertEqual(
            highest,
            10
        )

    # ======================================
    # LOWEST TEAM SCORE
    # ======================================

    def test_lowest_team_score(self):

        df = self.sample_ball_df()

        lowest = lowest_team_score(
            df,
            "India"
        )

        self.assertEqual(
            lowest,
            10
        )

# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    unittest.main()