from googleapiclient.discovery import build
import datetime
import os
from dotenv import load_dotenv
import utils

load_dotenv()


# Setup YouTube API key
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
def read_brief(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Define function to search YouTube with the generated queries
def search_youtube_videos(queries):
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    # Set the date range for the last three months
    current_date = datetime.datetime.utcnow()
    one_month_ago = (current_date - datetime.timedelta(days=90)).replace(microsecond=0)
    published_after = one_month_ago.isoformat("T") + "Z"
    
    results = {}
    for query in queries:
        # Perform a search request on YouTube
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            publishedAfter=published_after,
            regionCode="US",
            videoDuration="medium",
            order="viewCount",
            maxResults=2  # Adjust based on your requirements
        )
        response = request.execute()
        
        # Extract relevant data and store it in the results dictionary
        videos = []
        for item in response.get("items", []):
            video_data = {
                "title": item["snippet"]["title"],
                "videoId": item["id"]["videoId"],
                "description": item["snippet"]["description"],
                "publishedAt": item["snippet"]["publishedAt"]
            }
            videos.append(video_data)
        results[query] = videos

    return results

# Main function to perform the process
def main():
    # Step 1: Generate search queries
    queries = utils.generate_search_queries(brand_name, brand_brief)
    
    # Step 2: Search YouTube with the generated queries
    youtube_results = search_youtube_videos(queries)
    
    # Display the results
    for query, videos in youtube_results.items():
        print(f"\nResults for query: '{query}'")
        for video in videos:
            print(f"Title: {video['title']}")
            print(f"Video ID: {video['videoId']}")
            print(f"Description: {video['description']}")
            print(f"Published At: {video['publishedAt']}")
            print("-" * 40)

# Run the main function with a given brand name
brand_name = "Nike"  # Example brand
brand_brief = read_brief("Nike_Target_Audience.txt") # Example brand brief
main()
