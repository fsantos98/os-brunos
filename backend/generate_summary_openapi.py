import json
import logging
from datetime import datetime
from openai import OpenAI
from sqlite import DatabaseManager  # Assuming DatabaseManager is implemented as described earlier


class ImageError(Exception):
    """Custom exception for errors during text generation."""
    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
apiKey = "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"

def generate_text_with_openai(prompt):
    """
    Generate text using OpenAI GPT model.

    Args:
        prompt (str): The text prompt for the AI model.

    Returns:
        dict: The response from OpenAI.
    """
    client = OpenAI(api_key=apiKey)  # Replace with your actual API key

    logger.info("Generating text with OpenAI GPT model.")
    
    # Send the prompt to OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a highly efficient and intelligent assistant specialized in summarizing text. "
                    "Your role is to analyze input text, identify key points, and deliver concise, clear, and accurate summaries. "
                    "The summaries should maintain the essence and tone of the original content while reducing unnecessary details. "
                    "If specific instructions are provided, such as focusing on certain aspects or delivering a summary in a particular format, "
                    "follow those instructions carefully. "
                    "Additionally, you must provide the output in raw HTML format. "
                    "Make sure to use appropriate HTML tags such as <p>, <ul>, <li>, <h1>, <h2>, etc. "
                    "Do not include any other non-HTML formatting in your response."
                )
            },
            {"role": "user", "content": prompt}
        ]
    )   

    if not response or not response.choices:
        raise ImageError("Failed to generate text. No response from OpenAI.")
    
    # Access the content of the first choice correctly
    return response.choices[0].message.content


def send_to_generate_summary(prompt, command, user_id):
    """
    Generate a summary using OpenAI GPT and store it in the database.

    Args:
        prompt (str): The text prompt to summarize.
        command (str): The command or additional instructions.
        user_id (int): The ID of the user requesting the summary.

    Returns:
        dict: The response body from the text generation.
    """
    try:
        logging.basicConfig(level=logging.INFO,
                            format="%(levelname)s: %(message)s")

        # Prepare the combined prompt
        full_prompt = f"{prompt}\n\n{command}"
        
        # Generate text using OpenAI
        output_text = generate_text_with_openai(full_prompt)

        logger.info(f"Generated text: {output_text}")

        # Insert the summary into the database
        db_manager = DatabaseManager(
            db_name='defaultdb',
            user='avnadmin',
            password='AVNS_U-c1ezivY9TcPqqXrwg',
            host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
            port=18173
        )
        db_manager.insert_summary(user_id, output_text)

        return {"summary": output_text}

    except Exception as e:
        logger.error("An error occurred: %s", str(e))
        raise
