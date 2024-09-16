import asyncio
import aiohttp
import time


BASE_URL = "https://jsonplaceholder.typicode.com/posts/"


async def fetch_data(url, lock):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            async with lock:
                with open('data.txt', 'a') as f:
                    f.write(text)
                    f.write('\n')


async def main():
    file = open("data.txt", "w")
    file.close()

    lock = asyncio.Lock()

    funcs = [fetch_data(BASE_URL + str(i + 1), lock) for i in range(77)]

    await asyncio.gather(*funcs)

if __name__ == '__main__':
    t = time.time()
    asyncio.run(main())
    print(f"elapsed time: {time.time() - t}")
