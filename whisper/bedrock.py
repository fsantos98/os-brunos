import boto3
import json
from datetime import datetime

current_day = datetime.now().day
current_month = datetime.now().month
current_year = datetime.now().year
curr_date = str(current_day) + '/' + str(current_month) + '/' + str(current_year)

def get_bedrock_completion(prompt):
    brt = boto3.client(service_name='bedrock-runtime')

    body = json.dumps({
        "inputText": f"Extract the INITIAL_TIME and FINAL_TIME from the following text: {prompt}. The time should be in TIMESTAMP format in seconds. Today is {curr_date}",
        "textGenerationConfig": {
            "maxTokenCount": 3072,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9
        }
    })

    modelId = 'amazon.titan-text-express-v1'
    accept = 'application/json'
    contentType = 'application/json'

    response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())

    return response_body
