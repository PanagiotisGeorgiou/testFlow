import openai
import pandas as pd
import os
from dotenv import load_dotenv
import utils

load_dotenv()

# Set your OpenAI API key here or load from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # or set directly: openai.api_key = "YOUR_API_KEY"


# Function to read comments from the specific CSV file structure
def read_comments_from_csv(file_path):
    comments_df = pd.read_csv(file_path)
    comments = comments_df['comment'].dropna().tolist()  # Extract comments and remove any empty rows
    return comments

# Function to read a video transcript from a text file
def read_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to analyze comments and transcript with GPT-3.5 Turbo
def analyze_comments_with_openai(comments, transcript):
    # Combine comments into a single string
    comments_text = "\n".join(comments)
    
    # Formulate the prompt for the analysis
    prompt = f"""
    Based on the following customer comments and video transcript, analyze the audience language and answer the following:
    
    1. Tone and Formality: Describe the tone (e.g., casual, formal) and level of formality in the comments.
    2. Sentiment: Provide the overall sentiment in the comments (positive, negative, mixed, etc.).
    3. Recurring Themes or Phrases: Identify any recurring themes or phrases in the comments.
    4. Common Topics and Pain Points: Highlight any common topics or pain points mentioned by the audience.
    
    Comments:
    {comments_text}
    
    Video Transcript:
    {transcript}
    """
    
    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    
    # Get the response text
    answer = response['choices'][0]['message']['content']
    return answer

# Main function to run the analysis
def main():
    url = input("Enter YouTube URL: ")  
    video_id = utils.extract_video_id(url)
    comments = read_comments_from_csv(f'{video_id}_user_comments.csv')
    transcript = read_transcript(f'{video_id}_transcription.txt')
    analysis = analyze_comments_with_openai(comments, transcript)
    
    # Print the analysis
    utils.save_text_to_file(analysis, f'language_analysis/{video_id}_Language_of_comments_analysis.txt')
    #print("Analysis of Comments and Transcript:")
   # print(analysis)



# Run the main function
main()
