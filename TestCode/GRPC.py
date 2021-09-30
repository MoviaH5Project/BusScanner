# Source: https://grpc.io/docs/languages/python/quickstart/

import grpc
import Protos.BusGrpcService_pb2_grpc
import Protos.BusGrpcService_pb2


def run():
    channel = grpc.insecure_channel('193.106.164.115:5300')
    stub = Protos.BusGrpcService_pb2_grpc.BusGrpcEndpointStub(channel)
    response = stub.GetBus(Protos.BusGrpcService_pb2.BusRequest(id=3))
    print("Greeter client received: " + response.make)


if __name__ == '__main__':
    run()
