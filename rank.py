import gradio as gr
import pandas as pd
import numpy as np
import requests

# SerpAPI key setup
SERP_API_KEY = "44af408eb0808dbdbad81e8c17951f05fa502d5820a35b95267d4e82ef060ee6"

# Define the "Socio Score" formula with weighted factors
def calculate_socio_score(trust_factor, longevity_factor, engagement_quality, reach_factor, w1=0.3, w2=0.2, w3=0.3, w4=0.2):
    return (w1 * trust_factor) + (w2 * longevity_factor) + (w3 * engagement_quality) + (w4 * reach_factor)

# Fetch influencer data using requests
def fetch_influencer_data(name, platform):
    params = {
        "engine": "google",
        "q": f"{name} {platform} influencer stats",
        "api_key": SERP_API_KEY
    }
    response = requests.get("https://serpapi.com/search", params=params)
    data = response.json()
    return data

# Extract metrics (mocking some values for now)
def extract_metrics(data):
    trust_factor = np.random.uniform(0.5, 1)
    longevity_factor = np.random.uniform(0.5, 1)
    engagement_quality = np.random.uniform(0.5, 1)
    reach_factor = np.random.uniform(0.5, 1)

    # Mock follower count, views, and engagement stats
    followers = np.random.randint(50000, 5000000)
    views = np.random.randint(1000000, 100000000)
    engagement = np.random.uniform(0.5, 1)

    return trust_factor, longevity_factor, engagement_quality, reach_factor, followers, views, engagement

# Normalize scores within category
def normalize_scores(scores):
    mean = np.mean(scores)
    std_dev = np.std(scores)
    return [(score - mean) / std_dev for score in scores]

# Rank influencers based on custom and raw metrics
def rank_influencers(influencers, platform):
    scores = []
    data_records = []

    for influencer in influencers:
        data = fetch_influencer_data(influencer, platform)
        trust, longevity, engagement, reach, followers, views, engagement_stat = extract_metrics(data)
        score = calculate_socio_score(trust, longevity, engagement, reach)
        scores.append(score)

        # Store all data for detailed breakdown
        data_records.append([influencer, trust, longevity, engagement, reach, followers, views, engagement_stat, score])

    # Normalize custom scores
    normalized_scores = normalize_scores(scores)
    for i in range(len(data_records)):
        data_records[i].append(normalized_scores[i])

    columns = [
        "Influencer", "Trust Factor", "Longevity Factor", "Engagement Quality", "Reach Factor",
        "Followers", "Views", "Engagement Rate", "Socio Raw Score", "Socio Normalized Score"
    ]

    # Main DataFrame with all data
    df = pd.DataFrame(data_records, columns=columns)

    # Create additional simple ranking tables (only name + specific metric)
    rank_by_followers = df[["Influencer", "Followers"]].sort_values(by="Followers", ascending=False).copy()
    rank_by_views = df[["Influencer", "Views"]].sort_values(by="Views", ascending=False).copy()
    rank_by_engagement = df[["Influencer", "Engagement Rate"]].sort_values(by="Engagement Rate", ascending=False).copy()

    # Rank influencers by Socio Score
    df.sort_values(by="Socio Normalized Score", ascending=False, inplace=True)

    return df, rank_by_followers, rank_by_views, rank_by_engagement

# Generate a clean, short raw data report for each influencer
def generate_raw_data_report(influencers, platform):
    reports = []
    for influencer in influencers:
        data = fetch_influencer_data(influencer, platform)
        _, _, _, _, followers, views, engagement = extract_metrics(data)
        report = f"**{influencer} ({platform})**\n- Followers: {followers:,}\n- Views: {views:,}\n- Engagement Rate: {engagement:.2f}"
        reports.append(report)
    return "\n\n".join(reports)

# Format tables for better display
def format_table(df):
    # Format numbers with commas for readability
    if 'Followers' in df.columns:
        df['Followers'] = df['Followers'].apply(lambda x: f"{x:,}")
    if 'Views' in df.columns:
        df['Views'] = df['Views'].apply(lambda x: f"{x:,}")
    
    # Format float values to 2 decimal places
    for col in df.select_dtypes(include=['float']).columns:
        df[col] = df[col].apply(lambda x: f"{x:.2f}")
        
    return df

