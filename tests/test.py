import threading
import tfyarn


def factory_test():
    threads = []

    for i in range(0, 3):
        thread = threading.Thread(target=tfyarn.createTrainServer, args=('worker', i, str(i), 'localhost:50051'))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    factory_test()
