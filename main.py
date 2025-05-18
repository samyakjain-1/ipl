# import csv

# with open('matches.csv', 'r') as file:

#     reader = csv.DictReader(file)

#     with open ('new_matches.csv', 'w') as new_file:
#         csv_writer = csv.writer(new_file, delimiter="\t")
        
        
#         for line in reader:
#             csv_writer.writerow(line)

import pandas as pd
import streamlit as st

def load_data():
    df = pd.read_csv('matches.csv')
    return df

df = load_data()

st.title("IPL Match Visualizer")
st.write("Here is a sample of the dataset:")
st.dataframe(df)






