import requests

from utils.gpt import gpt_completion

def wikipedia_pages_search(query, history):
    print('[TOOL] wikipedia_pages_search', query)
    # REQUEST
    # --- matching terms
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "opensearch",
            "search": query,
        },
    )
    data = response.json()
    # RETURNs list of page titles that we found successfully. it's a str[] in a nested arr returned (also can pass back the )
    results = list(zip(data[1], data[3]))
    # print('[TOOL] wikipedia_pages_search -> ', results)
    return results


def wikipedia_page_content_retrieval(query, history):
    print('[TOOL] wikipedia_search', query)
    # REQUEST
    # --- page
    response = requests.get(
        "https://en.wikipedia.org/w/api.php",
        params={
            "action": "query",
            "format": "json",
            "titles": query,
            "prop": "extracts",
            "explaintext": True,  # Plain text
        },
    )
    data = response.json()
    # EXTRACT
    # --- if missing
    if data.get('query').get('pages').get('-1') != None:
        print('[TOOL] wikipedia_search: none found -> ', data)
        return f'No page found on Wikipedia for query, "{data["query"]["pages"]["-1"]["title"]}"'
    # --- if not
    page_id = next(iter(data["query"]["pages"].keys()))
    page_content = data["query"]["pages"][page_id]["extract"]

    # CONDENSE
    page_content = gpt_completion("CONTENT: {page_content}\n\n QUERY: {query}\n\n SUMMARY: ")
    
    # RETURN
    # print('[TOOL] wikipedia_search: found -> ', page_content)
    return page_content
