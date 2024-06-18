import openai
from config import OPENAI_API_KEY

# Set your API key
openai.api_key = OPENAI_API_KEY


# Function to get response from ChatGPT
def get_chatgpt_response(prompt='', model="gpt-3.5-turbo", max_tokens=50):
    try:
        res_ = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return res_.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)


# Example usage
prompt = "How do I create a ChatGPT bot using GPT-3.5?"
response = get_chatgpt_response(prompt)
print(response)
