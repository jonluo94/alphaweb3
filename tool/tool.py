import json

import requests

search_top = 1
access_key = "6d5c98ff7926e21be71508009bdf99df"


class SerpstackSearch:
    def search(query: str = ""):
        params = {
            'access_key': access_key,
            'query': query
        }
        api_result = requests.get('http://api.serpstack.com/search', params)
        api_response = api_result.json()
        return process_response(api_response)


def process_response(res: dict) -> str:
    """Process response from SerpAPI."""
    if "error" in res.keys():
        raise ValueError(f"Got error from SerpAPI: {res['error']}")
    if "answer_box" in res.keys() and type(res["answer_box"]) is list:
        res["answer_box"] = res["answer_box"][0]
    if "answer_box" in res.keys() and "answer" in res["answer_box"].keys():
        toret = res["answer_box"]["answer"]
    elif "answer_box" in res.keys() and "snippet" in res["answer_box"].keys():
        toret = res["answer_box"]["snippet"]
    elif "answer_box" in res.keys() and "snippet_highlighted_words" in res["answer_box"].keys():
        toret = res["answer_box"]["snippet_highlighted_words"][0]
    elif "sports_results" in res.keys() and "game_spotlight" in res["sports_results"].keys():
        toret = res["sports_results"]["game_spotlight"]
    elif "knowledge_graph" in res.keys() and "description" in res["knowledge_graph"].keys():
        toret = res["knowledge_graph"]["description"]
    else:
        toret = ""
        i = 0
        for ores in res["organic_results"]:
            if i >= search_top:
                break
            if "snippet" in ores and ores["snippet"] != "":
                toret += ores["snippet"] + "\n"
                i += 1
        if toret == "":
            toret = "No good search result found"

    return toret


if __name__ == "__main__":
    r = SerpstackSearch.search("中国的首都是什么")
    print(r)
