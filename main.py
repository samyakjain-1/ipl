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
# import plotly.express as px
import altair as alt



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
        "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    }
    
    for col in ["team1", "team2", "toss_winner", "winner"]:
        df[col] = df[col].replace(team_name_mapping)
        
    
    df["season"] = df["date"].dt.year
    return df





df = load_and_clean_data()

st.title("IPL Match Visualizer")
st.write("Here is a sample of the dataset:")
st.dataframe(df)

#match wins visualization
st.title("IPL Match Wins Visualization")
st.markdown("### How many matches has each team won?")

# Count team wins and calculate percentages
win_counts = df["winner"].value_counts().sort_values(ascending=False)
total_wins = win_counts.sum()
win_percentages = (win_counts / total_wins * 100).round(2)

# Create dataframe for chart
win_df = pd.DataFrame({
    "Team": win_counts.index,
    "Wins": win_counts.values,
    "Win %": win_percentages.values
})

# Get or initialize query param state
query_params = st.query_params
selected_team = query_params.get("team")

# Define selection object for Altair
team_select = alt.selection_single(fields=["Team"], name="team")

# Altair bar chart
bar_chart = alt.Chart(win_df).mark_bar().encode(
    x=alt.X("Team:N", sort="-y"),
    y="Wins:Q",
    color=alt.condition(
        team_select,
        alt.value("orange"),
        alt.value("gray")
    ),
    tooltip=["Team", "Wins", "Win %"]
).add_selection(team_select).properties(
    width=700,
    height=400,
    title="Total Matches Won by Each IPL Team"
)

# Add percentage text above bars
text = alt.Chart(win_df).mark_text(
    align='center',
    baseline='bottom',
    dy=-5
).encode(
    x="Team:N",
    y="Wins:Q",
    text=alt.Text("Win %:Q", format=".1f"),
    opacity=alt.condition(team_select, alt.value(1), alt.value(0.5))
)

# Display interactive chart
st.altair_chart(bar_chart + text, use_container_width=True)


# win trend over seasons
st.markdown("---")
st.markdown("## Win Trend of Each Team Over Seasons")

# Dropdown to select team
team_list = df["winner"].unique()
selected_team = st.selectbox("Select a team to view win trend over seasons:", sorted(team_list))

# Filter and group by season
team_wins = df[df["winner"] == selected_team]
season_wins = team_wins["season"].value_counts().sort_index()

# Plot the trend

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
st.markdown(f"### {selected_team}'s peak season was **{peak_year}** with **{peak_wins} wins**.")


# toss winner vs match winner
st.markdown("---")
st.markdown("## Toss Winner vs Match Winner")


# Check where toss winner also won the match
toss_and_match_winner = df["toss_winner"] == df["winner"]

# Count true (same) and false (different)
counts = toss_and_match_winner.value_counts()
counts.index = ["Toss Winner Won", "Toss Winner Lost"]

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
ax.pie(counts, labels=counts.index, autopct='%1.1f%%', colors=["blue", "grey"], startangle=90)
ax.set_title("### Toss Winner vs Match Outcome")
st.pyplot(fig)


#stadium-wise matches
st.markdown("---")
st.markdown("## Which Stadiums hosted the most matches?")

venue_counts = df["venue"].value_counts().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(venue_counts.index[:10], venue_counts.values[:10], color="steelblue")
ax.set_title("Top 10 IPL Venues by Number of Matches")
ax.set_ylabel("Number of Matches")
ax.set_xlabel("Venue")
ax.set_xticklabels(venue_counts.index[:10], rotation=45, ha="right")

# Add count labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 2, str(height), ha='center', fontsize=9)

st.pyplot(fig)

top_venue = venue_counts.idxmax()
top_count = venue_counts.max()
st.markdown(f"### The most matches were played at **{top_venue}** with **{top_count}** total matches.")
st.markdown(f"### Suprisingly, Dubai Stadium is also in the top 10 venues across all seasons.")


#top motm
st.markdown("---")
st.markdown("## Top Player of the Match Winners")

top_n = st.selectbox("Select number of top players to display:", [5, 10, 20, 50])

# Count top N PoM awards
pom_counts = df["player_of_match"].value_counts().head(top_n)

# Plot chart
fig, ax = plt.subplots(figsize=(12, 6 + top_n * 0.2))
bars = ax.barh(pom_counts.index[::-1], pom_counts.values[::-1], color="purple")
ax.set_title(f"Top {top_n} Players with Most Player of the Match Awards")
ax.set_xlabel("Number of Awards")
ax.set_ylabel("Player")

# Add labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, str(int(width)), va='center')

st.pyplot(fig)

# Summary
top_player = pom_counts.idxmax()
top_awards = pom_counts.max()
st.markdown(f"### **{top_player}** leads this list with **{top_awards}** Player of the Match awards.")



#matches player over seasons
st.markdown("---")
st.markdown("## Matches Played Each Season")

# Count matches by season
matches_per_season = df["season"].value_counts().sort_index()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(matches_per_season.index, matches_per_season.values, color="blue")
ax.set_title("Number of Matches Played Each IPL Season")
ax.set_xlabel("Season")
ax.set_ylabel("Number of Matches")

# Add labels
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 1, str(height), ha='center', fontsize=9)

st.pyplot(fig)

# Summary
max_season = matches_per_season.idxmax()
max_count = matches_per_season.max()
st.markdown(f"### The **{max_season}** season had the most matches  **{max_count}** in total.")


#nail-biting matches
st.markdown("---")
st.markdown("## Nail-Biter Matches by Season")

# Filter nail-biters: <9 runs OR <3 wickets OR super over
nail_biter_matches = df[
    ((df["result"] == "runs") & (df["result_margin"] < 9)) |
    ((df["result"] == "wickets") & (df["result_margin"] < 3)) |
    (df["super_over"] == True)
]

# Count by season
nail_biters_by_season = nail_biter_matches["season"].value_counts().sort_index()

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(nail_biters_by_season.index, nail_biters_by_season.values, color="crimson")
ax.set_title("Number of Nail-Biter Matches Per Season")
ax.set_xlabel("Season")
ax.set_ylabel("Nail-Biters")

for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, str(height), ha='center')

st.pyplot(fig)

# Summary
most_nailbiting_season = nail_biters_by_season.idxmax()
nailbiter_count = nail_biters_by_season.max()
st.markdown(f"### The most nail-biters happened in **{most_nailbiting_season}** with **{nailbiter_count}** total close matches!")