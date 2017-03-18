from __future__ import print_function

import grpc
import tfyarn.clusterspecgen_pb2 as csg
import tfyarn.clusterspecgen_pb2_grpc as csg_grpc


class ClusterSpecGenClient:
    def __init__(self, target):
        self.channel = grpc.insecure_channel(target)
        self.stub = csg_grpc.ClusterSpecGenStub(self.channel)

    def register_container(self, application_id, container_id, ip, port, job_name, task_index):
        container = csg.Container()
        container.applicationId = application_id
        container.containerId = container_id
        container.ip = ip
        container.port = port
        container.jobName = job_name
        container.taskIndex = task_index
        request = csg.RegisterContainerRequest(container=container)
        try:
            self.stub.RegisterContainer(request)
        except grpc.RpcError:
            return False
        return True

    def get_cluster_spec(self):
        request = csg.GetClusterSpecRequest()
        try:
            reply = self.stub.GetClusterSpec(request)
        except grpc.RpcError:
            return None
        return reply.clusterSpec
