import time
import grpc
from aiohttp import web
from concurrent import futures
import asyncio
import greet_pb2
import greet_pb2_grpc

# gRPC Servicer Implementation
class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("SayHello Request Made:")
        print(request)
        hello_reply = greet_pb2.HelloReply()
        hello_reply.message = f"{request.greeting} {request.name}"
        return hello_reply
    
    def ParrotSaysHello(self, request, context):
        print("ParrotSaysHello Request Made:")
        print(request)
        for i in range(3):
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name} {i + 1}"
            yield hello_reply
            time.sleep(3)

    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print("ChattyClientSaysHello Request Made:")
            print(request)
            delayed_reply.request.append(request)
        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    def InteractingHello(self, request_iterator, context):
        for request in request_iterator:
            print("InteractingHello Request Made:")
            print(request)
            hello_reply = greet_pb2.HelloReply()
            hello_reply.message = f"{request.greeting} {request.name}"
            yield hello_reply

# Aiohttp Application
class Application(web.Application):
    def __init__(self):
        super().__init__()
        self.grpc_task = None
        self.grpc_server = GrpcServer()
        self.add_routes()
        self.on_startup.append(self.__on_startup())
        self.on_shutdown.append(self.__on_shutdown())

    def __on_startup(self):
        async def _on_startup(app):
            self.grpc_task = asyncio.ensure_future(self.grpc_server.start())
        return _on_startup

    def __on_shutdown(self):
        async def _on_shutdown(app):
            await self.grpc_server.stop()
            self.grpc_task.cancel()
            await self.grpc_task
        return _on_shutdown

    def add_routes(self):
        self.router.add_get('/', self.index)

    async def index(self, request):
        data = {'msg': 'Hello world, from aiohttp HTTP server'}
        return web.json_response(data)

    def run(self):
        print('HTTP server starting on port 8000')
        web.run_app(self, host='0.0.0.0', port=8000)

# gRPC Server
class GrpcServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), self.server)
        self.server.add_insecure_port('[::]:50051')

    async def start(self):
        print('gRPC server starting on port 50051')
        self.server.start()

    async def stop(self):
        await self.server.stop(grace=0)

# Run both servers
if __name__ == "__main__":
    app = Application()
    app.run()
