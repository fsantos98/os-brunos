import openai

# Set your OpenAI API key
api_key = "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"

# Initialize the OpenAI API client
openai.api_key = api_key

def send_prompt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can use other engines like "gpt-3.5-turbo"
        prompt=prompt,
        max_tokens=1000,  # Adjust the max tokens as needed
        n=1,
        stop=None,
        temperature=0.7  # Adjust the temperature for creativity
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    prompt = """
    Your input text goes here. This text will be summarized, rewritten, and formatted by the model.
    """
    result = send_prompt(prompt)
    print(result)
