from __future__ import print_function

import os
import socket
import subprocess
import sys
import time

import tensorflow

from yarntf.clusterspecgenerator_client import ClusterSpecGeneratorClient


def createClusterSpec(am_address, application_id, job_name, task_index):
    client = ClusterSpecGeneratorClient(am_address)

    host = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]

    tb_port = -1
    if "TENSORBOARD" in os.environ:
        tb_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tb_s.bind(('', 0))
        tb_port = tb_s.getsockname()[1]
        tb_s.close()
        subprocess.Popen(["tensorboard --logdir=" + os.environ["TB_DIR"] + " --port=" + str(tb_port) + " --debug"])

    registered = client.register_container(application_id, host, port, job_name, task_index, tb_port)
    print(job_name + str(task_index) + ': createClusterSpec(): registered: ' + str(registered))
    assert registered

    for i in range(0, 30):
        time.sleep(1)
        cluster_spec_list = client.get_cluster_spec(application_id)
        if cluster_spec_list is None:
            print(job_name + str(task_index) + ': createClusterSpec(): clusterSpec: None', file=sys.stderr)
            sys.exit(1)
        elif len(cluster_spec_list) == 0:
            print(job_name + str(task_index) + ': createClusterSpec(): clusterSpec: (empty)')
        else:
            break
        if i == 29:
            print(job_name + str(task_index) + ': createClusterSpec(): clusterSpec: TIMEOUT', file=sys.stderr)
            sys.exit(1)

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
    print(job_name + str(task_index) + ': createClusterSpec(): clusterSpec: ', end='')
    print(cluster_spec_map)

    s.close()
    return tensorflow.train.ClusterSpec(cluster_spec_map)


def createClusterServer():
    am_address = os.environ['AM_ADDRESS']
    application_id = os.environ['APPLICATION_ID']
    job_name = os.environ['JOB_NAME']
    task_index = int(os.environ['TASK_INDEX'])
    cluster = createClusterSpec(am_address, application_id, job_name, task_index)
    return cluster, tensorflow.train.Server(cluster, job_name=job_name, task_index=task_index)
