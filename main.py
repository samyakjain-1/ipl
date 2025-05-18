# import csv

# with open('matches.csv', 'r') as file:

#     reader = csv.DictReader(file)

#     with open ('new_matches.csv', 'w') as new_file:
#         csv_writer = csv.writer(new_file, delimiter="\t")
        
        
#         for line in reader:
#             csv_writer.writerow(line)

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


def load_and_clean_data():
    df = pd.read_csv('matches.csv')
    
    #clean data
    df = df.drop(columns=["method"], errors="ignore")
    df = df.dropna(subset=["winner"])
    df["super_over"] = df["super_over"].map({"Y": True, "N": False})
    df["player_of_match"] = df["player_of_match"].fillna("No player of match")
    df["city"] = df["city"].fillna("Unknown")
    df["date"] = pd.to_datetime(df["date"])
    df["umpire1"] = df["umpire1"].fillna("No umpire")
    df["umpire2"] = df["umpire2"].fillna("No umpire")
    
    # Normalize team names
    team_name_mapping = {
        "Delhi Daredevils": "Delhi Capitals",
        "Kings XI Punjab": "Punjab Kings",
        "Rising Pune Supergiant": "Rising Pune Supergiants",
        "Royal Challengers Bengaluru": "Royal Challengers Bangalore",
        "Gujarat Lions": "Gujarat Titans",  # optional
    }
    
    for col in ["team1", "team2", "toss_winner", "winner"]:
        df[col] = df[col].replace(team_name_mapping)

    return df


df = load_and_clean_data()

st.title("IPL Match Visualizer")
st.write("Here is a sample of the dataset:")
st.dataframe(df)

#match wins visualization
st.title("IPL Match Wins Visualization")
st.markdown("### How many matches has each team won?")

# Count how many times each team has won
win_counts = df["winner"].value_counts().sort_values(ascending=False)

#percentage-wise calculation
total_wins = win_counts.sum()
win_percentages = (win_counts / total_wins * 100).round(2)

#dropdown
teams = win_counts.index.tolist()
selected_team = st.selectbox("Select a team to highlight:", teams)


fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(win_counts.index, win_counts.values, color='gray')

# Highlight selected team
highlight_index = win_counts.index.tolist().index(selected_team)
bars[highlight_index].set_color('orange')

# Annotate percentage labels above bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    team = win_counts.index[i]
    percent = win_percentages[team]
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, f"{percent}%", 
            ha='center', va='bottom', fontsize=9)

# Style
ax.set_title("Total Matches Won by Each IPL Team")
ax.set_ylabel("Number of Wins")
ax.set_xticklabels(win_counts.index, rotation=45, ha='right')

st.pyplot(fig)
# Summary
st.markdown(f"### 🏏 {selected_team} has won **{win_counts[selected_team]}** matches in total.")