# Gradio Interface Function
def influencer_analysis_interface(influencers, platform):
    if not influencers.strip():
        return ("Please enter at least one influencer name.", "", "", "", "")
        
    influencer_list = [i.strip() for i in influencers.split(',') if i.strip()]
    if not influencer_list:
        return ("Please enter valid influencer names.", "", "", "", "")
    
    try:
        df, rank_by_followers, rank_by_views, rank_by_engagement = rank_influencers(influencer_list, platform)
        
        # Format tables for better display
        df_formatted = format_table(df)
        rank_by_followers_formatted = format_table(rank_by_followers)
        rank_by_views_formatted = format_table(rank_by_views)
        rank_by_engagement_formatted = format_table(rank_by_engagement)
        
        raw_data_report = generate_raw_data_report(influencer_list, platform)

        # Format output with cleaner HTML
        return (
            f"<div class='data-section'><h3>Raw Data</h3><div class='data-content'>{raw_data_report}</div></div>",
            f"<div class='data-section'><h3>Ranking by Socio Score</h3><div class='data-content'><table class='data-table'>{df_formatted.to_html(index=False, classes='data-table')}</table></div></div>",
            f"<div class='data-section'><h3>Ranking by Followers</h3><div class='data-content'><table class='data-table'>{rank_by_followers_formatted.to_html(index=False, classes='data-table')}</table></div></div>",
            f"<div class='data-section'><h3>Ranking by Views</h3><div class='data-content'><table class='data-table'>{rank_by_views_formatted.to_html(index=False, classes='data-table')}</table></div></div>",
            f"<div class='data-section'><h3>Ranking by Engagement Rate</h3><div class='data-content'><table class='data-table'>{rank_by_engagement_formatted.to_html(index=False, classes='data-table')}</table></div></div>"
        )
    except Exception as e:
        return (f"<div class='error-message'>Error analyzing influencers: {str(e)}</div>", "", "", "", "")

