from __future__ import print_function
from tfyarn.clusterspecgen_client import ClusterSpecGenClient

import os
import socket
import tensorflow
import time


def createTrainServer(job_name, task_index, container_id=None, am_address=None):
    if container_id is None:
        container_id = os.environ['CONTAINER_ID']
    if am_address is None:
        am_address = os.environ['AM_ADDRESS']

    client = ClusterSpecGenClient(am_address)

    host = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    client.register_container(container_id, host, str(port), job_name, str(task_index))

    while True:
        time.sleep(0.2)
        cluster_spec_list = client.get_cluster_spec()
        if cluster_spec_list is None:
            print('createTrainServer: clusterSpec: None')
            pass
        elif len(cluster_spec_list) == 0:
            print('createTrainServer: clusterSpec: (empty)')
            pass
        else:
            break

    workers = []
    pses = []
    for container in cluster_spec_list:
        if container.jobName == 'worker':
            workers.append(container.ip + ':' + container.port)
        elif container.jobName == 'ps':
            pses.append(container.ip + ':' + container.port)
    cluster_spec_map = {'worker': workers, 'ps': pses}
    print('createTrainServer: clusterSpec: ', end='')
    print(cluster_spec_map)

    s.close()
    cluster = tensorflow.train.ClusterSpec(cluster_spec_map)
    server = tensorflow.train.Server(cluster, job_name=job_name, task_index=task_index)
    return server
