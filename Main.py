import streamlit as st
from st_xatadb_connection import XataConnection

st.set_page_config(
    page_title="My personal cloud with Xata",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

xata = st.connection('xata',type=XataConnection)

st.markdown('''
<div style="background-color:#EED7F9;padding:10px;border-radius:10px;text-align:center;">
    <h1 style="color:#6C3483;font-size:1.5rem;">
    MY PERSONAL CLOUD WITH XATA
    </h1>
    <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" class="bi bi-cloud-haze2" viewBox="0 0 16 16">
        <path d="M8.5 3a4 4 0 0 0-3.8 2.745.5.5 0 1 1-.949-.313 5.002 5.002 0 0 1 9.654.595A3 3 0 0 1 13 12H4.5a.5.5 0 0 1 0-1H13a2 2 0 0 0 .001-4h-.026a.5.5 0 0 1-.5-.445A4 4 0 0 0 8.5 3M0 7.5A.5.5 0 0 1 .5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m2 2a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m-2 4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5"/>
    </svg>
</div>
''',unsafe_allow_html=True)

cols = st.columns([0.3,0.4,0.3])

with cols[1]:
    file = st.file_uploader("Upload file")

    if file is not None:
        st.write('File type: ',file.type)
