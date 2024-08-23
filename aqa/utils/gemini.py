"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from config import GEMINI_API_KEY
from aqa.utils.enums import Languages

genai.configure(api_key=GEMINI_API_KEY)

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
    "temperature"       : 1,
    "top_p"             : 0.95,
    "top_k"             : 64,
    "max_output_tokens" : 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)

chat_session = None


def gemini_history(user_parts=None, model_parts=None):
    history = []
    if user_parts:
        history.append(
            {
                "role" : "user",
                "parts": [user_parts, ]
            }
        )
    if model_parts:
        history.append(
            {
                "role" : "user",
                "parts": [user_parts, ]
            }
        )
    session = model.start_chat(history=[])
    return session


def gemini_chat(text):
    global chat_session
    chat_session = gemini_history(user_parts=text)
    res_ = chat_session.send_message(text)
    chat_session = gemini_history(model_parts=res_.text)
    print(res_.text)
    return res_.text


def gemini_shorten_content(cont, length, lang=Languages.VI):
    prompt = f"Tôi có tiêu đề sản phẩm: {cont}.\nVui lòng rút gọn và cải thiện tiêu đề nội dung sản phẩm này nhưng không làm thay đổi ý nghĩa. Nội dung sau khi rút gọn ít hơn {length} kí tự. Vui lòng chỉ cung cấp tiêu đề sau khi rút gọn trong câu trả lời của bạn."
    if lang == Languages.EN:
        prompt += " Vui lòng trả lời bằng Tiếng Anh"
    return gemini_chat(prompt)
