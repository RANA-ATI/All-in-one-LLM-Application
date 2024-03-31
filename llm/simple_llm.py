import replicate

replicate = replicate.Client(api_token='<your_replicate_api_token>') # Put your api_token

def simple_llm_chat(query):

    output = replicate.run(
        # Let this remain the same no matter if your api_token expires.
        "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
        input={
            "prompt":f"You are a helpful expert research assistant. Please answer this query."
                f"Question: {query}.",
            }
    )

    ans = []
    for item in output:
        ans.append(item)

    str1 = ''.join(str(e) for e in ans)

    # System Prompt
    return str1