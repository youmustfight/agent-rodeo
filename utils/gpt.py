import json
import utils.env as env
import requests

COMPLETION_MODEL_3_5 = 'gpt-3.5-turbo'
COMPLETION_MODEL_4 = 'gpt-4'
TEMPERATURE_DEFAULT = 0.8 # going high to make it more volatile

def gpt_completion(prompt, model=COMPLETION_MODEL_3_5, temperature=TEMPERATURE_DEFAULT, max_tokens=2000, stop=['<<END>>']):
    max_retry = 3
    retry = 0
    while True:
        # print(f'[INFO] gpt_completion - {model}: COMPLETE THE "{prompt[0:120]}"...'.replace('\n', ' '))
        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={ 'Authorization': f'Bearer {env.env_get_open_ai_api_key()}', "content-type": "application/json" },
                json={
                    'model': model,
                    'messages': [
                        { 'role': 'system', 'content': 'You are a helpful assistant.' },
                        { 'role': 'user', 'content': prompt },
                    ],
                    'temperature': temperature,
                    # 'max_tokens': max_tokens,
                    # 'stop': stop
                },
            )
            response = response.json()
            if response.get('error') != None:
                raise response['error']
            text = response['choices'][0]['message']['content'].strip()
            return text
        except Exception as err:
            print('[Error]:', err, '\n', f'{prompt[0:320]}...')
            retry += 1
            if retry >= max_retry:
                return "[Error]: %s" % err


def extract_json_from_text_string(text_str: str):
    try:
        lp_idx = text_str.index('{')
        rp_idx = text_str.rindex('}')
        json_str = text_str[lp_idx:rp_idx+1]
        json_obj = json.loads(json_str)
        return json_obj 
    except Exception as err:
        print(err)
        return None