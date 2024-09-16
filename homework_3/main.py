import requests
import threading
import time


BASE_URL = "https://jsonplaceholder.typicode.com/posts/"


def fetch_data(url, lock):
    response = requests.get(url)

    if response.status_code == 200:
        with lock:
            with open('data.txt', 'a') as file:
                if threading.active_count() == 2:
                    file.write(response.text)
                    file.write('\n]\n')
                else:
                    file.write(response.text)
                    file.write(',\n')


def main():
    file = open("data.txt", "w")
    file.write("[\n")
    file.close()

    lock = threading.Lock()
    threads = list()

    for i in range(1, 78):
        thread = threading.Thread(target=fetch_data, args=(BASE_URL + str(i), lock))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    t = time.time()
    main()
    print(f"elapsed time: {time.time() - t}")
