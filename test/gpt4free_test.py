import g4f, asyncio

_providers = [
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.Bing,
    g4f.Provider.CodeLinkAva,
    g4f.Provider.DeepAi,
    g4f.Provider.GptGo,
    g4f.Provider.Wewordle,
    g4f.Provider.You,
    g4f.Provider.Yqcloud,
]


async def run_provider(provider: g4f.Provider.AsyncProvider):
    try:
        response = await provider.create_async(
            model=g4f.models.default.name,
            messages=[{"role": "user", "content": "你好"}],
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}:错误", e)


async def run_all():
    calls = [
        run_provider(provider) for provider in _providers
    ]
    await asyncio.gather(*calls)


def run_all_pd():
    from g4f.Provider import (
        AItianhu,
        Acytoo,
        Aichat,
        Ails,
        Aivvm,
        Bard,
        Bing,
        ChatBase,
        ChatgptAi,
        ChatgptLogin,
        CodeLinkAva,
        DeepAi,
        H2o,
        HuggingChat,
        Opchatgpts,
        OpenAssistant,
        OpenaiChat,
        Raycast,
        Theb,
        Vercel,
        Vitalentum,
        Wewordle,
        Ylokh,
        You,
        Yqcloud,
    )

    # Usage:
    pds = [
        AItianhu,
        Aivvm,
        ChatBase,
        ChatgptAi,
        DeepAi,
        Vitalentum,
        Yqcloud,
    ]
    for provider in pds:
        try:
            response = g4f.ChatCompletion.create(model="gpt-3.5-turbo",
                                                 provider=provider,
                                                 messages=[{"role": "user", "content": "你好"}],
                                                 stream=False, )
            print(f"{provider.__name__}:", response)
        except Exception as e:
            print(f"{provider.__name__}:错误", e)



if __name__ == '__main__':
    asyncio.run(run_all())
    run_all_pd()
