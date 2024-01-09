import streamlit as st
import pandas as pd
from st_xatadb_connection import XataConnection

# Set page config
st.set_page_config(
    page_title="My personal cloud with Xata",
    page_icon="🌩️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


xata = st.connection('xata',type=XataConnection)# Set Xata connection


def upload_file(file,description: str=""): # This Uploads a file to Xata
    try:
        if 'text' not in file.type:
            data = xata.insert("files",{"desc": description}) # Create file
        else: # If file is text
            content = file.read().decode("utf-8") # Read file
            data = xata.insert("files",{"desc": description,
            "text_file": content, "text_file_type": file.type, "text_file_name": file.name}) #Store file in text field type
    except Exception as e:
        st.error(f"Failed to create file: {e}")

    try:
        if 'text' not in file.type:
            xata.upload_file("files",data["id"],"content",file.read(),content_type=file.type) # Upload file
            xata.update("files",data["id"],{"content.name": file.name})
    except Exception as e:
        xata.delete("files",data["id"]) # Delete file if upload fails
        st.error(f"Failed to upload file: {e}")

    st.success("File uploaded successfully")

def render_img(file: dict):
    st.image(file['content']['url'],use_column_width=True,caption=file['desc'])
    st.download_button("Download",file['content']['url'],file['content']['name'],file['content']['mediaType'])

def render_pdf(file: dict):
    st.markdown(f'<iframe src="{file["content"]["url"]}" width="100%" height="400"></iframe>',unsafe_allow_html=True)
    st.caption(file['desc'])

def render_video(file: dict):
    st.video(file['content']['url'],format=file['content']['mediaType'])
    st.caption(file['desc'])
    st.download_button("Download",file['content']['url'],file['content']['name'],file['content']['mediaType'])

def render_audio(file: dict):
    st.audio(file['content']['url'],format=file['content']['mediaType'])
    st.caption(file['desc'])
    st.download_button("Download",file['content']['url'],file['content']['name'],file['content']['mediaType'])

def render_text(file: dict):
    with st.expander("View text"):
        st.code(file['text_file'],language=file['text_file_type'].split('/')[1])
    st.caption(file['desc'])
    st.download_button("Download",file['text_file'],file['text_file_name'],file['text_file_type'])

def render_dataframe(file: dict):
    try:
        st.dataframe(pd.read_csv(file['content']['url']),use_container_width=True)
    except Exception as e:
        st.dataframe(pd.read_excel(file['content']['url']),use_container_width=True)
        print(e)

    st.caption(file['desc'])
    st.download_button("Download",file['content']['url'],file['content']['name'],file['content']['mediaType'])

def render_file(file: dict):
    try:

        if "text_file" in file and file['text_file'] is not None:
            st.write(file['text_file_name'])
            render_text(file)
        elif file['content']['mediaType'] == "application/pdf":
            st.write(file['content']['name'])
            render_pdf(file)
        elif file['content']['mediaType'] == "image/png" or file['content']['mediaType'] == "image/jpg" or file['content']['mediaType'] == "image/jpeg" or file['content']['mediaType'] == "image/gif" or file['content']['mediaType'] == "image/bmp" or file['content']['mediaType'] == "image/svg+xml" or file['content']['mediaType'] == "image/webp":
            st.write(file['content']['name'])
            render_img(file)
        elif file['content']['mediaType'] == "video/mp4" or file['content']['mediaType'] == "video/webm" or file['content']['mediaType'] == "video/ogg":
            st.write(file['content']['name'])
            render_video(file)
        elif file['content']['mediaType'] == "audio/mp3" or file['content']['mediaType'] == "audio/wav" or file['content']['mediaType'] == "audio/ogg" or "audio/mpeg" in file['content']['mediaType']:
            st.write(file['content']['name'])
            render_audio(file)
        elif file['content']['mediaType'] == "text/csv" or file['content']['mediaType'] == "application/vnd.ms-excel" or file['content']['mediaType'] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            st.write(file['content']['name'])
            render_dataframe(file)
        else:
            st.write("File type not supported yet :(")
            st.download_button("Download",file['content']['url'],file['content']['name'],file['content']['mediaType'])
    except Exception as e:
        st.error("Failed to render file")
        print(e)

def render_files(files: list):
    cols = st.columns(3)
    st.divider()
    cols1 = st.columns(3)
    if len(files)  > 0:
        with cols[0]:
            render_file(files[0])
    if len(files)  > 1:
        with cols[1]:
            render_file(files[1])
    if len(files)  > 2:
        with cols[2]:
            render_file(files[2])
    if len(files)  > 3:
        with cols1[0]:
            render_file(files[3])
    if len(files)  > 4:
        with cols1[1]:
            render_file(files[4])
    if len(files)  > 5:
        with cols1[2]:
            render_file(files[5])

def app():
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
        if st.checkbox("Add description"):
            description = st.text_area("Description")
        else:
            description = ""
        if file is not None:
            st.write('File type: ',file.type)
            st.write(file.name)
        if st.button("Upload"):
            if file is not None:
                upload_file(file,description)

    if 'files' not in st.session_state or st.session_state.files is None:
        st.session_state.files = [xata.query("files",{"page":{"size":6},"sort":{"xata.createdAt":"desc"}})]

    if 'page' not in st.session_state:
        st.session_state.page = 0

    colsr = st.columns([0.9,0.1])
    if colsr[1].button("🔄",use_container_width=True):
        st.session_state.files= [xata.query("files",{"page":{"size":6},"sort":{"xata.createdAt":"desc"}})]
        st.session_state.page = 0
        st.rerun()

    st.subheader("My files")
    st.divider()
    render_files(st.session_state.files[st.session_state.page]['records'])

    colsp = st.columns([0.8,0.1,0.1])

    if colsp[1].button("⏮️",use_container_width=True):
        if st.session_state.page > 0:
            st.session_state.page -= 1
        st.rerun()

    if colsp[2].button("⏭️",use_container_width=True):
        if len(st.session_state.files) > st.session_state.page+1:
            st.session_state.page += 1
        else:
            st.session_state.files.append(xata.next_page("files",st.session_state.files[st.session_state.page],pagesize=6))
            st.session_state.page += 1
            if st.session_state.files[st.session_state.page] is None:
                del st.session_state.files[st.session_state.page]
                st.session_state.page = 0
        st.rerun()

if __name__ == "__main__":
    app()
    st.divider()
    st.caption("Made with ❤️ by Sergio Lopez Martinez")
