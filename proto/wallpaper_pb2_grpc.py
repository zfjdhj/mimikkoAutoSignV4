# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto import wallpaper_pb2 as proto_dot_wallpaper__pb2


class WallpaperStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAllAlbums = channel.unary_unary(
                '/com.mimikko.app.api.daylife.wallpaper.Wallpaper/GetAllAlbums',
                request_serializer=proto_dot_wallpaper__pb2.GetAllAlbumsRequest.SerializeToString,
                response_deserializer=proto_dot_wallpaper__pb2.GetAllAlbumsResponse.FromString,
                )
        self.GetWallpaperByAlbumId = channel.unary_unary(
                '/com.mimikko.app.api.daylife.wallpaper.Wallpaper/GetWallpaperByAlbumId',
                request_serializer=proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdRequest.SerializeToString,
                response_deserializer=proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdResponse.FromString,
                )


class WallpaperServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAllAlbums(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWallpaperByAlbumId(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_WallpaperServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetAllAlbums': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllAlbums,
                    request_deserializer=proto_dot_wallpaper__pb2.GetAllAlbumsRequest.FromString,
                    response_serializer=proto_dot_wallpaper__pb2.GetAllAlbumsResponse.SerializeToString,
            ),
            'GetWallpaperByAlbumId': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWallpaperByAlbumId,
                    request_deserializer=proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdRequest.FromString,
                    response_serializer=proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'com.mimikko.app.api.daylife.wallpaper.Wallpaper', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Wallpaper(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAllAlbums(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mimikko.app.api.daylife.wallpaper.Wallpaper/GetAllAlbums',
            proto_dot_wallpaper__pb2.GetAllAlbumsRequest.SerializeToString,
            proto_dot_wallpaper__pb2.GetAllAlbumsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWallpaperByAlbumId(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/com.mimikko.app.api.daylife.wallpaper.Wallpaper/GetWallpaperByAlbumId',
            proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdRequest.SerializeToString,
            proto_dot_wallpaper__pb2.GetWallpaperByAlbumIdResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
