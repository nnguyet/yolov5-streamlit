from io import StringIO
from pathlib import Path
import streamlit as st
import time
from detect import detect, parse_opt
import os
import sys
import argparse
from PIL import Image


def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    return max(get_subdirs(os.path.join('runs', 'detect')), key=os.path.getmtime)

if __name__ == '__main__':

    st.title('YOLOv5 Streamlit App')

    opt = parse_opt()

    # Input type select
    source = ("Image", "Video")
    source_index = st.sidebar.selectbox("Input type", range(
        len(source)), format_func=lambda x: source[x])

    # Image input
    if source_index == 0:
        uploaded_file = st.sidebar.file_uploader(
            "Upload Image", type=['png', 'jpeg', 'jpg'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Uploading...'):
                st.sidebar.image(uploaded_file)
                # Get image
                picture = Image.open(uploaded_file)
                # Save image
                picture = picture.save(f'data/images/{uploaded_file.name}')
                # Set path to parser
                opt.source = f'data/images/{uploaded_file.name}'
        else:
            is_valid = False

    # Video input
    else:
        uploaded_file = st.sidebar.file_uploader("Upload Video", type=['mp4'])
        if uploaded_file is not None:
            is_valid = True
            with st.spinner(text='Uploading...'):
                st.sidebar.video(uploaded_file)
                # Read from web and save video on server
                with open(os.path.join("data", "videos", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                # Set path to parser
                opt.source = f'data/videos/{uploaded_file.name}'
        else:
            is_valid = False

    if is_valid:
        print('Valid')
        if st.button('Detect Objects'):
            with st.spinner(text='Detecing...'):
                detect(**vars(opt))

            st.success('Successful!')

            if source_index == 0:
                with st.spinner(text='Preparing Images'):
                    for img in os.listdir(get_detection_folder()):
                        st.image(str(Path(f'{get_detection_folder()}') / img))

            else:
                with st.spinner(text='Preparing Video'):
                    for vid in os.listdir(get_detection_folder()):
                        st.video(open(str(Path(f'{get_detection_folder()}') / vid), 'rb').read())
