import numpy as np
import pandas as pd

data = pd.read_csv("../../data/players_21.csv")

# Renaming columns

data.rename(
    columns={
        "height_cm": "Height(cm)",
        "weight_kg": "Weight(kg)",
        "skill_moves": "Skill Moves",
        "attacking_crossing": "Crossing",
        "attacking_finishing": "Finishing",
        "attacking_heading_accuracy": "Heading Accuracy",
        "attacking_short_passing": "Short Passing",
        "attacking_volleys": "Volleys",
        "skill_dribbling": "Dribbling",
        "skill_curve": "Curve",
        "skill_fk_accuracy": "FK. Accuracy",
        "skill_long_passing": "Long Passing",
        "skill_ball_control": "Ball Control",
        "movement_acceleration": "Acceleration",
        "movement_sprint_speed": "Sprint Speed",
        "movement_agility": "Agility",
        "movement_reactions": "Reactions",
        "movement_balance": "Balance",
        "power_shot_power": "Shot Power",
        "power_jumping": "Jumping",
        "power_stamina": "Stamina",
        "power_strength": "Strength",
        "power_long_shots": "Long Shots",
        "mentality_aggression": "Aggression",
        "mentality_interceptions": "Interceptions",
        "mentality_positioning": "Positioning",
        "mentality_vision": "Vision",
        "mentality_penalties": "Penalties",
        "mentality_composure": "Composure",
        "defending_marking": "Marking",
        "defending_standing_tackle": "Standing Tackle",
        "defending_sliding_tackle": "Sliding Tackle",
    },
    inplace=True,
)


# Creating a function that extracts the primary position
def sim_pos(row):
    """
    row : takes the input as the row where the transformation is needed.
    It extracts the very first player position using the partition method
    of a dataframe,
    """

    return row.player_positions.partition(",")[0]


# Creating a function that assigns a value to determine strongness of right foot
def foot_trans(row):
    """
    row : takes the input as the row where the transformation is needed.
    It works in conjunction with 'weak_foot' to create a new column
    named as 'Right Foot' and assigns a score between -5 to 5 for right foot.
    """

    if row.preferred_foot == "Right":
        return 5 - row.weak_foot
    else:
        return row.weak_foot - 5


# Creating a function that renames positions with fuzzy positions
def pos_trans(row):
    """
    row : takes the input as the row where the transformation is needed.
    It works in conjunction with 'player_positions' to create a new column
    named as 'rough_position'.
    """

    if row.player_positions in ["ST", "CF"]:
        return "ST"
    if row.player_positions in ["LW", "RW", "LM", "RM"]:
        return "WF"
    if row.player_positions in ["CAM", "CDM", "CM"]:
        return "MF"
    if row.player_positions in ["LWB", "RWB", "LB", "RB"]:
        return "WB"
    if row.player_positions in ["CB"]:
        return "CB"
    if row.player_positions in ["GK"]:
        return "GK"


def calc_marking(row):
    """
    row : takes the input as the row where the transformation is needed.
    """
    if row["player_positions"] != "GK":
        return int(
            (
                10 * row["defending"]
                - 3 * row["Standing Tackle"]
                - 2 * row["Interceptions"]
                - row["Heading Accuracy"]
                - row["Sliding Tackle"]
            )
            / 3
        )
    else:
        return np.nan


data["player_positions"] = data.apply(sim_pos, axis=1)
data["Right Foot"] = data.apply(foot_trans, axis=1)
data["rough_position"] = data.apply(pos_trans, axis=1)
data["Marking"] = data.apply(calc_marking, axis=1)

data.to_csv("../../data/processed_data.csv")
