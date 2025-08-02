# -*- coding: utf-8 -*-
"""
Student Skill Portfolio Dashboard v2.0 - Stylish Version
"""
import streamlit as st
import datetime
import pandas as pd
import plotly.express as px

# -------------------- SETUP --------------------
st.set_page_config(page_title="Student Portfolio Dashboard", layout="wide")

# Initialize session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False
if "student_data" not in st.session_state:
    st.session_state.student_data = []

# # -------------------- DARK MODE TOGGLE --------------------
st.session_state.dark_mode = st.toggle("Light Mode 🌙")
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; color: white; }
        </style>
    """, unsafe_allow_html=True)
    

# # -------------------- HEADER --------------------
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>📘 Student Portfolio Dashboard</h1>
    <h4 style='text-align: center;'>Build your professional profile interactively!</h4>
    <hr>
""", unsafe_allow_html=True)   #some time streamlit ignore the html code...so for safety reason we use this line

# # -------------------- SIDEBAR PROFILE INPUT --------------------
st.sidebar.header("👤 Your Profile")
name = st.sidebar.text_input("Full Name")
dob = st.sidebar.date_input("Date of Birth", datetime.date(2000, 1, 1))
bio = st.sidebar.text_area("Short Bio")
photo = st.sidebar.file_uploader("Upload Profile Photo", type=["png", "jpg"])

# # -------------------- MAIN TABS --------------------
tab1, tab2, tab3, tab4 = st.tabs(["📚 Skills", "📂 Projects", "🏅 Certifications", "📊 Summary"])

# # -------------------- SKILLS TAB --------------------
with tab1:
    st.subheader("Your Skills")
    skills = st.multiselect("Select Skills", ["Python", "Java", "C++", "HTML", "CSS", "JavaScript", "SQL","Node js"])
    exp_data = {}
    for skill in skills:
        level = st.slider(f"{skill} Proficiency (0-10)", 0, 10, 5, key=skill)
        exp_data[skill] = level

#     # Skill Chart
    if exp_data:
        chart_data = pd.DataFrame({"Skill": list(exp_data.keys()), "Level": list(exp_data.values())})
        fig = px.bar(chart_data, x="Skill", y="Level", title="Skill Proficiency Chart", color="Skill")
        st.plotly_chart(fig)

# # -------------------- PROJECTS TAB --------------------
with tab2:
    st.subheader("Project Details")
    project_title = st.text_input("Project Title")
    project_desc = st.text_area("Project Description")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Project Length (words)", len(project_desc.split()))
    with col2:
        st.metric("Title Length", len(project_title))

# # -------------------- CERTIFICATIONS TAB --------------------
with tab3:
    st.subheader("Upload Certification")
    cert_file = st.file_uploader("Upload Certificate (PDF or Image)", type=["pdf", "png", "jpg"])
    if cert_file:
        if cert_file.type.startswith("image"):
            st.image(cert_file, width=300)
        else:
            st.success(f"Uploaded: {cert_file.name}")

# # -------------------- SUMMARY TAB --------------------
with tab4:
    st.subheader("🎓 Profile Summary")
    col1, col2 = st.columns([1,2])

    with col1:
        if photo:
            st.image(photo, width=150)
    
    with col2:
        st.markdown(f"### {name}")
        st.write(f"**DOB:** {dob}")
        st.write(f"**Bio:** {bio}")

    st.markdown("---")
    st.write("### 🛠 Skills")
    for skill, lvl in exp_data.items():
        st.progress(lvl / 10.0, text=f"{skill}: {lvl}/10")

    st.markdown("---")
    st.write("### 💼 Project")
    st.markdown(f"**{project_title}**")
    st.write(project_desc)

    if cert_file:
        st.markdown("---")
        st.write("### 🏅 Certificate Preview")
        st.write(cert_file.name)

# # -------------------- SAVE BUTTON --------------------
if st.button("💾 Save Profile"):
    profile = {
        "Name": name,
        "DOB": str(dob),
        "Bio": bio,
        "Skills": exp_data,
        "Project Title": project_title,
        "Project Desc": project_desc,
        "Certificate": cert_file.name if cert_file else "None"
    }
    st.session_state.student_data.append(profile)
    st.success("✅ Profile saved successfully!")

# # -------------------- VIEW ALL SAVED --------------------
if st.checkbox("📁 Show All Saved Profiles"):
    st.write(pd.DataFrame(st.session_state.student_data))
