import pandas as pd
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import io
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
import base64  # Standard Python Module

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

def most_chat_users(df):
    # Count the number of messages sent by each user and get the top users
    top_users_sr = df['User'].value_counts().head()

    # Calculate the percentage of messages sent by each user
    total_messages = df.shape[0]
    user_percentages_sr = (top_users_sr/ total_messages * 100).round(2)

    # Create a DataFrame with user names and their message percentages
    top_users_contribution_df = pd.DataFrame({'User': user_percentages_sr.index, 'Contribution(%)': user_percentages_sr}).reset_index(drop=True)

    return top_users_sr, top_users_contribution_df

def emoji_analysis(selected_user,df):
    if selected_user != 'All':
        df = df[df['User'] == selected_user]
    
    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'])

    # Extract emojis from the combined messages
    emojis_list = [c for c in all_messages if c in emoji.EMOJI_DATA]

    # Count the frequency of each emoji
    emojis_freq = Counter(emojis_list)

    # Convert the emoji frequency dictionary to a DataFrame
    emojis_freq_df = pd.DataFrame(list(emojis_freq.items()), columns=['Emoji', 'Frequency'])

    # Sort the DataFrame by frequency (descending order)
    emojis_freq_df = emojis_freq_df.sort_values(by='Frequency', ascending=False)

    # Reset the DataFrame index
    emojis_freq_df = emojis_freq_df.reset_index(drop=True)

    return emojis_freq_df


def get_daily_timeline(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    daily_timeline = df.groupby('Date',sort = False).count()['Message'].reset_index()

    return daily_timeline


def get_week_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    week_activity_map_sr = df['day_name'].value_counts()
    return week_activity_map_sr


def get_month_activity_map(selected_user,df):

    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    month_activity_map_sr = df['month_name'].value_counts()
    return month_activity_map_sr


def generate_wordcloud(selected_user, df):
    # Load stop words
    with open('stop_words.txt', 'r') as f:
        stop_words = f.read().splitlines()
        
    # Filter the DataFrame based on the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Remove rows with '<Media omitted>' in the 'message' column
    df = df[df['Message'] != '<Media omitted>']

    # Define a function to remove stop words from a message
    def remove_stop_words(message):
        words = message.lower().split()
        filtered_words = [word for word in words if word not in stop_words]
        return " ".join(filtered_words)

    # Apply stop word removal to the 'message' column
    df['Message'] = df['Message'].apply(remove_stop_words)

    # Create a WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wordcloud = wc.generate(" ".join(df['Message']))

    return wordcloud

# Function to do sentiment analysis
# Returns the count of number of positive, negative and neutral sentiment sentences
def sentiment_analysis(selected_user, df):
    if(selected_user != 'All'):
        df = df[df['User']==selected_user]
        
    sent = SentimentIntensityAnalyzer()
    positive = 0
    negative = 0
    neutral = 0
    df = df[df['Message']!='<Media omitted>']
    for msg in df['Message']:
        scores = sent.polarity_scores(msg)
        key_max = max(scores, key=lambda x: scores[x])
        if(key_max=='neg'):
            negative+=1
        elif(key_max=='pos'):
            positive+=1
        else:
            neutral+=1
            
    return positive, negative, neutral

# Generates HTML download links for a list of Matplotlib figures.
# Args: figures: A list of Matplotlib figures.
# Returns: A list of HTML download links, one for each figure.
def generate_html_download_link(figures):
  links = []
  for i, fig in enumerate(figures):
    towrite = io.BytesIO()
    fig.savefig(towrite, format="png")
    towrite.seek(0)
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:image/png;base64, {b64}" download="plot{i}.png"> Download Plot{i} </a>'
    links.append(href)
  return links

    
    