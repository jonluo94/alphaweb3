import g4f, asyncio


def run_all_pd():
    from g4f.Provider import (
        AiChatOnline,
        Aura,
        ChatBase,
        ChatForAi,
        ChatgptAi,
        ChatgptDemo,
        ChatgptNext,
        Chatxyz,
        GPTalk,
        GeminiProChat,
        Gpt6,
        GptChatly,
        GptForLove,
        GptGo,
        GptTalkRu,
        Koala,
        OnlineGpt,
        Poe,
        You,
    )

    # Usage:
    pds = [
        AiChatOnline,
        Aura,
        ChatBase,
        ChatForAi,
        ChatgptAi,
        ChatgptDemo,
        ChatgptNext,
        Chatxyz,
        GPTalk,
        GeminiProChat,
        Gpt6,
        GptChatly,
        GptForLove,
        GptGo,
        GptTalkRu,
        Koala,
        OnlineGpt,
        Poe,
        You,
    ]
    for provider in pds:
        try:
            # Set with provider
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=provider,
                messages=[{"role": "user", "content": "你好"}],
                stream=False,
            )

            print(f"{provider.__name__}:", response)
        except Exception as e:
            print(f"{provider.__name__}:错误", e)


if __name__ == '__main__':
    run_all_pd()
