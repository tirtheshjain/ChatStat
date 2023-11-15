import streamlit as st
import matplotlib.pyplot as plt
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
    options=["Top Statistics", "Most Mentioned (Tagged) User","Daily Timeline","Activity Map","User Who Chats the Most","Word Cloud","Emoji Usage Analysis","Sentiment Analysis"],
    default="Top Statistics"
)


# ---- UPLOAD SECTION ----
st.markdown("##")
st.write(":point_right: WhatsApp > Chat > Three dots > More > Export chat > Without media > Send or save the exported .txt file to your device.")
uploaded_file = st.file_uploader(":file_folder: Upload a WhatsApp Chat Exported (*.txt) File to Get Insights:",type=["txt"])

if uploaded_file:
    df = dataPreprocessor.preprocess(uploaded_file)
    
    with st.expander("Processed WhatsApp Chat Data"):
        st.dataframe(df)

    # ---- SIDEBAR ----
    user_list = df['User'].unique().tolist()
    user_list.insert(0,"All")
    selected_user = st.sidebar.selectbox("User",user_list)


    if st.button("Show Analysis"):
        plot_data = []    # list containing tuples of names and corresponding figure of all plots generated

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


        # Most tagged user analysis area
        if "Most Mentioned (Tagged) User" in analysis_filter:
            # finding the User Who got mentioned the Most (group level)
            if selected_user == 'All':
                most_tagged_user_df = utils.most_tagged_users(df)
                st.title("Most Mentioned (Tagged) User")
                if not most_tagged_user_df.empty:
                    fig, ax = plt.subplots()
                    ax.barh(most_tagged_user_df['Tagged Users'], most_tagged_user_df['Frequency'], color='#25d366')
                    ax.set_ylabel('Tagged User')
                    ax.set_xlabel('Frequency')
                    ax.set_title('Tagged Users Frequency')
                    st.pyplot(fig)
                    # Append the figure and a corresponding name to the plot_data list
                    plot_data.append(("MostMentionedUsers", fig))
                else:
                    st.info("No user has been tagged in the group.")
            else:
                # Display a warning message for the case when the selected user is not 'All'
                st.warning(f"Warning: You've selected a specific user: {selected_user}. Please note that 'Most Mentioned (Tagged) User' analysis is for all users.")
             
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
                    ax.set_xlabel('User')
                    ax.set_ylabel('Message Count')
                    ax.set_title('Top Users by Message Count')
                    st.pyplot(fig)
                    # Append the figure and a corresponding name to the plot_data list
                    plot_data.append(("UserWhoChatsTheMost", fig))
                with col2:
                    st.dataframe(top_users_contribution_df)
            else:
                # Display a warning message for the case when the selected user is not 'All'
                st.warning(f"Warning: You've selected a specific user: {selected_user}. Please note that 'User Who Chats the Most' analysis is for all users.")
             
            st.markdown("##")


        # emoji usage analysis Area
        if "Emoji Usage Analysis" in analysis_filter:
            emojis_freq_df = utils.emoji_analysis(selected_user,df)
            st.title("Emoji Usage Analysis")
            if not emojis_freq_df.empty:
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    emoji_x = []
                    for idx in range(len(emojis_freq_df["Frequency"].head())):
                        emoji_x.append('Emoji '+str(idx))
                    ax.bar(emoji_x,emojis_freq_df["Frequency"].head(),color='#25d366')
                    ax.set_xlabel('Emoji')
                    ax.set_ylabel('Frequency')
                    ax.set_title("Top Emojis by Usage Frequency")
                    st.pyplot(fig)
                    # Append the figure and a corresponding name to the plot_data list
                    plot_data.append(("EmojiUsageAnalysis", fig))
                with col2: 
                    st.dataframe(emojis_freq_df)
            else:
                st.info("No Emoji has been shared.")
            st.markdown("##")


        # Check if "Daily Timeline" is selected in the analysis_filter
        if "Daily Timeline" in analysis_filter:
            # Display the title for the Daily Timeline section
            st.title("Daily Timeline (Last 15 days)")
            
            # Get the daily timeline data using the utils module
            daily_timeline = utils.get_daily_timeline(selected_user, df).to_numpy()
            
            # Create a subplot for the plot
            fig, ax = plt.subplots()
            
            # Extract the last 15 days' data for plotting
            dates = []
            msg_count = []
            for i in range(len(daily_timeline) - 15, len(daily_timeline)):
                dates.append(daily_timeline[i][0])
                msg_count.append(daily_timeline[i][1])
            
            # Plot the data
            ax.plot(dates, msg_count, color='#25d366')
            
            # Set labels and title for the plot
            ax.set_xlabel('Date')
            ax.set_ylabel('Message Count')
            ax.set_title('Message Count Over Date')
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation='vertical')
            
            # Set the height of the plot
            fig.set_figheight(3)  # Set height in inches
            
            # Display the plot using Streamlit
            st.pyplot(fig)
            
            # Append the figure and a corresponding name to the plot_data list
            plot_data.append(("DailyTimeline", fig))
            
            # Add a markdown separator
            st.markdown("##")



        # Activity map Area
        if "Activity Map" in analysis_filter:
            st.title('Activity Map')
            col1,col2 = st.columns(2)

            with col1:
                active_day_sr = utils.get_week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(active_day_sr.index,active_day_sr.values,color='#25d366')
                ax.set_xlabel('Days of the week')
                ax.set_ylabel('Message Count')
                ax.set_title('Top messaging days')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                plot_data.append(("TopMessagingDays", fig))

            with col2:
                active_month_sr = utils.get_month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(active_month_sr.index, active_month_sr.values,color='#25d366')
                ax.set_xlabel('Month name')
                ax.set_ylabel('Message Count')
                ax.set_title('Top messaging months')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                plot_data.append(("TopMessagingMonths", fig))

            # Activity heatmap
            day_hour_heatmap = utils.get_day_hour_heatmap(selected_user, df)
            title = 'Day vs. Hour Activity Heatmap'
            fig, ax = plt.subplots()
            cax = ax.matshow(day_hour_heatmap, cmap='YlGnBu')  # Using a blue-green colormap
            fig.set_figheight(3)  # Set height in inches

            # Set ticks and labels
            plt.xticks(range(len(day_hour_heatmap.columns)), day_hour_heatmap.columns)
            plt.yticks(range(len(day_hour_heatmap.index)), day_hour_heatmap.index)  
            plt.gca().xaxis.set_tick_params(which='both', bottom=False)

            # Add color bar
            cbar = fig.colorbar(cax)
            cbar.set_label('Message Count')

            # Set the title
            ax.set_title("Day vs. Hour Activity Heatmap")

            st.pyplot(fig)
            plot_data.append(("DayHourActivityHeatmap", fig))

            st.markdown("##")


        # WordClouds Area
        if "Word Cloud" in analysis_filter:
            st.title("Word Cloud")
            col1,col2 = st.columns(2)
            wc,most_common_word_df = utils.generate_wordcloud(selected_user, df)
            
            if wc is not None:
                with col1:
                    fig, ax = plt.subplots()
                    # Remove the axis and tick labels
                    ax.set_axis_off()
                    # Display the word cloud
                    ax.imshow(wc)
                    # Plot the word cloud in Streamlit
                    st.pyplot(fig)
                    plot_data.append(("WordCloud", fig))
                
                with col2:
                    st.dataframe(most_common_word_df)
            else:
                st.warning("Insufficient chat text for creating a meaningful word cloud.")

            st.markdown("##")

        
        # -----Sentiment analysis Area------------------
        if "Sentiment Analysis" in analysis_filter:
            st.title("Sentiment Analysis")
            col1, col2 = st.columns(2)

            with col1:
                positive, negative, neutral = utils.sentiment_analysis(selected_user, df)

                labels = ['Positive', 'Negative', 'Neutral']
                data = [positive, negative, neutral]

                # Create a donut chart
                fig, ax = plt.subplots()
                ax.pie(data, startangle=90, wedgeprops=dict(width=0.4), autopct='%.1f%%', textprops={'rotation': 90})
                ax.axis('equal')

                # Add a circle in the center to create a donut hole
                center_circle = plt.Circle((0, 0), 0.70, fc='white')
                fig.gca().add_artist(center_circle)

                # Display the legends
                plt.legend(labels, loc='best')

                st.pyplot(fig)
                plot_data.append(("SentimentAnalysis", fig))

            with col2:
                if selected_user == 'All':
                    # Get the sentiment contributors
                    contributors = utils.user_sentiment_contributors(df)

                    # Display the most positive, negative, and neutral contributors
                    st.write("Most Positive Chat Contributor:", contributors['Most Positive User'])
                    st.write("Most Negative Chat Contributor:", contributors['Most Negative User'])
                    st.write("Most Neutral Chat Contributor:", contributors['Most Neutral User'])
                    
            st.markdown("##")

            

        # ---- DOWNLOAD SECTION Area ----
        if plot_data:
            all_plots_zip_data = utils.generate_all_plots_zip(plot_data)
    
            # Define button CSS
            button_style = """
                background-color: #25D366;
                color: #fff;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
            """

            st.markdown(f'<a href="data:file/zip;base64,{all_plots_zip_data}" download="all_plots.zip"><button style="{button_style}">Download All Plots</button></a>', unsafe_allow_html=True)

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
        \U0001F512  We do not share or store your data beyond the scope of this application.<br>
        """+ copyright +""".
        Developed with \U00002764 by Tirthesh Jain & Aditya Tomar
    </footer>
    """
st.markdown(footer,unsafe_allow_html=True)





