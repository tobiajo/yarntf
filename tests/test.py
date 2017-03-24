import threading
import time
import yarntf


def factory_test():
    threads = []

    for i in range(0, 3):
        thread = threading.Thread(target=yarntf.createClusterSpec,
                                  args=('localhost:50051', '(appId)', 'worker', i))
        thread.start()
        threads.append(thread)
        time.sleep(2)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    factory_test()
