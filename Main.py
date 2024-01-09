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
        xata.update("files",data["id"],{"content.name": file.name})
    except Exception as e:
        xata.delete("files",data["id"])
        st.error(f"Failed to upload file: {e}")

def render_img(file: dict):
    st.image(file['content']['url'],use_column_width=True,caption=file['desc'])

def render_pdf(file: dict):
    st.markdown(f'<iframe src="{file["content"]["url"]}" width="100%" height="400"></iframe>',unsafe_allow_html=True)

def render_video(file: dict):
    video_types = ["mp4","webm","ogg"]

    if any(video_type in file['content']['mediaType'] for video_type in video_types):
        st.video(file['content']['url'],format=file['content']['mediaType'])

def render_audio(file: dict):
    audio_types = ["mp3","wav","ogg",]

    if any(audio_type in file['content']['mediaType'] for audio_type in audio_types):
        data = xata.get("files",file["id"],columns=["content.base64Content"])
        st.audio(data['content']['base64Content'],format=file['content']['mediaType'])

def render_text(file: dict):
    text_types = ["txt","csv","json","xml","html","css","js","py","java","c","cpp","cs","php","sql","sh","bat","md"]

    if any(text_type in file['content']['mediaType'] for text_type in text_types):
        data = xata.get("files",file["id"],columns=["content.base64Content"])
        st.code(data['content']['base64Content'],language=file['content']['mediaType'])

def render_file(file: dict):
    if file['content']['mediaType'] == "application/octet-stream":
        st.write("File type not supported")
    elif file['content']['mediaType'] == "application/pdf":
        render_pdf(file)
    elif file['content']['mediaType'] == "image/png" or file['content']['mediaType'] == "image/jpg" or file['content']['mediaType'] == "image/jpeg" or file['content']['mediaType'] == "image/gif" or file['content']['mediaType'] == "image/bmp" or file['content']['mediaType'] == "image/svg+xml":
        render_img(file)
    elif file['content']['mediaType'] == "video/mp4" or file['content']['mediaType'] == "video/webm" or file['content']['mediaType'] == "video/ogg":
        render_video(file)
    elif file['content']['mediaType'] == "audio/mp3" or file['content']['mediaType'] == "audio/wav" or file['content']['mediaType'] == "audio/ogg":
        render_audio(file)
    else:
        render_text(file)

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


xata.query("files")
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
    if file is not None:
        st.write('File type: ',file.type)
        st.write(file.name)
    if st.button("Upload"):
        if file is not None:
            upload_file(file,description)

if 'files' not in st.session_state:
    st.session_state.files = xata.query("files",{"page":{"size":6}})
st.write(st.session_state.files)

st.write()

st.write("Files:")

render_files(st.session_state.files['records'])
