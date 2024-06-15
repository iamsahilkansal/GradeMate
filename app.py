import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import pandas as pd
import math

with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options = ["Home", "GPA Calculation", "CGPA Calculation", "GPA for 9", "Analysis"],
        icons = ["house", "calculator", "graph-up", "star", "bar-chart"],
        menu_icon = "border-width",
        default_index=0,
    )

if(selected == "Home"):
    st.title("Welcome to GradeMate")

    st.write("""
        This application helps you easily calculate and analyze your GPA and CGPA.
        Use the menu on the left to navigate through different features:
        - **GPA Calculation**: Calculate your GPA for a single semester.
        - **CGPA Calculation**: Calculate your Cumulative GPA.
        - **GPA for being 9 pointer**: Find out the GPA required to become a 9-pointer.
        - **Analysis**: Graphically analyze your semester-wise GPA and CGPA.
    """)

    st.subheader("Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Calculate GPA")
    with col2:
        st.button("Calculate CGPA")
    with col3:
        st.button("GPA for 9")
    with col4:
        st.button("Analysis")
    
    st.write("Made with ❤️ by Sahil Kansal")

if(selected == "GPA Calculation"):
    st.title(f"{selected}")
    grade_dict = {'S': 10, 'A': 9, 'B': 8, 'C': 7, 'D': 6, 'E': 5, 'F': 0}
    col1, col2 = st.columns(2)
    with col1:
        st.write("Enter the Number of Subjects")
    with col2:
        n = st.number_input("", min_value=0, step=1, value=0)
    
    data = []
    for i in range(n):
        col1, col2 = st.columns(2)
        with col1:
            temp_credit = st.number_input(f"Enter the credit for Subject {i + 1}", min_value=0.0, step=0.5, value=0.0)
        with col2:
            grade = st.selectbox(f'Select the grade for Subject {i + 1}', ('S', 'A', 'B', 'C', 'D', 'E', 'F'))
            temp_grade = grade_dict[grade]
        data.append({"credit": temp_credit, "grade": temp_grade})
    
    total_credits = sum(item["credit"] for item in data)
    if st.button("Calculate GPA") and n > 0 and total_credits>0:
        temp_sum = sum(item["credit"] * item["grade"] for item in data)
        gpa = round(temp_sum / total_credits, 2)
        st.write("The GPA is: ", gpa)
    else:
        st.warning("Select Correct Number of Subjects and Credits", icon="⚠️")


if(selected == "CGPA Calculation"):
    st.title(f"{selected}")
    col1, col2= st.columns(2)
    with col1:
        completed = st.number_input("Total Credits Completed", min_value=0.0, step=0.5, value=0.0)
    with col2:
        cg = st.number_input("Current CGPA", min_value=0.0, max_value=10.0, step=0.5, value=0.0)
    
    col1, col2= st.columns(2)
    with col1:
        sem = st.number_input("Credits Completed this semester", min_value=0.0, step=0.5, value=0.0)
    with col2:
        g = st.number_input("This Semester GPA", min_value=0.0, step=0.5, value=0.0)
    
    if(completed+sem>0):
        st.write("New CGPA is: ", round((completed*cg +sem*g)/(completed+sem), 2))
    else:
        st.warning("Select Correct Number of Credits", icon="⚠️")

if(selected == "GPA for 9"):
    st.title(f"GPA required for being 9 pointer")
    col1, col2, col3= st.columns(3)
    with col1:
        completed = st.number_input("Total Credits Completed", min_value=0.0, step=0.5, value=0.0)
    with col2:
        cg = st.number_input("Current CGPA", min_value=0.0, max_value=10.0, step=0.5, value=0.0)
    with col3:
        sem = st.number_input("Credits Opted this semester", min_value=0.0, step=0.5, value=0.0)
    if(sem>0):
        ans=(9.00*(completed+sem)-completed*cg)/sem
        st.write("GPA Required to be 9 pointer is: ", round(ans, 2))
    else:
        st.warning("Select Correct Number of Credits", icon="⚠️")


if(selected == "Analysis"):
    st.title(f"{selected}")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Enter the Number of Semesters Completed")
    with col2:
        n = st.number_input("", min_value=0, max_value=8, step=1, value=0)
    
    credits=[]
    gpa=[]
    cgpa=[]
    total=[]
    def cal_cgpa(prev_cgpa, credits_completed, current_gpa, current_credits):
        ans=(prev_cgpa*credits_completed + current_gpa*current_credits)/(current_credits+credits_completed)
        return round(ans, 2)
    
    for i in range(n):
        col1, col2 = st.columns(2)
        with col1:
            temp_credit = st.number_input(f"Number of credit completed in Semester {i + 1}", min_value=0.0, step=0.5, value=0.0)
            credits.append(temp_credit)
        with col2:
            temp_gpa = st.number_input(f"Enter the gpa for Semester {i + 1}", min_value=0.0, step=0.5, max_value=10.0, value=0.0)
            gpa.append(temp_gpa)
        
        if(temp_credit>0):
            if(i==0):
                total.append(temp_credit)
                cgpa.append(temp_gpa)
            else:
                total.append(temp_credit+total[i-1])
                cgpa.append(cal_cgpa(cgpa[i-1], total[i-1], temp_gpa, temp_credit))
        else:
            st.warning("Select Correct Number of Credits", icon="⚠️")
    type = st.selectbox("Select the analysis type", ("Sem-GPA Analysis", "Sem-CGPA Analysis"))    

    if st.button("Analyse"):
        if(type=="Sem-GPA Analysis"):
            data = {"Semester": ["Semester " + str(i + 1) for i in range(n)], "GPA": gpa}
            df = pd.DataFrame(data)

            fig = px.line(df, x='Semester', y='GPA', markers=True, title='GPA Analysis')
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(range=[math.floor(min(gpa)), 10])
            
        elif(type=="Sem-CGPA Analysis"):
            data = {"Semester": ["Semester " + str(i + 1) for i in range(n)], "CGPA": cgpa}
            df = pd.DataFrame(data)

            fig = px.line(df, x='Semester', y='CGPA', markers=True, title='CGPA Analysis')
            fig.update_xaxes(tickangle=45)
            fig.update_yaxes(range=[math.floor(min(cgpa)), 10])
        
        st.plotly_chart(fig)
        

        
