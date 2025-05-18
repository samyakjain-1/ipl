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
        
    df["season"] = df["season"].apply(normalize_season)

    return df

def normalize_season(s):
    try:
        if isinstance(s, str) and "/" in s:
            # If season like "2007/08" → take second part and convert to 2008
            end_year = int(s.split("/")[-1])
            return 2000 + end_year if end_year < 100 else end_year
        else:
            # Try to cast to int and ensure it's 4-digit
            s = int(float(s))
            return s if s > 1000 else 2000 + s
    except:
        return None  # or raise/log depending on how strict you want to be



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


# win trend over seasons
st.markdown("---")
st.markdown("## 📊 Win Trend of Each Team Over Seasons")

# Dropdown to select team
team_list = df["winner"].unique()
selected_team = st.selectbox("Select a team to view win trend over seasons:", sorted(team_list))

# Filter and group by season
team_wins = df[df["winner"] == selected_team]
season_wins = team_wins["season"].value_counts().sort_index()

# Plot the trend
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(season_wins.index, season_wins.values, marker='o', linewidth=2)
ax.set_title(f"{selected_team} - Wins by Season")
ax.set_xlabel("Season")
ax.set_ylabel("Wins")
ax.grid(True)

st.pyplot(fig)

# Summary of peak season
peak_year = season_wins.idxmax()
peak_wins = season_wins.max()
st.markdown(f"### 📈 {selected_team}'s peak season was **{peak_year}** with **{peak_wins} wins**.")


# toss winner vs match winner
st.markdown("---")
st.markdown("## 🎯 Toss Winner vs Match Winner")


# Check where toss winner also won the match
toss_and_match_winner = df["toss_winner"] == df["winner"]

# Count true (same) and false (different)
counts = toss_and_match_winner.value_counts()
counts.index = ["Toss Winner Also Won", "Toss Winner Lost"]

# fig, ax = plt.subplots()
# bars = ax.bar(counts.index, counts.values, color=["green", "red"])
# ax.set_title("Did the Toss Winner Also Win the Match?")
# ax.set_ylabel("Number of Matches")

# # Add count labels on top
# for bar in bars:
#     height = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2, height + 5, str(height), ha='center')

# st.pyplot(fig)

fig, ax = plt.subplots()
ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=["blue", "black"], startangle=90)
ax.set_title("Toss Winner vs Match Outcome")
st.pyplot(fig)

