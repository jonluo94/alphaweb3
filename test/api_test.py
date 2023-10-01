import requests

headers = {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept': 'application/json'
}



def test_openai_model():
    # grgbrain/upload_knowledge_data
    r = requests.get('http://127.0.0.1:7861/v1/models')
    print(r.json())

def test_openai_chat():
    # grgbrain/upload_knowledge_data
    r = requests.post('http://127.0.0.1:7861/v1/chat/completions', json={
        "model": "yqcloud",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    }, headers=headers)
    print(r.json())

if __name__ == '__main__':
    test_openai_model()
    test_openai_chat()