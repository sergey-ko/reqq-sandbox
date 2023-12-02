import streamlit as st
import requests
import yaml
import time

st.set_page_config(layout="wide")
st.title("Assess requirements quality")
st.subheader("according to INCOSE rules")

with open('req_examples.txt', 'r') as file:
    options = [line.strip() for line in file]

selected_option = st.selectbox("Select an example", options)

# Configuring input as multiline input
user_input = st.text_area("Enter requirement text here:", selected_option)

with open('req_1.gpt4.yaml', 'r', encoding='utf-8') as file:
    r1_gpt4 = yaml.safe_load(file)

results = r1_gpt4

# Send POST request to API
if st.button("Submit"):
    # response = requests.post("https://api.example.com/endpoint", json={"text": user_input})
    # if response.status_code == 200:
    #     results = response.json()
        time.sleep(1)  # Add a 1-second delay

        
        

        # Display text proposal
        st.write("Proposal:")
        st.write(results["ProposedText"])

        # Display results in a table
        st.write("Results:")

        import pandas as pd

        df = pd.DataFrame(results['Assessments'])
        df = df.drop(columns=['RuleDescription','IsAcceptable'])
        df = df.rename(columns={'RuleName': 'Rule', 'RuleScore': 'Score','RuleId':'ID'})
        results_table = df

        # def format_score(score):
        #     if score == 1:
        #         return '<span style="color: red;">{}</span>'.format(score)
        #     elif score == 3:
        #         return '<span style="color: yellow;">{}</span>'.format(score)
        #     elif score == 5:
        #         return '<span style="color: green;">{}</span>'.format(score)
        #     else:
        #         return score

        # results_table['Score'] = results_table['Score'].apply(format_score)

        st.dataframe(results_table, 
                     use_container_width=True, 
                     hide_index=True, 
                     column_config={
                        "ID": st.column_config.TextColumn(
                            "ID",
                            help="ID",
                            width="small",
                        ),
                        "Rule": st.column_config.TextColumn(
                            "Rule",
                            help="Rule",
                            width="medium",
                        ),
                        "Score": st.column_config.ProgressColumn(
                            "Score",
                            help="1 is bad, 5 is perfect",
                            format="%f",
                            width="small",
                            min_value=1,
                            max_value=5,
                        ),
                        "Comment": st.column_config.TextColumn(
                            "Comment",
                            help="Comment",
                            width="large",
                        ),
                        },                    
                     column_order=['ID','Rule','Score','Comment'])


