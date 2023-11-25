import pandas as pd
import emoji
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import io
import nltk
nltk.downloader.download('vader_lexicon')
nltk.downloader.download('stopwords')
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import base64  # Standard Python Module
import re
from zipfile import ZipFile

# Function calculate message_count, words_count, media_count, links_count, emojis_count
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


# Function find most mentioned(tagged) user
def most_tagged_users(df):
    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'])

    tagged_users = re.findall(r'@\d{12}', all_messages)  # Find tagged users in the format @91XXXXXXXXXX

    # Replace "@" with "+" in the tagged_users list
    tagged_users = [user.replace('@', '+') for user in tagged_users]

    # Create a new DataFrame for the most tagged users and their frequencies
    most_tagged_user_df = pd.DataFrame(tagged_users, columns=['Tagged Users'])
    most_tagged_user_df['Frequency'] = most_tagged_user_df['Tagged Users'].apply(lambda x: tagged_users.count(x))
    most_tagged_user_df = most_tagged_user_df.drop_duplicates().sort_values(by='Frequency')

    return most_tagged_user_df


# Function find most active users
def most_chat_users(df):
    # Count the number of messages sent by each user and get the top users
    top_users_sr = df['User'].value_counts().head()

    # Calculate the percentage of messages sent by each user
    total_messages = df.shape[0]
    user_percentages_sr = (top_users_sr/ total_messages * 100).round(2)

    # Create a DataFrame with user names and their message percentages
    top_users_contribution_df = pd.DataFrame({'User': user_percentages_sr.index, 'Contribution(%)': user_percentages_sr}).reset_index(drop=True)

    return top_users_sr, top_users_contribution_df


# Function return Emojis used and frequency in dataFrame
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

# Function return DataFrame, which contains a count of messages per day 
def get_daily_timeline(selected_user, df):
    # Check if 'All' is selected; if not, filter the DataFrame by the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Group the DataFrame by 'Date', count the number of 'Message' entries for each date,
    # and reset the index to create a new DataFrame
    daily_timeline = df.groupby('Date', sort=False).count()['Message'].reset_index()

    # Return the daily_timeline DataFrame
    return daily_timeline


# ---- utility functions for activity map -----
def get_week_activity_map(selected_user, df):
     # Check if 'All' is selected; if not, filter the DataFrame by the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Create a Series that counts the occurrences of each day name.
    week_activity_map_sr = df['day_name'].value_counts()

    # Return the Series with counts of activities for each day of the week.
    return week_activity_map_sr

def get_month_activity_map(selected_user, df):
     # Check if 'All' is selected; if not, filter the DataFrame by the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Create a Series that counts the occurrences of each month name.
    month_activity_map_sr = df['month_name'].value_counts()

    # Return the Series with counts of activities for each month.
    return month_activity_map_sr


# Function to generates a heatmap of message counts based on the hour of the day and day of the week
# Returns: pandas.DataFrame: A DataFrame representing the day vs. hour activity heatmap.
def get_day_hour_heatmap(selected_user, df):
    # Filter the DataFrame by the selected user, if not 'All'
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Group the data by 'hour' and 'day_name', counting the number of messages
    data = df.groupby(['hour', 'day_name'], as_index=False)['Message'].count()

    # Pivot the data to create the heatmap
    data = data.pivot(index='day_name', columns='hour', values='Message')
     
    # Reorder the day names in the DataFrame
    data = data.reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

    return data


# ---- utility functions for word cloud-----
def generate_wordcloud(selected_user, df):
    # Load stop words
    with open('stop_words.txt', 'r') as f:
        custom_words = set(f.read().splitlines())
        
    # Importing set of stopwords from nltk
    stop_words = set(stopwords.words('english'))
    
    # Merging the two sets, one custom-created and the other from nltk, and storing them as a list
    stop_words = list(stop_words.union(custom_words))

    # Filter the DataFrame based on the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Remove rows with '<Media omitted> & deleted message' in the 'message' column
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']

    # Define a function to remove stop words from a message
    def remove_stop_words(message):
        words = message.lower().split()
        filtered_words = [word for word in words if word not in stop_words]
        return " ".join(filtered_words)

    # Apply stop word removal to the 'message' column
    df['Message'] = df['Message'].apply(remove_stop_words)

    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'])
    
    # Remove emojis from the combined messages
    all_messages = ''.join([c for c in all_messages if c not in emoji.EMOJI_DATA])

    # Use regular expressions to remove user mentions and phone numbers
    all_messages = re.sub(r'(@\d{12})', '', all_messages)

    if len(all_messages) == 0:
        return None, None  # Return None if there are no words
        
    # Create a WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    wordcloud = wc.generate(all_messages)

    # Calculate the most common words and create a DataFrame
    words = all_messages.split()
    most_common_word_df = pd.DataFrame(pd.Series(words).value_counts().head().reset_index())
    most_common_word_df.columns = ['Most Common Words', 'Frequency']

    return wordcloud, most_common_word_df


