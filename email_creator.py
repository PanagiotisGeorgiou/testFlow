import openai
import os
from dotenv import load_dotenv
import utils

load_dotenv()

# Set your OpenAI API key here or load from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # or directly: openai.api_key = "YOUR_API_KEY"

# Function to dynamically read and combine language analysis from all files in a folder
def read_language_analyses_from_folder(folder_path):
    combined_analysis = []
    # Iterate over all .txt files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # Only process text files
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_analysis.append(file.read())
    # Combine analyses into a single summary
    return "\n\n".join(combined_analysis)

# Create a string of HTML image tags from a list of image URLs or paths
def format_images_as_html(image_urls):
    image_html = ""
    for url in image_urls:
        image_html += f'<img src="{url}" alt="Promotional Image" style="max-width: 100%; margin: 10px 0;">\n'
    return image_html

# Function to generate an HTML promotional email using GPT-3.5-turbo
def generate_promotional_email_html(brand_brief, promo_goal, images_html, combined_language_analysis):
    # Create the prompt for the OpenAI API
    prompt = f"""
    Based on the following information, write an HTML promotional email that aligns with the audience's language and preferences.

    - **Brand Brief**: {brand_brief}
    - **Promotional Goal**: {promo_goal}
    - **Audience Language Analysis**: {combined_language_analysis}

    Include the following images in the email:
    {images_html}

    The HTML email should:
    - Follow a friendly tone as per the audience analysis.
    - Use engaging language that fits the audience's communication style.
    - Include a clear call-to-action button with a link placeholder (e.g., `<a href='#'>`).
    - Be formatted properly with sections, text styling, and images.
    
    Generate the full HTML for the email.
    """

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled in HTML email marketing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    
    # Get the HTML content from the response
    email_html = response['choices'][0]['message']['content']
    return email_html

# Main function to generate the HTML email
def main():
    # Input data
    brand_brief = "Nike is an American athletic footwear and apparel corporation headquartered near Beaverton, Oregon, United States. It is the world's largest supplier of athletic shoes and apparel and a major manufacturer of sports equipment."  
    promo_goal = "20 percent off on men's shoes, for 24 hours only on website Nike.com"  
    images = ["https://media.istockphoto.com/id/1492552654/vector/hand-drawn-style-20-percent-off-discount-sale-promotion-label-illustration-vector.jpg?s=2048x2048&w=is&k=20&c=ymHKmObOlqumrtATBAS1CYmKZnzfxDiN9CxgoDT9HP4=", 
              "https://www.logodesignvalley.com/blog/wp-content/uploads/2023/05/05.png",
              "https://cdna.lystit.com/300/375/tr/photos/asos/5fc2f6f3/nike-Black-Air-Winflo-11-Sneakers.jpeg"]
    language_analysis_folder = 'language_analysis'  # Folder containing language analysis text files

    # Read and prepare the inputs
    combined_language_analysis = read_language_analyses_from_folder(language_analysis_folder)
    images_html = format_images_as_html(images)

    # Generate the email HTML
    email_html = generate_promotional_email_html(brand_brief, promo_goal, images_html, combined_language_analysis)

    # Output the email HTML
    utils.save_text_to_file(email_html, 'demo.html')
    # print("Generated Promotional Email HTML:")
    # print(email_html)

# Run the main function
main()
