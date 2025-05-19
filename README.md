# 🏏 IPL Match Visualizer

Welcome to the **IPL Match Visualizer** — a website built using Python and Streamlit to help fans, analysts, and curious minds explore historical data from the **Indian Premier League (IPL)** in a visual, interactive way.

This project takes raw IPL data (from official records) and turns it into beautiful, easy-to-understand graphs and summaries — so anyone can explore how their favorite teams and players have performed over the years.

---

## 🎯 What This Website Can Do

Here’s what you can explore with this app:

- **🏆 How many matches each team has won?**
- **📈 How each team’s performance has changed over the seasons?**
- **🎲 Does winning the toss actually help you win the match?**
- **🏟️ Which stadiums have hosted the most IPL matches?**
- **🌟 Who has won the most Player of the Match awards?**
- **📅 How the number of matches has changed over the years?**
- **🔥 Which seasons had the most nail-biting, close finishes?**

Each section includes easy-to-use charts and short summaries so you don’t need any stats or cricket expertise to enjoy the data.

---

## 🧹 How the Data Was Cleaned and Prepared

When I started, the IPL data was in a raw CSV file (like a big spreadsheet). It had:
- Missing values (e.g., no umpire listed in some matches)
- Inconsistent team names (e.g., "Delhi Daredevils" vs. "Delhi Capitals")
- Some values stored in technical or confusing ways

### Here's what I did:
- 🧼 **Filled in missing info** like unknown cities or umpires
- 🔁 **Standardized team names** so each team has only one name across all seasons
- 📅 **Converted dates into seasons** so I can group matches by year
- ✅ **Removed rows with incomplete data** (like matches with no winner)

This step was crucial to make sure the charts and calculations were accurate and easy to understand.

---

## 📊 How Each Visualization Was Built

### 1. **Total Match Wins by Team**
I counted how many matches each team has won and calculated their win percentage. I used a bar chart that lets users highlight any team and see how successful they’ve been across IPL history.

### 2. **Win Trend Over the Years**
I let users pick a team and then show a line chart of how many matches they’ve won each season. This helps you see when a team had its best or worst years.

### 3. **Toss Winner vs Match Winner**
I checked whether the team that won the toss ended up winning the match. I then showed the result in a pie chart to easily understand whether the toss gives a real advantage.

### 4. **Top Stadiums**
I looked at which stadiums have hosted the most matches. This helps see where IPL games happen most frequently, and reveals interesting facts (like Dubai being in the top 10!).

### 5. **Top Player of the Match Winners**
I counted how many times each player was named “Player of the Match.” The user can choose to see the top 5, 10, 20, or 50 players.

### 6. **Matches Played Each Season**
I displayed how the number of matches per season has changed — some seasons had more games, others fewer (like during COVID).

### 7. **Nail-Biter Matches**
I defined a match as a “nail-biter” if it was:
- Won by fewer than 9 runs, or
- Won by fewer than 3 wickets, or
- Went to a Super Over

I then showed which seasons had the most thrilling, down-to-the-wire games.

---

## 💡 Challenges Faced

Building this project wasn’t always straightforward. Here are a few challenges and how I solved them:

- **Team names kept changing over the years**  
  → I created a mapping to unify names (e.g., "Delhi Daredevils" → "Delhi Capitals")

- **Missing data like umpires or cities**  
  → I filled missing values with placeholders like “Unknown” or “No umpire” to keep the data clean

- **Some years showed up as 2,008 instead of 2008**  
  → This was due to number formatting, so I converted year values to text

- **Some tools didn’t let us track what the user clicked on**  
  → I used Streamlit’s built-in `query_params` feature to remember user selections

- **Showing too much data at once could be overwhelming**  
  → So I added dropdowns and filters to keep things simple and interactive

---

## 🌍 Where You Can Use This

This app can be used by:
- **Fans** who want to explore their favorite team’s success
- **Analysts** who want to dig into trends and patterns
- **Students** learning about data science and visualization
- **Anyone curious** about how cricket matches unfold season after season

---

## 🙏 Acknowledgements

This project is based on publicly available IPL match data and was built using:
- 🐍 Python
- 📊 Pandas for data handling
- 📈 Altair, Plotly & Streamlit for interactive charts and dashboards

Thanks for checking it out! Let us know if you have feedback or feature ideas — we’d love to hear from you!


