# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import Protos.BusGrpcService_pb2 as BusGrpcService__pb2


class BusGrpcEndpointStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetBus = channel.unary_unary(
                '/BusGrpcEndpoint.BusGrpcEndpoint/GetBus',
                request_serializer=BusGrpcService__pb2.BusRequest.SerializeToString,
                response_deserializer=BusGrpcService__pb2.Bus.FromString,
                )
        self.GetFob = channel.unary_unary(
                '/BusGrpcEndpoint.BusGrpcEndpoint/GetFob',
                request_serializer=BusGrpcService__pb2.Nfc.SerializeToString,
                response_deserializer=BusGrpcService__pb2.Fob.FromString,
                )
        self.CheckIn = channel.unary_unary(
                '/BusGrpcEndpoint.BusGrpcEndpoint/CheckIn',
                request_serializer=BusGrpcService__pb2.BusRequest.SerializeToString,
                response_deserializer=BusGrpcService__pb2.Response.FromString,
                )
        self.CheckOut = channel.unary_unary(
                '/BusGrpcEndpoint.BusGrpcEndpoint/CheckOut',
                request_serializer=BusGrpcService__pb2.BusRequest.SerializeToString,
                response_deserializer=BusGrpcService__pb2.Response.FromString,
                )


class BusGrpcEndpointServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetBus(self, request, context):
        """Bus gets initial data about itself, by id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFob(self, request, context):
        """Scanner gets Fob MAC Address by NFC ID
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckIn(self, request, context):
        """NFC scanned
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CheckOut(self, request, context):
        """Bluetooth device left
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BusGrpcEndpointServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetBus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetBus,
                    request_deserializer=BusGrpcService__pb2.BusRequest.FromString,
                    response_serializer=BusGrpcService__pb2.Bus.SerializeToString,
            ),
            'GetFob': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFob,
                    request_deserializer=BusGrpcService__pb2.Nfc.FromString,
                    response_serializer=BusGrpcService__pb2.Fob.SerializeToString,
            ),
            'CheckIn': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckIn,
                    request_deserializer=BusGrpcService__pb2.BusRequest.FromString,
                    response_serializer=BusGrpcService__pb2.Response.SerializeToString,
            ),
            'CheckOut': grpc.unary_unary_rpc_method_handler(
                    servicer.CheckOut,
                    request_deserializer=BusGrpcService__pb2.BusRequest.FromString,
                    response_serializer=BusGrpcService__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'BusGrpcEndpoint.BusGrpcEndpoint', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BusGrpcEndpoint(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetBus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BusGrpcEndpoint.BusGrpcEndpoint/GetBus',
            BusGrpcService__pb2.BusRequest.SerializeToString,
            BusGrpcService__pb2.Bus.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetFob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BusGrpcEndpoint.BusGrpcEndpoint/GetFob',
            BusGrpcService__pb2.Nfc.SerializeToString,
            BusGrpcService__pb2.Fob.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckIn(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BusGrpcEndpoint.BusGrpcEndpoint/CheckIn',
            BusGrpcService__pb2.BusRequest.SerializeToString,
            BusGrpcService__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CheckOut(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BusGrpcEndpoint.BusGrpcEndpoint/CheckOut',
            BusGrpcService__pb2.BusRequest.SerializeToString,
            BusGrpcService__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
