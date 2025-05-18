# import csv

# with open('matches.csv', 'r') as file:

#     reader = csv.DictReader(file)

#     with open ('new_matches.csv', 'w') as new_file:
#         csv_writer = csv.writer(new_file, delimiter="\t")
        
        
#         for line in reader:
#             csv_writer.writerow(line)

import pandas as pd
import streamlit as st


def load_and_clean_data():
    df = pd.read_csv('matches.csv')
    
    #clean data
    df = df.drop(columns=["method"], errors="ignore")
    df["super_over"] = df["super_over"].map({"Y": True, "N": False})
    df["player_of_match"] = df["player_of_match"].fillna("No player of match")
    df["umpire1"] = df["umpire1"].fillna("No umpire")
    df["umpire2"] = df["umpire2"].fillna("No umpire")

    return df


df = load_and_clean_data()

st.title("IPL Match Visualizer")
st.write("Here is a sample of the dataset:")
st.dataframe(df)






