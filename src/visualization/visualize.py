import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.display import HTML
import plotly.graph_objs as go  # For interactive graphs
import plotly.express as px

data = pd.read_csv("../../data/processed_data.csv")


def save_styled_dataframe_to_html(df, file_name):
    # Define the directory where you want to save the file
    save_directory = "../../reports/"

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Define the full file path, combining the directory and the specified file name
    file_path = os.path.join(save_directory, file_name)

    # Define a custom color mapping function
    def color_map(val):
        color = f"rgb(0, {255 - val * 2}, 0)"  # Create varying shades of green
        return f"background-color: {color}"

    # Apply the custom color mapping to the DataFrame
    styled_table = (
        df.style.set_caption("Top Players")
        .set_table_styles(
            [{"selector": "tr:hover", "props": [("background-color", "#0080ff")]}]
        )
        .set_precision(0)
        .background_gradient(cmap="Greens")
    )

    # Render the styled table to HTML
    styled_html = HTML(styled_table.render())

    # Save the rendered HTML to the specified file path
    with open(file_path, "w") as file:
        file.write("styled_html")
    return styled_table


# Creating a new dataframe - top_player
top_player = data[
    data.short_name.isin(
        [
            "L. Messi",
            "Cristiano Ronaldo",
            "R. Lewandowski",
            "K. De Bruyne",
            "K. Mbappé",
            "Neymar Jr",
            "Sergio Ramos",
            "N. Kanté",
            "T. Kroos",
            "M. Salah",
            "K. Benzema",
            "G. Bale",
        ]
    )
]
top_player = top_player[
    [
        "short_name",
        "club_name",
        "rough_position",
        "pace",
        "shooting",
        "passing",
        "dribbling",
        "defending",
        "physic",
        "overall",
    ]
].reset_index(drop=True)

save_styled_dataframe_to_html(top_player, "top_players.html")


def compare_players(list_of_players, file_name):
    """
    The function accepts the names of players whose stats we want to compare.
    """
    output_dir = "../../reports/figures/plots"
    os.makedirs(output_dir, exist_ok=True)

    names = list_of_players
    fig = go.Figure()

    # The stats we are using to compare, Feel free to use your own stats.
    stats = ["pace", "shooting", "passing", "dribbling", "defending", "Acceleration"]
    for name in names:
        # Extract player stats based on name
        player_stats = data[data["short_name"].str.contains(name)][stats]

        fig.add_trace(
            go.Scatterpolar(
                # Passing numeric parameters
                r=player_stats.iloc[0],
                # Passing parameter names
                theta=[
                    "Pacing",
                    "Shooting",
                    "Passing",
                    "Dribbling",
                    "Defending",
                    "Acceleration",
                    "Pacing",
                ],
                # Setting the fill parameter
                fill="toself",
                # Specify the signature on hover
                hovertemplate="<b>%{theta}</b>" + f"<b>: " + "%{r}",
                # Specify a caption for the legend
                name=name,
                opacity=0.6,
            )
        )

        fig.update_layout(
            # Set the name of the chart
            title="Comparison between players",
            # Setting the background color
            paper_bgcolor="rgb(223, 223, 223)",
            # Setting the chart theme
            template="xgridoff",
            # Passing chart parameters
            polar=dict(
                # Background color
                bgcolor="rgba(223, 223, 223, 0.6)",
                # Adding a line with numeric divisions
                radialaxis=dict(
                    # Displaying the line
                    visible=True,
                    # Set the range of divisions
                    range=[0, 100],
                ),
            ),
        )

    output_file = os.path.join(output_dir, f"plot_{file_name}.png")
    if os.path.exists(output_file):
        os.remove(output_file)
    plt.savefig(output_file)

    fig.show()


compare_players(["L. Messi", "Cristiano Ronaldo"], "messi_vs_ronaldo")

compare_players(["Neymar Jr", "Pogba", "K. Mbappé"], "ney_mbappe_pogba")


