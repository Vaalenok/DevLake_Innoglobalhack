import json
import re

import chardet
import requests


async def rating_feedback(feedback: str) -> json:
    global json_ready

    def get_streamed_response(api_url, payload, headers=None):
        response = requests.post(api_url, json=payload, headers=headers, stream=True)

        if response.status_code != 200:
            raise Exception(f"Ошибка API: {response.status_code} {response.text}")

        full_response = ""

        response.encoding = 'utf-8'

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                try:
                    data = json.loads(decoded_line.lstrip('data: '))
                    if 'choices' in data:
                        content = data['choices'][0]['delta'].get('content', '')
                        full_response += content
                except json.JSONDecodeError:
                    pass

        byte_string = full_response.encode('utf-8')
        detected_encoding = chardet.detect(byte_string)['encoding']
        decoded_response = byte_string.decode(detected_encoding)

        return decoded_response

    api_url = 'http://localhost:1337/v1/chat/completions'
    payload = {
        "messages": [
            {
                "content": f"{feedback}",
                "role": "user"
            }
        ],
        "model": "unsloth.F16",
        "stream": True,
        "max_tokens": 1024,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "temperature": 0.7,
        "top_p": 0.95
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    success = False

    while not success:
        try:
            complete_response = get_streamed_response(api_url, payload, headers)
            valid_json_str = re.sub(r"(?<={|,)\s*'([^']*?)'\s*:", r'"\1":', complete_response)
            valid_json_str = re.sub(r":\s*'([^']*?)'\s*(?=,|})", r':"\1"', valid_json_str)
            valid_json_str = valid_json_str.replace("'", '')
            valid_json_str = valid_json_str.replace("_", ' ')

            json_ready = json.loads(valid_json_str)
            success = True
        except Exception as e:
            pass
    return json_ready
