from concurrent.futures import ThreadPoolExecutor
import requests
import threading


BASE_URL = "https://jsonplaceholder.typicode.com/posts/"


def fetch_data(url, lock):
    response = requests.get(url)

    if response.status_code == 200:
        with lock:
            with open('data.txt', 'a') as file:
                file.write(response.text)
                file.write('\n')
    else:
        with lock:
            with open('data.txt', 'a') as file:
                file.write(f"Cant fetch data for url: {url}")
                file.write('\n')


def main():
    file = open("data.txt", "w")
    file.close()

    lock = threading.Lock()

    with ThreadPoolExecutor(max_workers=77) as executor:
        for i in range(1, 77):
            executor.submit(fetch_data, BASE_URL + str(i), lock)


if __name__ == '__main__':
    main()
