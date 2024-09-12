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

    for i in range(1, 78):
        thread = threading.Thread(target=fetch_data, args=(BASE_URL + str(i), lock))
        thread.start()


if __name__ == '__main__':
    main()
