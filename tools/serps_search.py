import json
import requests
import utils.env as env

def serps_search(query, history):
    print('[TOOL] serps_search', query)
    response = requests.request(
        'POST',
        'https://google.serper.dev/search',
        headers={
            'X-API-KEY': env.env_get_serper_api_key(),
            'Content-Type': 'application/json'
        },
        data=json.dumps({
            'q': query,
            "autocorrect": False
        }),
    )
    result_arr = response.json()['organic']
    result = list(map(lambda obj: obj.get("snippet"), result_arr))
    # print('[TOOL] serps_search -> search_results', result)
    return result
