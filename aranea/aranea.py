import asyncio
import aiohttp


@asyncio.coroutine
def get_page(client, url):
    response = yield from client.get(url)
    if response.status == 200:
        return (yield from response.read())
    else:
        raise ValueError('need to handle bad responses, redirects...')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    try:
        content = loop.run_until_complete(get_page(
            client, 'http://aiohttp.readthedocs.org/en/stable/index.html'))
    except:
        raise
    else:
        print(content)
    finally:
        client.close()
