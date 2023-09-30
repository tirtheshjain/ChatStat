import streamlit as st
# import streamlit_authenticator as stauth
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
#import streamlit_lottie as st_lottie
import requests
import json
import time as t 
import numpy as np
import pandas as pd
import dataPreprocessor
from io import StringIO

st.set_page_config(page_title="ChatStat ",page_icon=":chart:",layout="wide")
st.title(":chart: ChatStat | The WhatsApp Chat Analyzer")

st.sidebar.title("Welcome To ChatStat !")
filters = st.sidebar.multiselect(
    "Choose the filter",
    options=["Top Statistics", "Monthly Timeline","Daliy Timeline","Activity Map","Most Busy user","word cloud","Most Common words","Emoji Analysis"],
    default="Top Statistics"
)

st.markdown("##")


uploaded_file = st.file_uploader("Upload an exported '.txt' file from your WhatsApp group:")

if uploaded_file:
    df = dataPreprocessor.preprocess(uploaded_file)
    st.dataframe(df)



# --- DOWNLOAD SECTION ---

# def generate_html_download_link(fig):
#     # Credit Plotly: https://discuss.streamlit.io/t/download-plotly-plot-as-html/4426/2
#     towrite = StringIO()
#     fig.write_html(towrite, include_plotlyjs="cdn")
#     towrite = BytesIO(towrite.getvalue().encode())
#     b64 = base64.b64encode(towrite.read()).decode()
#     href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
#     return st.markdown(href, unsafe_allow_html=True)

# st.subheader('Downloads:')
# generate_html_download_link(fig)

st.markdown("##")

hide_st_style = """
    <style>
    #MainMenu {visibility : hidden;}
    header {visibility : hidden;}
    </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

footer = """
    <style>
        .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        }
    </style>
    <div class="footer"><p>Developed with ❤ </p></div>
    """
st.markdown(footer,unsafe_allow_html=True)

#spinner
with st.spinner("Just wait"):
    t.sleep(5)

st.balloons()