# Create a cleaner Gradio interface
with gr.Blocks(
    title="InfluenceIQ - Social Media Influencer Analysis",
    css="""
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Rubik:wght@400;500;600;700&display=swap');
    
    :root {
        --primary-color: #d00e18;
        --primary-dark: #900c3f;
        --primary-light: #ffebee;
        --secondary-color: #2b2d42;
        --text-color: #333;
        --background-light: #ffffff;
        --background-dark: #f9f9f9;
        --border-color: #e9ecef;
        --shadow-sm: 0 4px 6px rgba(0,0,0,0.05);
        --shadow-md: 0 8px 15px rgba(0,0,0,0.08);
        --radius-sm: 8px;
        --radius-md: 15px;
        --transition: all 0.3s ease;
    }
    
    body {
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-color);
        background-color: var(--background-dark);
        line-height: 1.6;
    }
    
    /* Container styling */
    #component-0 {
        max-width: 1200px !important;
        margin: 2rem auto !important;
        border-radius: var(--radius-md) !important;
        box-shadow: var(--shadow-md) !important;
        overflow: hidden !important;
        background: var(--background-light) !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    
    /* Header styling */
    .app-header {
        padding: 2.5rem 2.5rem 2rem;
        background: linear-gradient(135deg, #d00e18, #900c3f);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .app-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 20px;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 1200 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z' fill='%23ffffff' fill-opacity='.3'%3E%3C/path%3E%3C/svg%3E");
        background-size: cover;
        transform: scale(1.5);
        z-index: 1;
    }
    
    .app-header h1 {
        font-family: 'Rubik', sans-serif;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        position: relative;
        z-index: 2;
    }
    
    .app-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 700px;
        position: relative;
        z-index: 2;
        font-weight: 300;
    }
    
    /* Form styling */
    .form-container {
        background: var(--background-light);
        padding: 2rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    /* Fixing input elements */
    .form-container input, 
    .form-container select,
    .form-container textarea {
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.9rem 1.2rem !important;
        background-color: white !important;
        color: var(--text-color) !important;
        font-size: 1rem !important;
        font-family: 'Poppins', sans-serif !important;
        transition: var(--transition) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .form-container input:focus, 
    .form-container select:focus,
    .form-container textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(208, 14, 24, 0.15) !important;
        outline: none !important;
    }
    
    /* Fix for dropdown elements */
    .gradio-dropdown {
        border-radius: var(--radius-sm) !important;
    }
    
    .gradio-dropdown > div {
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-sm) !important;
    }
    
    /* Results styling */
    .results-container {
        padding: 2rem;
        background: var(--background-dark);
    }
    
    .data-section {
        background: white;
        border-radius: var(--radius-sm);
        margin-bottom: 1.8rem;
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: var(--transition);
    }
    
    .data-section:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-3px);
    }
    
    .data-section h3 {
        font-family: 'Rubik', sans-serif;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 1.2rem;
        margin: 0;
        background: linear-gradient(to right, rgba(208, 14, 24, 0.05), rgba(144, 12, 63, 0.05));
        color: var(--primary-color);
        border-bottom: 1px solid var(--border-color);
        display: flex;
        align-items: center;
    }
    
    .data-section h3::before {
        content: '';
        display: inline-block;
        width: 4px;
        height: 18px;
        background: var(--primary-color);
        margin-right: 10px;
        border-radius: 2px;
    }
    
    .data-content {
        padding: 1.2rem;
        overflow-x: auto;
    }
    
    /* Table styling */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.95rem;
    }
    
    .data-table th {
        background-color: #f8f9fa;
        text-align: left;
        padding: 1rem;
        border-bottom: 1px solid var(--border-color);
        font-weight: 600;
        font-family: 'Rubik', sans-serif;
        color: var(--secondary-color);
    }
    
    .data-table td {
        padding: 0.9rem 1rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .data-table tr:nth-child(even) {
        background-color: rgba(0,0,0,0.01);
    }
    
    .data-table tr:hover {
        background-color: rgba(208, 14, 24, 0.03);
    }
    
    .data-table tr:last-child td {
        border-bottom: none;
    }
    
    /* Button styling */
    button.primary {
        background: linear-gradient(135deg, #d00e18, #900c3f) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.9rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
        cursor: pointer !important;
        transition: var(--transition) !important;
        box-shadow: 0 4px 15px rgba(208, 14, 24, 0.2) !important;
        letter-spacing: 0.5px !important;
    }
    
    button.primary:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 20px rgba(208, 14, 24, 0.3) !important;
    }
    
    button.primary:focus {
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(208, 14, 24, 0.3) !important;
    }
    
    /* Error messages */
    .error-message {
        color: var(--primary-color);
        padding: 1rem;
        background: var(--primary-light);
        border-radius: var(--radius-sm);
        border: 1px solid rgba(208, 14, 24, 0.2);
        margin-bottom: 1rem;
        font-size: 0.95rem;
    }
    
    /* Loader styling */
    .wrap.svelte-rwxv37 {
        border-color: var(--primary-color) !important;
    }
    
    /* Label styling */
    label span {
        font-family: 'Rubik', sans-serif !important;
        font-weight: 500 !important;
        color: var(--secondary-color) !important;
    }
    
    /* Responsive improvements */
    @media (max-width: 768px) {
        .app-header {
            padding: 2rem 1.5rem 1.5rem;
        }
        
        .app-header h1 {
            font-size: 1.8rem;
        }
        
        .form-container, .results-container {
            padding: 1.5rem;
        }
        
        .data-section h3 {
            font-size: 1.1rem;
            padding: 1rem;
        }
        
        button.primary {
            width: 100% !important;
            padding: 0.8rem !important;
        }
    }
    """
) as demo:
    # Header
    with gr.Row(elem_classes=["app-header"]):
        gr.Markdown(
            """
            # InfluenceIQ
            Uncover the power behind every voice with advanced social media influencer analytics
            """
        )
    
    # Input Form
    with gr.Row(elem_classes=["form-container"]):
        with gr.Column(scale=3):
            influencers_input = gr.Textbox(
                label="Enter Influencers (comma-separated)",
                placeholder="e.g., MrBeast, Emma Chamberlain, Logan Paul",
                lines=2
            )
        with gr.Column(scale=2):
            platform_dropdown = gr.Dropdown(
                choices=["Instagram", "YouTube", "TikTok", "Twitter"],
                label="Select Platform",
                value="Instagram"
            )
        with gr.Column(scale=1, min_width=100):
            analyze_btn = gr.Button("Analyze", variant="primary", elem_classes=["primary"])
    
    # Results
    with gr.Row(elem_classes=["results-container"]):
        with gr.Column():
            raw_output = gr.HTML(label="Raw Data")
            socio_output = gr.HTML(label="Socio Score Ranking")
            followers_output = gr.HTML(label="Followers Ranking")
            views_output = gr.HTML(label="Views Ranking")
            engagement_output = gr.HTML(label="Engagement Ranking")
    
    # Set up event listeners
    analyze_btn.click(
        fn=influencer_analysis_interface,
        inputs=[influencers_input, platform_dropdown],
        outputs=[raw_output, socio_output, followers_output, views_output, engagement_output]
    )

# Launch the app
demo.launch()