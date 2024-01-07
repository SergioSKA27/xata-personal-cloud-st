import streamlit as st
from st_xatadb_connection import XataConnection

st.set_page_config(
    page_title="My personal cloud with Xata",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

xata = st.connection('xata',type=XataConnection)

def upload_file(file,description):
    try:
        data = xata.insert("files",{"desc": description})
    except Exception as e:
        st.error(f"Failed to create file: {e}")

    try:
        xata.upload_file("files",data["id"],"content",file.read(),content_type=file.type)
    except Exception as e:
        xata.delete("files",data["id"])
        st.error(f"Failed to upload file: {e}")

def render_img(file):
    img_types = ["png","jpg","jpeg","gif","bmp","svg"]

    if file["content"]["type"] in img_types:
        st.image(file["content"]["url"])



st.markdown('''
<div style="background-color:#EED7F9;padding:10px;border-radius:10px;text-align:center;">
    <h1 style="color:#6C3483;font-size:1.5rem;">
    MY PERSONAL CLOUD WITH XATA
    </h1>
    <svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" fill="currentColor" class="bi bi-cloud-haze2" viewBox="0 0 16 16">
        <path d="M8.5 3a4 4 0 0 0-3.8 2.745.5.5 0 1 1-.949-.313 5.002 5.002 0 0 1 9.654.595A3 3 0 0 1 13 12H4.5a.5.5 0 0 1 0-1H13a2 2 0 0 0 .001-4h-.026a.5.5 0 0 1-.5-.445A4 4 0 0 0 8.5 3M0 7.5A.5.5 0 0 1 .5 7h5a.5.5 0 0 1 0 1h-5a.5.5 0 0 1-.5-.5m2 2a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5m-2 4a.5.5 0 0 1 .5-.5h9a.5.5 0 0 1 0 1h-9a.5.5 0 0 1-.5-.5"/>
    </svg>
</div>
''',unsafe_allow_html=True)

cols = st.columns([0.3,0.4,0.3])

with cols[1]:
    file = st.file_uploader("Upload file")
    description = st.text_area("Description")

    if st.button("Upload"):
        if file is not None:
            st.write('File type: ',file.type)
            st.write(file.name)
            upload_file(file,description)



st.write(xata.query("files"))
