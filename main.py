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
import plotly.express as px
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
st.markdown("""
🏆 This interactive bar chart displays the total number of matches won by each IPL team throughout 
the tournament's history. We calculated the number of wins using the "winner" column and also computed 
each team's win percentage relative to the total matches. You can click on any team in the chart to 
highlight it and view its stats. The chart also displays the win percentage above each bar to give a 
clearer picture of relative performance. This visualization helps fans compare overall success and 
dominance of different IPL teams over the years.
""")

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

st.markdown("This section visualizes how many matches a selected IPL team has won in each season. We filtered the dataset by the chosen team using a dropdown, grouped their match wins by season, and displayed the trend as a line chart. This helps analyze consistency and performance spikes across different IPL editions.")

# Dropdown to select team
team_list = sorted(df["winner"].dropna().unique())
selected_team = st.selectbox("Select a team to view win trend over seasons:", team_list)

# Compute season-wise wins
team_wins = df[df["winner"] == selected_team]
season_wins = team_wins["season"].value_counts().sort_index()
season_wins_df = season_wins.reset_index()
season_wins_df.columns = ["Season", "Wins"]

# Convert 'Season' to string so Streamlit treats x-axis as categorical
season_wins_df["Season"] = season_wins_df["Season"].astype(str)

# Streamlit line chart
st.line_chart(season_wins_df.set_index("Season"))

# Summary
peak_year = season_wins.idxmax()
peak_wins = season_wins.max()
st.markdown(f"### {selected_team}'s peak season was **{peak_year}** with **{peak_wins} wins**.")



# Toss winner vs match winner
st.markdown("---")
st.markdown("## Toss Winner vs Match Winner")
st.markdown("This chart compares the number of times the team that won the toss also won the match versus when they didn't. We created a Boolean condition to check if the toss winner equals the match winner and then counted those outcomes. The pie chart shows how often toss-winning teams convert their advantage into a match win — offering insight into how critical the toss might be in IPL outcomes.")
# Check where toss winner also won the match
toss_and_match_winner = df["toss_winner"] == df["winner"]

# Count true (same) and false (different)
counts = toss_and_match_winner.value_counts()
counts.index = ["Toss Winner Won", "Toss Winner Lost"]

# Convert to DataFrame for Plotly
toss_df = counts.reset_index()
toss_df.columns = ["Outcome", "Count"]

# Plotly pie chart
fig = px.pie(
    toss_df,
    names="Outcome",
    values="Count",
    title="Toss Winner vs Match Outcome",
    color_discrete_sequence=["blue", "grey"]
)

# Display in Streamlit
st.plotly_chart(fig)


# Stadium-wise matches
st.markdown("---")
st.markdown("## Which Stadiums hosted the most matches?")
st.markdown("""
🏟️ Here, we ranked the top 10 stadiums by the total number of IPL matches they've hosted. 
The data is grouped by the "venue" column and sorted to display the venues with the most matches. 
This bar chart helps us see which stadiums are most frequently used across IPL seasons and includes 
an observation about Dubai's rise as a venue.
""")

# Get top 10 venues by number of matches
venue_counts = df["venue"].value_counts().sort_values(ascending=False).head(10)

# Convert to DataFrame for st.bar_chart
venue_df = venue_counts.reset_index()
venue_df.columns = ["Venue", "Matches"]
venue_df["Venue"] = venue_df["Venue"].astype(str)  # Ensure x-axis is treated as categorical
venue_df = venue_df.set_index("Venue")

# Display chart
st.bar_chart(venue_df)
#added a summary
# Add summary
top_venue = venue_counts.idxmax()
top_count = venue_counts.max()
st.markdown(f"### The most matches were played at **{top_venue}** with **{top_count}** total matches.")
st.markdown("### Surprisingly, Dubai Stadium is also in the top 10 venues across all seasons.")


