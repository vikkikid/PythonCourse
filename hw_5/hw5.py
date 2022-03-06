import os
import time
import aiohttp
import asyncio

# useful sources: 
# https://docs.aiohttp.org/en/stable/client_quickstart.html
# https://stackoverflow.com/questions/40143289/why-do-most-asyncio-examples-use-loop-run-until-complete


if __name__ == '__main__':
    path = 'artifacts'
    easy = path + '/easy'
    os.makedirs(easy, exist_ok=True)
    
    src = 'https://thiscatdoesnotexist.com/'
    n = 15
    wait = 1
    
    async def get_cats():
        async with aiohttp.ClientSession() as session:
            for i in range(n):
                async with session.get(src) as resp:
                    with open(f"{easy}/{i + 1}.png", "bw") as file:
                        file.write((await resp.content.read()))
                time.sleep(wait)

    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(get_cats())
    