# ----- utility functions for sentiment analysis--------

# Function to calculate the sentiment score for a given message
def calculate_sentiment_score(message, sent):
    message = emoji.demojize(message)
    scores = sent.polarity_scores(message)
    return scores['compound']

# Function to identify the users with the most positive, negative, and neutral sentiments
def user_sentiment_contributors(df):
    # Initialize the SentimentIntensityAnalyzer
    sent = SentimentIntensityAnalyzer()
    # Create a dictionary to store compound sentiment scores & tootal message for each user
    user_scores = {}
    user_message_counts = {}
    
    # Remove rows with '<Media omitted> & deleted message' in the 'message' column
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']

    # Iterate through the DataFrame to calculate sentiment scores for each user
    for index, row in df.iterrows():
        user = row['User']
        message = row['Message']
        compound_score = calculate_sentiment_score(message, sent)

        # Update the total compound sentiment score and message count for the user
        user_scores[user] = user_scores.get(user, 0) + compound_score
        user_message_counts[user] = user_message_counts.get(user, 0) + 1
    
    # Calculate weighted scores for each user based on sentiment and message count
    weighted_scores = {user: user_scores[user] / user_message_counts[user] for user in user_scores if user_message_counts[user] > 0}

    most_positive_user = max(weighted_scores, key=weighted_scores.get)
    most_negative_user = min(weighted_scores, key=weighted_scores.get)
    most_neutral_user = min(weighted_scores, key=lambda user: abs(weighted_scores[user]))

    return {
        'Most Positive User': most_positive_user,
        'Most Negative User': most_negative_user,
        'Most Neutral User': most_neutral_user
    }

# Function to calculate the count of positive, negative, and neutral sentiment sentences
def sentiment_analysis(selected_user, df):
    # Filter the DataFrame based on the selected user
    if selected_user != 'All':
        df = df[df['User'] == selected_user]

    # Initialize the SentimentIntensityAnalyzer
    sent = SentimentIntensityAnalyzer()
    positive = 0
    negative = 0
    neutral = 0

    # Remove rows with '<Media omitted> & deleted message' in the 'message' column
    df = df[df['Message'] != '<Media omitted>']
    df = df[df['Message'] != 'This message was deleted']

    # Iterate through the messages and count the sentiment categories
    for msg in df['Message']:
        compound_score = calculate_sentiment_score(msg, sent)

        # Update sentiment category counts based on compound score
        if compound_score > 0.05:
            positive += 1
        elif compound_score < -0.05:
            negative += 1
        else:
            neutral += 1

    return positive, negative, neutral


# Function to generate a zip file containing all plots
# Args plot_data (list): A list of Matplotlib figures to be included in the zip file.
# Returns str: Base64-encoded binary data of the zip file containing the plots.
def generate_all_plots_zip(plot_data):
    # Create a BytesIO buffer to hold the zip file
    with io.BytesIO() as zip_buffer:
        # Create a ZipFile object for writing the zip file
        with ZipFile(zip_buffer, "w") as zipf:
            for name, fig in plot_data:
                # Create a BytesIO buffer for each image
                with io.BytesIO() as img_buffer:
                    fig.savefig(img_buffer, format="png")
                    img_buffer.seek(0)
                    # Write the image to the zip file with a unique name
                    zipf.writestr(f"{name}.png", img_buffer.read())
        
        # Move the buffer cursor to the beginning and encode the zip file in base64
        zip_buffer.seek(0)
        b64 = base64.b64encode(zip_buffer.read()).decode()
        
        return b64

    
    
