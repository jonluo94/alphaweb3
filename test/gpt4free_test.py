import g4f, asyncio

_providers = [
    g4f.Provider.Aichat,
    g4f.Provider.ChatBase,
    g4f.Provider.Bing,
    g4f.Provider.GptGo,
    g4f.Provider.You,
    g4f.Provider.Yqcloud,
]


async def run_provider(provider: g4f.Provider.BaseProvider):
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": "Hello"}],
            provider=provider,
        )
        print(f"{provider.__name__}:", response)
    except Exception as e:
        print(f"{provider.__name__}:", e)


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
        Bard,
        Bing,
        ChatBase,
        ChatgptAi,
        H2o,
        HuggingChat,
        OpenAssistant,
        OpenaiChat,
        Raycast,
        Theb,
        Vercel,
        Vitalentum,
        Ylokh,
        You,
        Yqcloud,
    )

    # Usage:
    pds = [
        AItianhu,
        Acytoo,
        Aichat,
        Ails,
        Bard,
        Bing,
        ChatBase,
        ChatgptAi,
        H2o,
        HuggingChat,
        OpenAssistant,
        OpenaiChat,
        Raycast,
        Theb,
        Vercel,
        Vitalentum,
        Ylokh,
        You,
        Yqcloud,
    ]
    for provider in pds:
        try:
            # Set with provider
            response = g4f.ChatCompletion.create(
                model="gpt-3.5-turbo",
                provider=g4f.Provider.Aichat,
                messages=[{"role": "user", "content": "Hello"}],
                stream=False,
            )

            print(f"{provider.__name__}:", response)
        except Exception as e:
            print(f"{provider.__name__}:错误", e)



if __name__ == '__main__':
    asyncio.run(run_all())
    run_all_pd()
