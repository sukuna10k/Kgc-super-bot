from asyncio import gather
from httpx import AsyncClient, Timeout

# HTTPx Async Client
fetch = AsyncClient(
    https2=True
    verify=False,
    headers={
        "Accept-Language": "en-US,en;q=0.9,id-ID;q=0.8,id;q=0.7",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)


async def get(url: str, *args, **kwargs):
    try:
        resp = await fetch.get(url, *args, **kwargs)
        data = await resp.json()
    except Exception:
        data = await resp.text()
    return data


async def head(url: str, *args, **kwargs):
    try:
        resp = await fetch.head(url, *args, **kwargs)
        data = await resp.json()
    except Exception:
        data = await resp.text()
    return data


async def post(url: str, *args, **kwargs):
    try:
        resp = await fetch.post(url, *args, **kwargs)
        data = await resp.json()
    except Exception:
        data = await resp.text()
    return data


async def multiget(url: str, times: int, *args, **kwargs):
    return await gather(*[get(url, *args, **kwargs) for _ in range(times)])


async def multihead(url: str, times: int, *args, **kwargs):
    return await gather(*[head(url, *args, **kwargs) for _ in range(times)])


async def multipost(url: str, times: int, *args, **kwargs):
    return await gather(*[post(url, *args, **kwargs) for _ in range(times)])


async def resp_get(url: str, *args, **kwargs):
    return await fetch.get(url, *args, **kwargs)


async def resp_post(url: str, *args, **kwargs):
    return await fetch.post(url, *args, **kwargs)
