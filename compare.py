pip install gradio
pip install groq
!pip install gradio requests beautifulsoup4 matplotlib pandas groq wikipedia-api google-search-results
pip install --upgrade google-api-python-client
pip install --upgrade google-auth-oauthlib google-auth-httplib2
import gradio as gr
import requests
import wikipediaapi
from groq import Groq
import pandas as pd
from googleapiclient.discovery import build

# Set up Groq API client
client = Groq(api_key="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")

# Set up SerpAPI configuration
SERPAPI_KEY = "44af408eb0808dbdbad81e8c17951f05fa502d5820a35b95267d4e82ef060ee6"
SERPAPI_URL = "https://serpapi.com/search.json"

# Wikipedia setup with User-Agent
wiki_api = wikipediaapi.Wikipedia(
    language='en',
    user_agent="InfluencerAnalysisTool/1.0 (contact: your_email@example.com)"
)

# YouTube API setup
YOUTUBE_API_KEY =  "AIzaSyBhMeFyFo4xooS4BkYiRYk_0BAXZoVaeAg"  # Add your YouTube API key here
youtube_api = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# 🎯 Fetch influencer summary from Wikipedia
def fetch_wikipedia_summary(username):
    page = wiki_api.page(username.replace(" ", "_"))
    if page.exists():
        return page.summary
    return "No Wikipedia summary found."

# 🔍 Fetch influencer data from Google via SerpAPI
def fetch_google_data(username):
    params = {
        "engine": "google",
        "q": username,
        "api_key": SERPAPI_KEY
    }
    response = requests.get(SERPAPI_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("organic_results", [])
        if results:
            return results[0].get("snippet", "No Google data found.")
    return "No Google data found."

# 🧠 Analyze content via Groq AI
def analyze_influencer_content(username, topic):
    response = client.chat.completions.create(
        messages=[{
            "role": "system",
            "content": f"Analyze the social media presence of {username} on the topic: {topic}. "
                        f"Provide insights on content quality, engagement trends, audience demographics, and growth patterns."
        }],
        model="llama3-8b-8192",
    )
    return response.choices[0].message.content

# 📝 YouTube Channel ID Retrieval
def get_channel_id(api_key, channel_name):
    """Search for a channel by name and get its channel ID."""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": channel_name,
        "type": "channel",
        "maxResults": 1,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        return data["items"][0]["id"]["channelId"]
    else:
        return None

# 📝 Get YouTube Channel Statistics
def get_channel_statistics(api_key, channel_name):
    """Get all available statistics of a channel by name."""
    channel_id = get_channel_id(api_key, channel_name)

    if not channel_id:
        return {"error": "Channel not found"}

    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        "part": "snippet,statistics",
        "id": channel_id,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "items" in data and len(data["items"]) > 0:
        snippet = data["items"][0]["snippet"]
        stats = data["items"][0]["statistics"]
        return {
            "channel_name": snippet.get("title", "N/A"),
            "published_at": snippet.get("publishedAt", "N/A"),
            "subscriber_count": stats.get("subscriberCount", "N/A"),
            "total_views": stats.get("viewCount", "N/A"),
            "total_videos": stats.get("videoCount", "N/A"),
            "custom_url": snippet.get("customUrl", "N/A")
        }
    else:
        return {"error": "Failed to fetch statistics"}

# 📝 Get YouTube Video IDs from a Channel
def get_video_ids(channel_id):
    video_ids = []
    request = youtube_api.search().list(
        part='id',
        channelId=channel_id,
        maxResults=5,  # Limit to recent 5 videos
        order='date'  # Most recent first
    )
    response = request.execute()
    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_ids.append(item['id']['videoId'])
    return video_ids

# 📝 Get Comments from YouTube Videos
def get_comments(video_id, max_comments=5):
    comments = []
    request = youtube_api.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=max_comments
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(comment)

    return comments

# 📌 Core analysis function for both celebrities
def influencer_analysis(celebrity1, celebrity2):
    topics = [
        "Popularity & Reach", "Influence & Impact", "Talent & Skill", "Net Worth & Earning Potential",
        "Audience Engagement & Fandom", "Longevity & Consistency", "Media Appearances & Influence in Entertainment",
        "Personality & Public Image", "Contribution to Industry or Field", "Philanthropy & Charity Work",
        "Global Appeal & Cross-Cultural Impact", "Creativity & Innovation", "Youtube Analysis"
    ]

    # Create empty list for analysis results
    results_celebrity1 = []
    results_celebrity2 = []

    # Get YouTube statistics for each celebrity
    youtube_stats_celebrity1 = get_channel_statistics(YOUTUBE_API_KEY, celebrity1)
    youtube_stats_celebrity2 = get_channel_statistics(YOUTUBE_API_KEY, celebrity2)

    # Fetch data for each celebrity
    try:
        for topic in topics:
            # Get content analysis for each topic for both celebrities
            celebrity1_analysis = analyze_influencer_content(celebrity1, topic)
            celebrity2_analysis = analyze_influencer_content(celebrity2, topic)

            results_celebrity1.append(celebrity1_analysis)
            results_celebrity2.append(celebrity2_analysis)

        # Construct a comparison table
        comparison_data = {
            "Category": topics,
            f"{celebrity1} Analysis": results_celebrity1,
            f"{celebrity2} Analysis": results_celebrity2,
            f"{celebrity1} YouTube Subscriber Count": youtube_stats_celebrity1.get("subscriber_count", "N/A"),
            f"{celebrity2} YouTube Subscriber Count": youtube_stats_celebrity2.get("subscriber_count", "N/A"),
            f"{celebrity1} YouTube Views": youtube_stats_celebrity1.get("total_views", "N/A"),
            f"{celebrity2} YouTube Views": youtube_stats_celebrity2.get("total_views", "N/A"),
            f"{celebrity1} YouTube Videos Published": youtube_stats_celebrity1.get("total_videos", "N/A"),
            f"{celebrity2} YouTube Videos Published": youtube_stats_celebrity2.get("total_videos", "N/A"),
        }
        comparison_table = pd.DataFrame(comparison_data)

        # Return the comparison data and a summary message
        return comparison_table

    except Exception as e:
        return f"⚠ Error fetching data: {e}"

# 🎯 Gradio web interface setup
with gr.Blocks() as interface:
    gr.Markdown("# 🔍 Celebrity Comparison Analysis Tool")
    gr.Markdown("Enter the names of two celebrities to fetch detailed insights on various topics and compare them.")

    with gr.Row():
        celebrity1_input = gr.Textbox(label="Celebrity 1 Name")
        celebrity2_input = gr.Textbox(label="Celebrity 2 Name")
        analyze_button = gr.Button("Analyze Comparison")

    comparison_output = gr.Dataframe(label="📋 Comparison Analysis Table")

    analyze_button.click(influencer_analysis,
                         inputs=[celebrity1_input, celebrity2_input],
                         outputs=[comparison_output])

interface.launch(share=True)
