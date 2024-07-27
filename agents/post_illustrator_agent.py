from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from config.settings import OPENAI_API_KEY
from datetime import datetime
import os
import requests

def post_illustrator_agent(state: dict):
    post_content = state['content']
    print("\nGenerating image for the post...")
    
    # Initialize DALL-E model
    model = DallEAPIWrapper()
    
    # Generate image based on the post content
    image_url = model.run(post_content)
    
    # Save image to a file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, "..", "output", datetime.now().strftime('%Y-%m-%d'))
    os.makedirs(image_dir, exist_ok=True)
    image_path = os.path.join(image_dir, "image.png")
    
    response = requests.get(image_url)
    with open(image_path, "wb") as f:
        f.write(response.content)
    
    # Save post content and image path to a markdown file
    markdown_path = os.path.join(image_dir, "post.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(f"# {post_content}\n\n![Image]({image_path})")
    
    return {'image_path': image_path}