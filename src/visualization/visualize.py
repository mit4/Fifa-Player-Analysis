import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.display import HTML
import os

data = pd.read_csv("data/processed_data.csv")


def save_styled_dataframe_to_html(df, file_name):
    # Define the directory where you want to save the file
    save_directory = "reports/"

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
        file.write(styled_table.to_html(escape=False))

    print(f"Styled table saved to '{file_path}'")


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


def plot_position_distribution(data):
    output_dir = "reports/figures/plots"
    os.makedirs(output_dir, exist_ok=True)

    all_pos = data["player_positions"].unique()
    stat_pos = pd.DataFrame(np.zeros(15).reshape(1, 15), columns=all_pos)

    def add(row):
        stat_pos[row.player_positions][0] += 1

    data.apply(add, axis=1)
    stat_pos = stat_pos.loc[:, ~(stat_pos == 0).all()]

    # Create a pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(
        stat_pos.loc[0, :], labels=stat_pos.columns, autopct="%1.1f%%", startangle=90
    )

    ax.set_title("Proportion of Each Position")
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    output_file = os.path.join(output_dir, "position_distribution.png")
    plt.savefig(output_file)

    plt.show()


# Example usage:
plot_position_distribution(data)


def compare_players(list_of_players, file_name, data):
    output_dir = "reports/figures/plots"
    os.makedirs(output_dir, exist_ok=True)

    # Define stats and their labels
    stats = ["pace", "shooting", "passing", "dribbling", "defending", "Acceleration"]
    labels = ["Pace", "Shooting", "Passing", "Dribbling", "Defending", "Acceleration"]

    # Create a DataFrame to store player stats
    player_stats_df = pd.DataFrame(index=labels)

    for name in list_of_players:
        player_stats = data[data["short_name"].str.contains(name)][
            stats
        ].values.tolist()[0]
        player_stats_df[name] = player_stats

    # Normalize the stats to be between 0 and 1
    normalized_stats_df = player_stats_df / player_stats_df.max()

    # Number of stats and players
    num_stats = len(labels)
    num_players = len(list_of_players)

    # Create a radar chart
    angles = [n / float(num_stats) * 2 * 180 for n in range(num_stats)]
    angles += angles[:1]

    rad = [n / float(num_stats) * 2 * 3.14 for n in range(num_stats)]
    rad += rad[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True})

    for i, player in enumerate(list_of_players):
        player_stats = normalized_stats_df[player].values.tolist()
        player_stats += player_stats[:1]

        ax.plot(rad, player_stats, linewidth=2, linestyle="solid", label=player)
        ax.fill(rad, player_stats, alpha=0.2)

    ax.set_thetagrids(angles[:-1], labels)
    plt.yticks(
        [0.2, 0.4, 0.6, 0.8], ["0.2", "0.4", "0.6", "0.8"], color="grey", size=10
    )
    plt.ylim(0, 1)
    plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    plt.title("Comparison between players")

    output_file = os.path.join(output_dir, f"plot_{file_name}.png")
    plt.savefig(output_file)
    plt.show()


# Example usage:
compare_players(["L. Messi", "Cristiano Ronaldo"], "messi_vs_ronaldo", data)
compare_players(["Neymar Jr", "Pogba", "K. Mbappé"], "ney_mbappe_pogba", data)


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

    output_dir = "reports/figures/plots"
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
