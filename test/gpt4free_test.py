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
            messages=[{"role": "user", "content": "你好"}],
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
        AItianhuSpace,
        AiAsk,
        Aichat,
        ChatBase,
        ChatForAi,
        ChatgptAi,
        ChatgptX,
        FakeGpt,
        FreeGpt,
        GPTalk,
        GptForLove,
        GptGo,
        Hashnode,
        MyShell,
        OpenaiChat,
        Theb,
        Vercel,
        You,
        Yqcloud,
        Acytoo,
        Aibn,
        Ails,
        Chatgpt4Online,
        ChatgptDemo,
        ChatgptDuo,
        ChatgptFree,
        ChatgptLogin,
        Cromicle,
        GptGod,
        Opchatgpts,
        Ylokh
    )

    # Usage:
    pds = [
        AItianhu,
        AItianhuSpace,
        AiAsk,
        Aichat,
        ChatBase,
        ChatForAi,
        ChatgptAi,
        ChatgptX,
        FakeGpt,
        FreeGpt,
        GPTalk,
        GptForLove,
        GptGo,
        Hashnode,
        MyShell,
        OpenaiChat,
        Theb,
        Vercel,
        You,
        Yqcloud,
        Acytoo,
        Aibn,
        Ails,
        Chatgpt4Online,
        ChatgptDemo,
        ChatgptDuo,
        ChatgptFree,
        ChatgptLogin,
        Cromicle,
        GptGod,
        Opchatgpts,
        Ylokh
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
    asyncio.run(run_all())
    run_all_pd()
