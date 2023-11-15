# ChatStat | The WhatsApp Chat Analyzer

## Overview
ChatStat is a Streamlit-based WhatsApp chat analyzer designed to provide insightful statistics about your conversations. Easily analyze your chat data in a user-friendly environment with this tool.

## Getting Started
To utilize ChatStat, follow these steps:

1. Export your WhatsApp chat: WhatsApp > Chat > Three dots > More > Export chat > Without media > Save the exported .txt file to your device.

2. Upload the exported file: Utilize the file upload feature to upload the exported WhatsApp chat file.

## Features
### Analysis Filters
- Top Statistics
- Most Mentioned (Tagged) User
- Daily Timeline
- Activity Map
- User Who Chats the Most
- Word Cloud
- Emoji Usage Analysis
- Sentiment Analysis

### Processed WhatsApp Chat Data
Explore the processed WhatsApp chat data in an expandable section within the app.

### User Filter
Analyze chat statistics specific to a selected user in a group chat. Choose a user from the sidebar, and ChatStat will provide insights based on that user's activity.

### Top Statistics
Gain an overview of message count, word count, media count, links count, and emoji count.

### Most Mentioned (Tagged) User
Identify the most mentioned (tagged) users in the group.

### User Who Chats the Most
Determine which user is the most active in terms of message count.

### Emoji Usage Analysis
Analyze the frequency of emoji usage in the chat.

### Daily Timeline
View the message count over the days.

### Activity Map
Explore the top messaging days and months. Analyze the distribution of messages throughout the week and hours of the day with the day vs. hour activity heatmap.

### Word Cloud
Generate a word cloud based on the chat text and view the most common words.

### Sentiment Analysis
Analyze the overall sentiment of the chat and identify the most positive, negative, and neutral contributors.

### Download All Plots
Download a zip file containing all generated plots for further analysis or sharing.

## Usage
1. Upload your exported WhatsApp chat file.
2. Select the desired filters from the sidebar.
3. Click the "Show Analysis" button to generate insights.
4. Download a zip file containing all generated plots for further analysis or sharing.

## Development
This project is developed using Streamlit, matplotlib, dataPreprocessor, and utils. The codebase is available in the files:
- [app.py](app.py)
- [dataPreprocessor.py](dataPreprocessor.py)
- [utils.py](utils.py)

## Deployment Information
This app is deployed using [Streamlit Sharing](https://www.streamlit.io/sharing). You can access the live version [here](https://chat-stat.streamlit.app/).

## Hosting Information
For those interested in hosting or running the app locally, you can follow these steps:

1. Clone the repository: 
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
    ```bash
    streamlit run app.py
   
## Contributors
- Tirthesh Jain
- Aditya Tomar

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- [Streamlit](https://streamlit.io/)
- [Matplotlib](https://matplotlib.org/)

## Contact
For any questions or issues, please contact the developers:
- Tirthesh Jain - [tirtheshjain2408@gmail.com]
- Aditya Tomar - [aditya001tomar@gmail.com]

---

<div align="center">🔒 We do not share or store your data beyond the scope of this application.</div>

<div align="center">💖 Developed with love by Tirthesh Jain & Aditya Tomar. © [2023] ChatStat.</div>
