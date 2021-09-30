# Source: https://grpc.io/docs/languages/python/quickstart/

import grpc
import Protos.BusGrpcService_pb2_grpc
import Protos.BusGrpcService_pb2
from LoggerInterface import LoggerInterface


class GRPCCaller:
    def __init__(self, logger: LoggerInterface):
        self.channel = grpc.insecure_channel('193.106.164.115:5300')
        self.stub = Protos.BusGrpcService_pb2_grpc.BusGrpcEndpointStub(self.channel)
        self.logger = logger
        self.bus_id = 9

    def request(self, endpoint, *args):
        try:
            response = endpoint(*args)
            self.logger.log("Greeter client received response ", self.logger.INFO)
            return response
        except Exception as exception:
            self.logger.log_exception(message='GRCP error', exception=exception)

    def get_bus(self):
        return self.request(self.stub.GetBus, Protos.BusGrpcService_pb2.BusRequest(id=self.bus_id))

    def get_fob(self, nfc_id):
        return self.request(self.stub.GetFob, Protos.BusGrpcService_pb2.Nfc(nfc_id=nfc_id))

    def check_in(self):
        return self.request(self.stub.CheckIn, Protos.BusGrpcService_pb2.BusRequest(id=self.bus_id))

    def check_out(self):
        return self.request(self.stub.CheckOut, Protos.BusGrpcService_pb2.BusRequest(id=self.bus_id))
