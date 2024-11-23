import json
import logging
import boto3
from botocore.exceptions import ClientError
from sqlite import DatabaseManager  # Assuming DatabaseManager is implemented as described earlier


class ImageError(Exception):
    """Custom exception for errors returned by Amazon Titan Text Express model."""
    def __init__(self, message):
        self.message = message


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def generate_text(model_id, body):
    """
    Generate text using Amazon Titan Text Express model on demand.

    Args:
        model_id (str): Model identifier (e.g., amazon.titan-text-express-v1).
        body (str): The request body to use.

    Returns:
        response_body (json): The response from the model.
    """
    logger.info("Generating text with Amazon Titan Text Express model %s", model_id)

    bedrock = boto3.client(service_name='bedrock-runtime')

    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body, modelId=model_id, accept=accept, contentType=content_type
    )
    response_body = json.loads(response.get("body").read())

    finish_reason = response_body.get("error")

    if finish_reason is not None:
        raise ImageError(f"Text generation error. Error is {finish_reason}")

    logger.info(
        "Successfully generated text with Amazon Titan Text Express model %s", model_id
    )

    return response_body


def send_to_generate_summary(prompt, command, user_id):
    """
    Generate a summary using Amazon Titan Text Express and store it in the database.

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

        model_id = 'amazon.titan-text-express-v1'

        # Prepare the prompt
        discussion_prompt = prompt
        summary_command = command
        full_prompt = f"{discussion_prompt}\n\n{summary_command}"

        body = json.dumps({
            "inputText": full_prompt,
            "textGenerationConfig": {
                "maxTokenCount": 4096,
                "stopSequences": [],
                "temperature": 0,
                "topP": 1
            }
        })

        # Generate text
        response_body = generate_text(model_id, body)

        # Log input and response details
        logger.info(f"Input token count: {response_body['inputTextTokenCount']}")
        for result in response_body['results']:
            logger.info(f"Token count: {result['tokenCount']}")
            logger.info(f"Output text: {result['outputText']}")
            logger.info(f"Completion reason: {result['completionReason']}")

        # Insert the summary into the database
        db_manager = DatabaseManager(
            db_name='defaultdb',
            user='avnadmin',
            password='AVNS_U-c1ezivY9TcPqqXrwg',
            host='mysql-3ed7264d-execcsgo-bef4.f.aivencloud.com',
            port=18173
        )
        for result in response_body['results']:
            summary_text = result['outputText']
            db_manager.insert_summary(user_id, summary_text)

        return response_body

    except ClientError as err:
        message = err.response["Error"]["Message"]
        logger.error("A client error occurred: %s", message)
        raise

    except ImageError as err:
        logger.error(err.message)
        raise

    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        raise
