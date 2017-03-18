from __future__ import print_function
from tfyarn.clusterspecgen_client import ClusterSpecGenClient

import os
import socket
import tensorflow
import time


def createClusterSpec(job_name, task_index, application_id=None, container_id=None, am_address=None):
    if application_id is None:
        application_id = os.environ['APPLICATION_ID']
    if container_id is None:
        container_id = os.environ['CONTAINER_ID']
    if am_address is None:
        am_address = os.environ['AM_ADDRESS']

    client = ClusterSpecGenClient(am_address)

    host = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    client.register_container(application_id, container_id, host, port, job_name, task_index)

    while True:
        time.sleep(0.2)
        cluster_spec_list = client.get_cluster_spec()
        if cluster_spec_list is None:
            print(container_id + ': createTrainServer: clusterSpec: None')
            pass
        elif len(cluster_spec_list) == 0:
            print(container_id + ': createTrainServer: clusterSpec: (empty)')
            pass
        else:
            break

    workers = []
    pses = []
    last_worker_task_id = -1
    last_ps_task_id = -1
    for container in cluster_spec_list:
        if container.jobName == 'worker':
            assert container.taskIndex == last_worker_task_id + 1
            last_worker_task_id = container.taskIndex
            workers.append(container.ip + ':' + str(container.port))
        elif container.jobName == 'ps':
            assert container.taskIndex == last_ps_task_id + 1
            last_ps_task_id = container.taskIndex
            pses.append(container.ip + ':' + str(container.port))

    cluster_spec_map = {'worker': workers, 'ps': pses}
    print(container_id + ': createTrainServer: clusterSpec: ', end='')
    print(cluster_spec_map)

    s.close()
    return tensorflow.train.ClusterSpec(cluster_spec_map)
