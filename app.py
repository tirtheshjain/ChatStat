import streamlit as st
import matplotlib.pyplot as plt
# import streamlit_authenticator as stauth
import base64  # Standard Python Module
from io import StringIO, BytesIO  # Standard Python Module
#import streamlit_lottie as st_lottie
import requests
import json
import time as t 
import numpy as np
import pandas as pd
import dataPreprocessor, utils
import math

st.set_page_config(page_title="ChatStat ",page_icon=":chart:",layout="wide")
st.title(":chart: ChatStat | The WhatsApp Chat Analyzer")

# ---- SIDEBAR ----
st.sidebar.title("Welcome To ChatStat !")
st.sidebar.subheader("Filters")
analysis_filter = st.sidebar.multiselect(
    "Analysis",
    options=["Top Statistics","Daliy Timeline","Activity Map","Most Active Users","Word Cloud","Most Common words","Emoji Analysis","Sentiment Analysis"],
    default="Top Statistics"
)


# ---- UPLOAD SECTION ----
st.markdown("##")
st.text("WhatsApp > Chat > Three dots > More > Export chat > Without media > Send or save the exported .txt file to your device.")
uploaded_file = st.file_uploader("Upload a WhatsApp export '.TXT' file:")

if uploaded_file:
    df = dataPreprocessor.preprocess(uploaded_file)
    st.dataframe(df)

    user_list = df['User'].unique().tolist()
    user_list.insert(0,"All")
    selected_user = st.sidebar.selectbox("User",user_list)

    if st.button("Show Analysis"):
        # Top Stats Area
        if "Top Statistics" in analysis_filter:
            message_count, words_count, media_count, links_count, emojis_count = utils.top_stats(selected_user,df)
            st.title("Top Statistics")
            col1, col2, col3 = st.columns(3)
            col4, col5, col6 = st.columns(3)

            with col1:
                st.header("Total Messages")
                st.title(message_count)
            with col2:
                st.header("Total Words")
                st.title(words_count)
            with col3:
                st.header("Average Words per Message")
                st.title(math.ceil(words_count/message_count))
            with col4:
                st.header("Media Shared")
                st.title(media_count)
            with col5:
                st.header("Links Shared")
                st.title(links_count)
            with col6:
                st.header("Emojis Shared")
                st.title(emojis_count)
            st.markdown("##")

        # Most Active Users Area
        if "Most Active Users" in analysis_filter:
            # finding the busiest users in the group(Group level)
            if selected_user == 'All':
                st.title('Most Active Users')
                top_user_sr, top_users_contribution_df = utils.most_active_users(df)
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.pie(top_user_sr.values,labels=top_user_sr.index, autopct="%0.2f")
                    st.pyplot(fig)
                with col2:
                    st.dataframe(top_users_contribution_df)
            else:
                # Display a warning message for the case when the selected user is not 'All'
                st.warning(f"Warning: You've selected a specific user: {selected_user}. Please note that 'Most Active User' analysis is for all users.")
            st.markdown("##")
                
        # emoji analysis
        if "Emoji Analysis" in analysis_filter:
            emojis_freq_df = utils.emoji_analysis(selected_user,df)
            st.title("Emoji Analysis")

            col1,col2 = st.columns(2)

            with col1:
                fig, ax = plt.subplots()
                ax.bar(emojis_freq_df["Emoji"].head(),emojis_freq_df["Frequency"].head(),color='#25d366')
                ax.set_xlabel('Emoji')
                ax.set_ylabel('Frequency')
                st.pyplot(fig)
            with col2: 
                st.dataframe(emojis_freq_df)
            st.markdown("##")

        # daily timeline area
        if "Daliy Timeline" in analysis_filter:
            st.title("Daily Timeline")
            daily_timeline = utils.get_daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['Date'].tail(30), daily_timeline['Message'].tail(30), color='#25d366')
            ax.set_xlabel('Date')
            ax.set_ylabel('Message Count')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            st.markdown("##")

        # activity map Area
        if "Activity Map" in analysis_filter:
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                st.header("Top messaging days")
                active_day_sr = utils.get_week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(active_day_sr.index,active_day_sr.values,color='#25d366')
                ax.set_xlabel('Days of the week')
                ax.set_ylabel('Message Count')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.header("Top messaging months")
                active_month_sr = utils.get_month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(active_month_sr.index, active_month_sr.values,color='#25d366')
                ax.set_xlabel('Month name')
                ax.set_ylabel('Message Count')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            st.markdown("##")

        #WordClouds
        if "Word Cloud" in analysis_filter:
            st.title("Word Cloud")
            wc = utils.generate_wordcloud(selected_user,df)
            fig, ax = plt.subplots()
            # Clear x-axis and y-axis tick labels
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.imshow(wc)
            st.pyplot(fig)
            st.markdown("##")
            

        #---- DOWNLOAD SECTION ----

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
    <div class="footer">
        <p>&copy; 2023 ChatStat</p>
        <p>Developed with ❤ by Tirthesh Jain & Aditya Tomar</p>
    </div>
    """
st.markdown(footer,unsafe_allow_html=True)

# #spinner
# with st.spinner("Just wait"):
#     t.sleep(5)

# st.balloons()




