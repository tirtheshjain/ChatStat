import streamlit as st
import matplotlib.pyplot as plt
# import streamlit_authenticator as stauth
#import streamlit_lottie as st_lottie
import requests
import json
import time as t 
import numpy as np
import pandas as pd
import dataPreprocessor, utils
import math
import datetime

st.set_page_config(page_title="ChatStat ",page_icon=":chart:",layout="wide")
st.title(":chart: ChatStat | The WhatsApp Chat Analyzer")

# ---- SIDEBAR ----
st.sidebar.title("Welcome To ChatStat !")
st.sidebar.subheader("Filters")
analysis_filter = st.sidebar.multiselect(
    "Analysis",
    options=["Top Statistics","Daily Timeline","Activity Map","User Who Chats the Most","Word Cloud","Most Common words","Emoji Analysis","Sentiment Analysis"],
    default="Top Statistics"
)


# ---- UPLOAD SECTION ----
st.markdown("##")
st.text("WhatsApp > Chat > Three dots > More > Export chat > Without media > Send or save the exported .txt file to your device.")
uploaded_file = st.file_uploader("Upload a WhatsApp Chat Exported (*.txt) File to Get Insights:")

if uploaded_file:
    df = dataPreprocessor.preprocess(uploaded_file)
    st.dataframe(df)

    user_list = df['User'].unique().tolist()
    user_list.insert(0,"All")
    selected_user = st.sidebar.selectbox("User",user_list)

    if st.button("Show Analysis"):
        figures = []    #list of all plots generated
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

        # User Who Chats the Most Area
        if "User Who Chats the Most" in analysis_filter:
            # finding the User Who Chats the Most (group level)
            if selected_user == 'All':
                st.title('User Who Chats the Most')
                top_user_sr, top_users_contribution_df = utils.most_chat_users(df)
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    ax.bar(top_user_sr.index, top_user_sr.values,color='#25d366')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                    figures.append(fig)
                with col2:
                    st.dataframe(top_users_contribution_df)
            else:
                # Display a warning message for the case when the selected user is not 'All'
                st.warning(f"Warning: You've selected a specific user: {selected_user}. Please note that 'User Who Chats the Most' analysis is for all users.")
             
            st.markdown("##")
                
        # emoji analysis Area
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
                figures.append(fig)
            with col2: 
                st.dataframe(emojis_freq_df)
            st.markdown("##")

        # daily timeline area
        if "Daily Timeline" in analysis_filter:
            st.title("Daily Timeline (Last 15 days)")
            daily_timeline = utils.get_daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['Date'].tail(15), daily_timeline['Message'].tail(15), color='#25d366')
            ax.set_xlabel('Date')
            ax.set_ylabel('Message Count')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            figures.append(fig)
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
                figures.append(fig)

            with col2:
                st.header("Top messaging months")
                active_month_sr = utils.get_month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(active_month_sr.index, active_month_sr.values,color='#25d366')
                ax.set_xlabel('Month name')
                ax.set_ylabel('Message Count')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                figures.append(fig)

            st.markdown("##")

        #WordClouds Area
        if "Word Cloud" in analysis_filter:
            st.title("Word Cloud")
            wc = utils.generate_wordcloud(selected_user, df)
            
            fig, ax = plt.subplots()
            
            # Remove the axis and tick labels
            ax.set_axis_off()

            # Display the word cloud
            ax.imshow(wc)

            # Plot the word cloud in Streamlit
            st.pyplot(fig)
            figures.append(fig)
            st.markdown("##")

        # ---- DOWNLOAD SECTION Area ----
        st.subheader('Downloads:')
        links = utils.generate_html_download_link(figures)
        downloads = "<p>"
        for href in links:
            downloads += href 
        downloads += "</p>"
        st.markdown(downloads, unsafe_allow_html=True)
        st.markdown("##")


#---- Footer Area----

hide_st_style = """
    <style>
    #MainMenu {visibility : hidden;}
    header {visibility : hidden;}
    </style>
"""
st.markdown(hide_st_style,unsafe_allow_html=True)

# Get the current date and time
now = datetime.datetime.now()

# Format the copyright information
copyright = f"&copy; {now.year} ChatStat"

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
    <footer class="footer">
        🔒Everything is processed in your browser. No data leaves your device.</br>
        """+ copyright +""".
        Developed with ❤ by Tirthesh Jain & Aditya Tomar
    </footer>
    """
st.markdown(footer,unsafe_allow_html=True)





