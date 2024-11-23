import boto3
import base64
import json

# Initialize a session using Amazon Bedrock
client = boto3.client('bedrock-runtime', region_name='us-west-2')

# Define the parameters for the model invocation
body = {
    "textToImageParams": {
        "text": "Make me a graph of the improvement of the company from the following budgets during the 1 trimester: 1000, 2000, 5000"
    },
    "taskType": "TEXT_IMAGE",
    "imageGenerationConfig": {
        "cfgScale": 8,
        "seed": 0,
        "width": 512,
        "height": 512,
        "numberOfImages": 1
    }
}

# Invoke the model
response = client.invoke_model(
    modelId='amazon.titan-image-generator-v1',
    body=json.dumps(body)
)

# Read and decode the response
response_body = json.loads(response['body'].read().decode('utf-8'))

# Save the full response to a file for inspection
with open('response.json', 'w') as response_file:
    json.dump(response_body, response_file, indent=4)

# Access the generated image data
if 'images' in response_body and len(response_body['images']) > 0:
    image_data = response_body['images'][0]

    # Save the image
    with open('generated_image.png', 'wb') as image_file:
        image_file.write(base64.b64decode(image_data))

    print("Image saved as 'generated_image.png'")
else:
    print("No images generated.")
