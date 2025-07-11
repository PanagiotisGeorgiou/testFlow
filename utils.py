import re
import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)
    print("Text saved to {}".format(filename))


def extract_video_id(url):
    # Define regex pattern to match YouTube video ID
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    
    # Return the video ID if a match is found, else None
    return match.group(1) if match else None

# Define function to generate search queries using OpenAI
def generate_search_queries(brand_name, brand_brief):

   # Call OpenAI API with ChatCompletion to get search queries
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": (
                f"Provide a list of 30 YouTube search queries that could help find videos relevant to {brand_name}'s target audience. "
                f"The queries should avoid using the brand name '{brand_name}' but should target topics, themes, and interests relevant to the brand’s audience. "
                 "The queries should also be in a form of keywords, and contain maximum three words"
                #f"Here’s a brief about the brand: {brand_brief}"
                f"Here’s the brand's target audience: {brand_brief}"
            )}
        ]        #max_tokens=100
    )
    # Extract generated queries (assuming they come as a list)
    queries = response['choices'][0]['message']['content'].strip().splitlines()
    
    # Limit to exactly five queries (may need extra filtering based on response format)
    return [query.strip("- ") for query in queries if query.strip()]