def plot_position_distribution(data):
    output_dir = "../../reports/figures/plots"
    os.makedirs(output_dir, exist_ok=True)

    all_pos = data["player_positions"].unique()
    sta_pos = pd.DataFrame(np.zeros(15).reshape(1, 15), columns=all_pos)

    def add(row):
        sta_pos[row.player_positions][0] += 1

    data.apply(add, axis=1)
    sta_pos = sta_pos.loc[:, ~(sta_pos == 0).all()]

    fig = px.pie(sta_pos, values=sta_pos.loc[0, :], names=sta_pos.columns)

    fig.update_traces(textposition="inside", textinfo="percent+label")

    fig.update_layout(
        height=600, width=1000, title_text="Proportion of Each Position", title_x=0.5
    )

    fig.update_traces(
        textfont_size=12, marker=dict(line=dict(color="#000000", width=2))
    )
    output_file = os.path.join(output_dir, f"position_distribution.png")
    if os.path.exists(output_file):
        os.remove(output_file)
    plt.savefig(output_file)

    fig.show()


plot_position_distribution(data)


def generate_and_display_boxplot(data, position):
    if position == "GK":
        label = ["DIV", "HAN", "KIC", "REF", "SPD", "POS"]
        columns = [
            "gk_diving",
            "gk_handling",
            "gk_kicking",
            "gk_reflexes",
            "gk_speed",
            "gk_positioning",
        ]
        title = "GK Boxplot"
        color = "red"
    elif position == "Non-GK":
        label = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"]
        columns = ["pace", "shooting", "passing", "dribbling", "defending", "physic"]
        title = "Non-GK Boxplot"
        color = "green"
    else:
        print("Invalid position. Please provide 'GK' or 'Non-GK'.")
        return

    output_dir = "../../reports/figures/plots"
    os.makedirs(output_dir, exist_ok=True)

    # Filter data based on the provided position
    if position == "GK":
        position_data = data[data["player_positions"] == "GK"]
    elif position == "Non-GK":
        position_data = data[data["player_positions"] != "GK"]
    else:
        print("Invalid position. Please provide 'GK' or 'Non-GK'.")
        return

    # Remove columns with all NaN values
    position_data = position_data.dropna(axis=1, how="all")

    # Remove rows with any NaN values in specific columns
    position_data = position_data.dropna(axis=0, how="any", subset=columns)

    # Extract column values for boxplot
    values = [position_data[column] for column in columns]

    fig, ax = plt.subplots()
    ax.boxplot(values, labels=label, patch_artist=True)
    ax.set_title(title)
    ax.set_xlabel("Attributes")
    ax.set_ylabel("Values")

    # Customize boxplot colors
    for box, color in zip(ax.artists, [color] * len(label)):
        box.set_facecolor(color)

    output_file = os.path.join(output_dir, f"boxplot_{position}.png")
    if os.path.exists(output_file):
        os.remove(output_file)
    plt.savefig(output_file)

    plt.show()


generate_and_display_boxplot(data, "GK")  # For GK boxplot
generate_and_display_boxplot(data, "Non-GK")  # For Non-GK boxplot

import matplotlib.pyplot as plt
import seaborn as sns
import os


def generate_and_save_heatmap(data):
    save_directory = "../../reports/figures/plots"
    club_pos_overall = (
        data.groupby(by=["club_name", "rough_position"], as_index=False)["overall"]
        .mean()
        .sort_values(by="overall", ascending=False)
        .head(250)
    )

    club_pos_overall = club_pos_overall.pivot_table(
        values="overall", index=["rough_position"], columns="club_name"
    )

    club_pos_overall.index = ["CB", "GK", "MF", "ST", "WB", "WF"]

    # Create a figure and a heatmap
    plt.figure(figsize=(40, 8))
    sns.heatmap(data=club_pos_overall, annot=True, cmap="coolwarm")

    # Add Cosmetics
    plt.title("Average Player Rating")
    plt.xlabel("FPL Club")
    plt.ylabel("FPL Position 2019-20")

    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Define the full file path, combining the directory and the specified file name
    file_path = os.path.join(save_directory, "heatmap.png")

    # Save the plot as an image file
    plt.savefig(file_path)

    plt.show()


generate_and_save_heatmap(data)
