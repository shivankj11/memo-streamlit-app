import streamlit as st
import hmac
import os, time, subprocess, asyncio
from time import sleep

st.set_page_config(
    page_title="iSeed Doc Export",
    page_icon=":printer:",
)

def take_info():

    cols = st.columns([0.6, 0.4], gap='large')
    col1, col2 = cols

    #  Widgets to take the input file
    with col1:
        uploader = st.file_uploader('Upload Notion HTML Zip',
            key='file', type=['zip'], accept_multiple_files=False)
        st.button('Run', key='run', on_click=run_job)

    # Optional arguments for bash script
    with col2:
        st.write("Customization (optional)")
        st.text_input("Title of Output PDF",
            value="Company: Investment Memo", key='output title')
        st.checkbox("Cover Page?", value=True, key='cover page')
        st.text_input("Template",
            value="Deal_Memo_Standard", key='template')
    
    return cols


def load_args(data) -> str:
    s = 'notion-export-prettify '

    # save file
    local_save = 'temp_save.zip'
    with open(local_save, 'wb') as file:
        file.write(data)
    s += local_save + ' '

    # output file
    output_file = 'result_file.pdf'
    s += '-o ' + output_file + ' '

    # options
    s += '--no-heading-numbers '

    s += '--title \"' + st.session_state['output title'] + '\" '

    s += '--template \"' + st.session_state['template'] + '\" '

    if st.session_state['cover page']:
        s += '--cover-page '
    else:
        s += '--no-cover-page '

    print(s)
    return s, local_save, output_file


def run_notion_export(cmd):
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, capture_output=False)
    return proc


def run_job():
    global cols
    progress_bar = st.progress(0, text="Processing...")
    sleep(0.3)

    progress_bar.progress(10, text="Reading file")
    sleep(0.4)
    uploaded_file = st.session_state['file']
    if uploaded_file is None:
        st.error('Invalid file / No file uploaded', icon="🚨")
        progress_bar.empty()
        return False

    file = st.session_state['file'].read()

    progress_bar.progress(30, text=f"Sending :blue[file] to bash script")
    cmd, local_save, output_file = load_args(file)
    sleep(0.4)

    progress_bar.progress(50, text="Running bash script")
    res = run_notion_export(cmd)

    progress_bar.progress(80, text="Collecting results")
    sleep(0.4)

    # delete temp files and widgets
    os.remove("temp_save.zip")
    progress_bar.empty()
    st.success(f'Output file: {output_file}')
    with open(output_file, 'rb') as f:
        b = f.read()
    st.download_button(
        label="Download",
        data=b,
        file_name=output_file,
        key='download output'
    )
    cols[0].empty()


if __name__ == '__main__':
    # Headers
    logo_path = "iseed_logo.png"
    st.image(logo_path, width=250)
    st.title("iSeed Deal Memo Printer")
    st.subheader("Exported Notion HTML :arrow_right: Pretty PDF")
    st.write("")

    # Setup app
    cols = take_info()
