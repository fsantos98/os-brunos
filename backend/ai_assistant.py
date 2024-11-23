import time
import json
from openai import OpenAI
from datetime import datetime

client = OpenAI(api_key="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")

def get_timestamps_ai(prompt):

    #prompt = "create some bullet points for the meeting i had yesterday at 10am that lasted for 2 hours"
    #{"initial_time":"2024-11-22T10:00:00Z","final_time":"2024-11-22T12:00:00Z"}
    current_day = datetime.now().day
    current_month = datetime.now().month
    current_year = datetime.now().year

    curr_date = str(current_day) + '/' + str(current_month) + '/' + str(current_year)
    print("Today is " + curr_date)

    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {
                "role": "system", 
                "content": "Extract TIMESTAMPS from prompt."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "timestamp",
                "schema": {
                    "type": "object",
                    "properties": {
                        "initial_time": {
                            "description": "The timestamp of the earlier date. Format: YYYY-MM-DD HH:MM, Today is " + curr_date,
                            "type": "string"
                        },
                        "final_time": {
                            "description": "The timestamp of the latest date. Format: YYYY-MM-DD HH:MM, Today is " + curr_date,
                            "type": "string"
                        },
                        "additionalProperties": False
                    }
                }
            }
        }
    )

    print(prompt)
    print(response.choices[0].message.content)
    json_l = json.loads(response.choices[0].message.content)
    print(json_l)


    return json_l["initial_time"], json_l["final_time"]


# completion = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[
#         {
#             "role": "system", 
#             "content": "Try to extract the initial and final timestamp of the given text. It should return in a json objectINITIAL_TIMESTAMP: <time>FINAL_TIMESTAMP: <time>the time should be in timestamp in seconds. The prompt is: give me a summary the meeting I had yesterday from 10am to 12 am. return in json object"
#         }
#     ]
# )

# print(completion.choices[0].message)

#prompt = "give me a summary the meeting I had yesterday from 10am to 12 am."
#{"initial_time":"2024-11-22T10:00:00","final_time":"2024-11-22T12:00:00"}

#prompt = "i need a summary of the meeting i had today from 10am to 11am"
# {"initial_time":"2024-11-23T10:00:00","final_time":"2024-11-23T11:00:00"}
