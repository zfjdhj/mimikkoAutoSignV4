# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import activitynew_pb2 as proto_dot_activitynew__pb2


class ActivityNewStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListActivityNew = channel.unary_unary(
                '/com.mimikko.app.api.daylife.activity.ActivityNew/ListActivityNew',
                request_serializer=proto_dot_activitynew__pb2.ListActivityNewRequest.SerializeToString,
                response_deserializer=proto_dot_activitynew__pb2.ListActivityNewResponse.FromString,
                )
        self.GetTodayAvailableSign = channel.unary_unary(
                '/com.mimikko.app.api.daylife.activity.ActivityNew/GetTodayAvailableSign',
                request_serializer=proto_dot_activitynew__pb2.GetTodayAvailableSignRequest.SerializeToString,
                response_deserializer=proto_dot_activitynew__pb2.GetTodayAvailableSignResponse.FromString,
                )


class ActivityNewServicer(object):
    """Missing associated documentation comment in .proto file."""

    def ListActivityNew(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetTodayAvailableSign(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ActivityNewServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListActivityNew': grpc.unary_unary_rpc_method_handler(
                    servicer.ListActivityNew,
                    request_deserializer=proto_dot_activitynew__pb2.ListActivityNewRequest.FromString,
                    response_serializer=proto_dot_activitynew__pb2.ListActivityNewResponse.SerializeToString,
            ),
            'GetTodayAvailableSign': grpc.unary_unary_rpc_method_handler(
                    servicer.GetTodayAvailableSign,
                    request_deserializer=proto_dot_activitynew__pb2.GetTodayAvailableSignRequest.FromString,
                    response_serializer=proto_dot_activitynew__pb2.GetTodayAvailableSignResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.mimikko.app.api.daylife.activity.ActivityNew', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ActivityNew(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def ListActivityNew(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mimikko.app.api.daylife.activity.ActivityNew/ListActivityNew',
            proto_dot_activitynew__pb2.ListActivityNewRequest.SerializeToString,
            proto_dot_activitynew__pb2.ListActivityNewResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetTodayAvailableSign(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mimikko.app.api.daylife.activity.ActivityNew/GetTodayAvailableSign',
            proto_dot_activitynew__pb2.GetTodayAvailableSignRequest.SerializeToString,
            proto_dot_activitynew__pb2.GetTodayAvailableSignResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
