from utils.gpt import gpt_completion


def writing(query, history):
    print('[TOOL] writing', query)
    res = gpt_completion(f"""
    ## CONTEXT:
    {history}
    ---
    ## QUERY:
    {query}
    ---
    ## RESPONSE: """)
    print('[TOOL] writing -> ', res)
    return res
