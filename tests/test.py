import threading
import time
import tfyarn


def factory_test():
    threads = []

    for i in range(0, 3):
        time.sleep(0.25)
        thread = threading.Thread(target=tfyarn.createClusterSpec,
                                  args=('worker', i, 'A1', 'C' + str(2 - i), 'localhost:50051'))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    factory_test()
