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

    model = "gemini-2.5-flash-preview-04-17"
    text = ''
    for death in deths:
        text += f"""
        [date_of_birth:{death.date_of_birth}, place_of_birth:{death.place_of_birth}, date_of_death:{death.date_of_deth}, cause_of_death:{death.death_cause}],
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
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""you will get alist of deaths records, give a short analytic summary on tham """),
        ],
    )

    responce = client.models.generate_content(
        model=model,
        contents=contents,
        config=generate_content_config,)
    return responce.text