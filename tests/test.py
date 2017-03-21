import threading
import time
import yarntf


def factory_test():
    threads = []

    for i in range(0, 3):
        time.sleep(0.25)
        thread = threading.Thread(target=yarntf.createClusterSpec,
                                  args=('worker', i, 'A1', 'localhost:50053'))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    factory_test()
