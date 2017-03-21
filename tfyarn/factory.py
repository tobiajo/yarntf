from __future__ import print_function
from tfyarn.clusterspecgenerator_client import ClusterSpecGeneratorClient

import os
import socket
import tensorflow
import time


def createClusterSpec(job_name, task_index, application_id=None, am_address=None):
    if application_id is None:
        application_id = os.environ['APPLICATION_ID']
    if am_address is None:
        am_address = os.environ['AM_ADDRESS']

    client = ClusterSpecGeneratorClient(am_address)

    host = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    client.register_container(application_id, host, port, job_name, task_index)

    while True:
        time.sleep(0.2)
        cluster_spec_list = client.get_cluster_spec()
        if cluster_spec_list is None:
            print(job_name + str(task_index) + ': createTrainServer: clusterSpec: None')
            pass
        elif len(cluster_spec_list) == 0:
            print(job_name + str(task_index) + ': createTrainServer: clusterSpec: (empty)')
            pass
        else:
            break

    workers = []
    pses = []
    last_worker_task_index = -1
    last_ps_task_index = -1
    for container in cluster_spec_list:
        if container.jobName == 'worker':
            assert container.taskIndex == last_worker_task_index + 1
            last_worker_task_index = container.taskIndex
            workers.append(container.ip + ':' + str(container.port))
        elif container.jobName == 'ps':
            assert container.taskIndex == last_ps_task_index + 1
            last_ps_task_index = container.taskIndex
            pses.append(container.ip + ':' + str(container.port))

    cluster_spec_map = {'worker': workers, 'ps': pses}
    print(job_name + str(task_index) + ': createTrainServer: clusterSpec: ', end='')
    print(cluster_spec_map)

    s.close()
    return tensorflow.train.ClusterSpec(cluster_spec_map)
