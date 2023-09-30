import pandas as pd
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud

def top_stats(selected_user, df):
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Fetch the number of messages
    message_count = df.shape[0]

    # Combine all messages into a single string for word count and emoji count
    all_messages = ' '.join(df['Message'].astype(str))

    # Fetch the total number of words
    words_list = all_messages.split()
    words_count = len(words_list)

    # Fetch the number of media messages
    media_count = df[df['Message'] == '<Media omitted>'].shape[0]

    # Create an instance of URLExtract
    extract = URLExtract()

    # Fetch the number of links shared
    links_list = extract.find_urls(all_messages)
    links_count = len(links_list)

    # Fetch the number of emojis shared
    emojis_list = [c for c in all_messages if c in emoji.EMOJI_DATA]
    emojis_count = len(emojis_list)

    return message_count, words_count, media_count, links_count, emojis_count

def generate_wordcloud(selected_user, df):
    # Load stop words
    # with open('stop_hinglish.txt', 'r') as f:
    #     stop_words = f.read().splitlines()

    # Filter the DataFrame based on the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Remove rows with '<Media omitted>' in the 'message' column
    df = df[df['Message'] != '<Media omitted>']

    # Define a function to remove stop words from a message
    # def remove_stop_words(message):
    #     words = message.lower().split()
    #     filtered_words = [word for word in words if word not in stop_words]
    #     return " ".join(filtered_words)

    # Apply stop word removal to the 'message' column
    #df['message'] = df['message'].apply(remove_stop_words)

    # Create a WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='#E5E5E5')
    wordcloud = wc.generate(" ".join(df['Message']))

    return wordcloud

def most_active_users(df):
    # Count the number of messages sent by each user and get the top users
    top_users_sr = df['User'].value_counts().head()

    # Calculate the percentage of messages sent by each user
    total_messages = df.shape[0]
    user_percentages_sr = (top_users_sr/ total_messages * 100).round(2)

    # Create a DataFrame with user names and their message percentages
    top_users_contribution_df = pd.DataFrame({'User': user_percentages_sr.index, 'Contribution(%)': user_percentages_sr}).reset_index(drop=True)

    return top_users_sr, top_users_contribution_df