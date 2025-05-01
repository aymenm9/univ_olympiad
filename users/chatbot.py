import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
load_dotenv()

def chatbot(message:str,chat_history:list = []):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-flash-preview-04-17"
    text = message
    contents = []
    for msg in chat_history:
        print(msg)
        contents.append(
            types.Content(
                role=msg['role'],
                parts=[
                    types.Part.from_text(text=msg['parts'][0]['text']),
                ],
            )
        )   
    
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),
            ],
        ),
    )
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""you are a helpfull medical chatbot assistant"""),
        ],
    )

    responce = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,
        )
    return responce.text