import pandas as pd
import numpy as np
import streamlit as st
import pickle
from xgboost import XGBClassifier

st.title("The Bank Marketing Project")
st.markdown("* **First you have to enter values for the variable on the left side**")
st.markdown("* **Then you can click predict button to see the results**")
st.markdown("* **If you want to see the description of variables please click Descriptions button**")

col_1 , col_2 = st.columns([1,1])
with col_1 : 
    btn_1 = st.button("Descriptions")
with col_2 : 
    btn_2 = st.button("Close Description")

if btn_1 : 
    st.header("The Descriptions of variables")
    st.markdown("* **Age** - age of the customer")
    st.markdown("* **Age Group** - what age group does the customer lie (10 - 19 = 1 20 - 29 = 2 30 - 39 = 3 40 - 49 = 4 50 - 59 = 5 60 - 69 = 6 70 - 79 = 7 80 - 89 = 8 90 - 99 = 9")
    st.markdown("* **Eligible** - if the customer is eligible for the talk or not")
    st.markdown("* **Job** - what does the customer do?")
    st.markdown("* **Salary** - salary of the customer")
    st.markdown("* **Marital** - married or not?")
    st.markdown("* **Education** - level of education complited")
    st.markdown("* **Marital Education** - married or not- education")
    st.markdown("* **Targeted** - if the customer or being targeted or not")
    st.markdown("* **Default** - if the customer in default list or not")
    st.markdown("* **Balance** - remaining balance in their accounts")
    st.markdown("* **Housing** - housing")
    st.markdown("* **Loan** - has prior loan or not")
    st.markdown("* **Contact** - source of this information")
    st.markdown("* **Day** - today's date")
    st.markdown("* **Month** - Month")
    st.markdown("* **Duration** - number of days")
    st.markdown("* **Campaign** - marketing campaign")
    st.markdown("* **Pdays** - number of days that passed by after the client was last contacted")
    st.markdown("* **Previous** - previous response")
    st.markdown("* **Outcome** - outcome of the previous marketing campaign")
    st.markdown("* **Y** - predict if the customer will buy the product or not!")
    st.markdown("* **Response** - response of the actor")

if btn_2 : 
    print()

st.header("The Dataset")  
data = pd.read_csv("bank-marketing.csv")
st.write(data.head())
    
st.sidebar.header("Please select inputs")

Age = st.sidebar.slider(label = "Please select input for Age variable" , max_value = 95 , min_value = 15 , value = 15)
Age_group = st.sidebar.slider(label = "Please select input for Age group variable" , max_value = 9 , min_value = 0 , value = 0)
Eligible = st.sidebar.radio(label = "Please select input for Eligible variable (N = No , Y = Yes)" , options = ["N" , "Y"])
Job_test = st.sidebar.selectbox(label = "Please select input for Job variable" , options = ['management' , 'technician', 'entrepreneur', 'blue-collar','retired', 'admin.', 'services', 'self-employed','unemployed', 'housemaid', 'student'])
Job = int
if Job_test == 'management' : 
    Job = 8
elif Job_test == "uneployed" : 
    Job = 0
elif Job_test == "retired" : 
    Job = 10
elif Job_test == "student" : 
    Job = 1
elif Job_test == "housemaid" : 
    Job = 2
elif Job_test == "self-employed" : 
    Job = 3
elif Job_test == "services" : 
    Job = 4
elif Job_test == "blue-collar" : 
    Job = 5
elif Job_test == "technician" : 
    Job = 6
elif Job_test == "admin" : 
    Job = 7
elif Job_test == "entrepreneur" : 
    Job = 9
Salary = st.sidebar.slider(label = "Please select input for Salary variable" , max_value = 120000 , min_value = 0 , value = 0 , step = 1000)
Marital = st.sidebar.selectbox(label = "Please select input for Job variable" , options = ["married" , "single" ,"divorced"])
Education_test = st.sidebar.selectbox(label = "Please select input for Eduaction variable" , options = ["tertiary" , "secondary" , "primary"])
Education = int
if Education_test == "primary" : 
    Education = 0
elif Education_test == "secondary" : 
    Education = 1
elif Education_test == "tertiary" : 
    Education = 2
    
Marital_education = st.sidebar.selectbox(label = "Please select input for Marital education variable" , options = ['married-tertiary', 'single-secondary', 'married-secondary','married-unknown', 'single-unknown', 'single-tertiary','divorced-tertiary', 'married-primary', 'divorced-secondary','single-primary', 'divorced-primary', 'divorced-unknown'])
Targeted = st.sidebar.radio(label = "Please select input for Targeted variable" , options = ["no" , "yes"])
Default = st.sidebar.radio(label = "Please select input for Default variable" , options = ["no" , "yes"])
Balance = st.sidebar.slider(label = "Please select input for Balance group variable" , max_value = 102127 , min_value = -8019 , value = -8019 , step = 10)
Housing = st.sidebar.radio(label = "Please select input for Housing variable" , options = ["no" , "yes"])
Loan = st.sidebar.radio(label = "Please select input for Loan variable" , options = ["no" , "yes"])
Contact = st.sidebar.radio(label = "Please select input for Loan variable" , options = ["cellular" , "telephone"])
Day = st.sidebar.slider(label = "Please select input for Day group variable" , max_value = 31 , min_value = 1 , value = 1 , step = 1)
Month = st.sidebar.selectbox(label = "Please select input for Month variable" , options = ['may', 'jun', 'jul', 'aug', 'oct', 'nov', 'dec', 'jan', 'feb','mar', 'apr', 'sep'])
Duration = st.sidebar.slider(label = "Please select input for Duration group variable" , max_value = 4918 , min_value = 0 , value = 0)
Campaign = st.sidebar.slider(label = "Please select input for Campaign group variable" , max_value = 63 , min_value = 1 , value = 1)
Pdays = st.sidebar.slider(label = "Please select input for Pdays group variable" , max_value = 871 , min_value = -1 , value = -1)
Previous = st.sidebar.slider(label = "Please select input for Previous group variable" , max_value = 275 , min_value = 0 , value = 0)
Response = st.sidebar.radio(label = "Please select input for Response variable (0 = No , 1 = Yes)" , options = [0 , 1])

btn_3 = st.sidebar.button("Predict")


st.header("You have selected these inputs")

data_test = pd.DataFrame(data = {"Age" : [Age] , "Age group" : [Age_group] , "Eligible" : [Eligible] , "Job" : [Job] , "Salary" : [Salary], 
                                "Marital" : [Marital] , "Education" : [Education] , "Marital-education" : [Marital_education] , "Targeted" : [Targeted] , "Default" : [Default] , "Balance" : [Balance] , "Housing" : [Housing] , "Loan" : [Loan] ,"Contact" : [Contact], "Day" : [Day] , "Month" : [Month] , "Duration" : 	[Duration] , "Campaign" : [Campaign], "Pdays" : [Pdays] , "Previous" : [Previous] , "Response" : [Response]})

st.write(data_test.head())

if btn_3 : 
    st.header("The Predcition")
    model = pickle.load(open("Model", "rb"))
    prediction = model.predict(data_test)
    proba = model.predict_proba(data_test)
    if prediction == 0 : 
        st.markdown("The customer **won't** buy the product and probablity is **{}**".format(np.round(proba[:,0][0],2)*100))
    elif prediction == 1 : 
        st.markdown("The customer **will** buy the product and probablity is **{}**".format(np.round(proba[:,1][0],2)*100))
        
        
