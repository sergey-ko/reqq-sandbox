import streamlit as st
import requests
import pandas as pd

st.set_page_config(layout="wide")
st.title("Assess requirements quality")
st.subheader("according to INCOSE rules")

with open('req_examples.txt', 'r') as file:
    options = [line.strip() for line in file]

selected_option = st.selectbox("Select an example", options)

# Configuring input as multiline input
user_input = st.text_area("Enter requirement text here:", selected_option)

# Variable to control the disabled state of the button
button_disabled = False
submit_btn = st.button("Submit", disabled=button_disabled)

# Create a placeholder
processing_placeholder = st.empty()

# Send POST request to API
if submit_btn:
    button_disabled = True
    processing_placeholder.text("Processing ... it might take up to 1 minute. Please wait.")

    api_url = "https://apimreqq.azure-api.net/Assessment"
    response = requests.post(api_url+"?requirementText="+user_input, headers={"Ocp-Apim-Subscription-Key": st.secrets["api_key"] })
                              
    if response.status_code == 200:
        results = response.json()

        # Display text proposal
        st.write("Proposal:")
        st.write(results["proposedText"])

        # Display results in a table
        st.write("Results:")       

        df = pd.DataFrame(results['assessments'])
        df = df.drop(columns=['ruleDescription','isAcceptable'])
        df = df.rename(columns={'ruleName': 'Rule', 
                                'score': 'Score',
                                'ruleId':'ID',
                                'comment':'Comment'})
        results_table = df

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
        
        button_disabled = False
        processing_placeholder.empty()
    else:
        button_disabled = False
        processing_placeholder.text("We experienced some error, please retry or contact support.")


        
        