# Top Player of the Match
st.markdown("---")
st.markdown("## Top Player of the Match Winners")
st.markdown("""
🏅 This section showcases the players with the most "Player of the Match" awards in IPL history. 
A dropdown allows users to select the top 5, 10, 20, or 50 players. We counted appearances of each 
player in the "player_of_match" column and plotted the selected top ones. This visual highlights 
the most impactful and consistent match-winning players.
""")

# Dropdown to select top N players
top_n = st.selectbox("Select number of top players to display:", [5, 10, 20, 50])

# Get top N player-of-the-match counts
pom_counts = df["player_of_match"].value_counts().head(top_n)

# Convert to DataFrame
pom_df = pom_counts.reset_index()
pom_df.columns = ["Player", "Awards"]
pom_df["Player"] = pom_df["Player"].astype(str)
pom_df = pom_df.set_index("Player")

# Reverse for "horizontal-like" visual (top players at bottom)
pom_df = pom_df[::-1]

# Streamlit native bar chart
st.bar_chart(pom_df)

# Summary
top_player = pom_counts.idxmax()
top_awards = pom_counts.max()
st.markdown(f"### **{top_player}** leads this list with **{top_awards}** Player of the Match awards.")




# Matches Played Each Season
st.markdown("---")
st.markdown("## Matches Played Each Season")
st.markdown("""
📆 This bar chart displays how many IPL matches were played in each season. We counted matches by 
the "season" field and plotted them chronologically. This gives insight into how the tournament has 
evolved in scale and format — including seasons with more playoff matches or special circumstances 
like COVID affecting schedule size.
""")

# Count matches by season
matches_per_season = df["season"].value_counts().sort_index()

# Convert to DataFrame
season_df = matches_per_season.reset_index()
season_df.columns = ["Season", "Matches"]
season_df["Season"] = season_df["Season"].astype(str)  # Treat x-axis as categorical
season_df = season_df.set_index("Season")

# Streamlit bar chart
st.bar_chart(season_df)

# Summary
max_season = matches_per_season.idxmax()
max_count = matches_per_season.max()
st.markdown(f"### The **{max_season}** season had the most matches — **{max_count}** in total.")



# Nail-Biter Matches by Season
st.markdown("---")
st.markdown("## Nail-Biter Matches by Season")
st.markdown("""
🔥 This section analyzes the most thrilling IPL matches — the "nail-biters." We defined a match as 
a nail-biter if it was decided by less than 9 runs, fewer than 3 wickets, or went to a Super Over. 
After filtering such close matches, we counted how many occurred in each season and displayed the 
results. This helps highlight which IPL seasons had the most edge-of-your-seat finishes.
""")

# Filter nail-biters: <9 runs OR <3 wickets OR super over
nail_biter_matches = df[
    ((df["result"] == "runs") & (df["result_margin"] < 9)) |
    ((df["result"] == "wickets") & (df["result_margin"] < 3)) |
    (df["super_over"] == True)
]

# Count by season
nail_biters_by_season = nail_biter_matches["season"].value_counts().sort_index()

# Convert to DataFrame for Streamlit
nailbiter_df = nail_biters_by_season.reset_index()
nailbiter_df.columns = ["Season", "Nail-Biters"]
nailbiter_df["Season"] = nailbiter_df["Season"].astype(str)
nailbiter_df = nailbiter_df.set_index("Season")

# Display chart
st.bar_chart(nailbiter_df)

# Summary
most_nailbiting_season = nail_biters_by_season.idxmax()
nailbiter_count = nail_biters_by_season.max()
st.markdown(f"### The most nail-biters happened in **{most_nailbiting_season}** with **{nailbiter_count}** total close matches!")

st.markdown("---")
st.markdown("## 🙏 Acknowledgements")

st.markdown("""
This project is based on publicly available IPL match data and was built using:

- 🐍 **Python**
- 📊 **Pandas** for data handling
- 📈 **Altair**, **Plotly** & **Streamlit** for interactive charts and dashboards

Thanks for checking it out!
""")