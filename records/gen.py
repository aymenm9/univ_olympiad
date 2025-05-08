import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def generate(deths)->str:
    load_dotenv()
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    text = ''
    for death in deths:
        text += f"""
        [birth date:{death.birth_date}, birth place:{death.birth_wilaya}, {death.birth_commune}, death date:{death.death_date}, death place:{death.death_wilaya}, {death.death_commune}, death cause:{death.death_cause}, Description:{death.description}],
        """
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=text),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""you will get alist of deaths records, give a short analytic summary on tham """),
        ],
    )

    responce = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,)
    return responce.text