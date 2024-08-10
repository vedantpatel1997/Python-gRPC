import grpc
import greet_pb2
import greet_pb2_grpc
import asyncio

def get_client_stream_requests():
    while True:
        name = input("Please enter a name (or nothing to stop chatting): ")

        if name == "":
            break

        hello_request = greet_pb2.HelloRequest(greeting="Hello", name=name)
        yield hello_request

async def run():
    try:
        # Connect to the gRPC server
        channel = grpc.aio.insecure_channel('localhost:50051')
        
         # Define SSL credentials (empty for public servers)
        ssl_credentials = grpc.ssl_channel_credentials()

        # Connect to the gRPC server using secure_channel for HTTPS
        # channel = grpc.aio.secure_channel('pythongrpc-server.azurewebsites.net:443', ssl_credentials)
        
        stub = greet_pb2_grpc.GreeterStub(channel)

        print("1. SayHello - Unary")
        print("2. ParrotSaysHello - Server Side Streaming")
        print("3. ChattyClientSaysHello - Client Side Streaming")
        print("4. InteractingHello - Both Streaming")
        rpc_call = input("Which rpc would you like to make: ")

        if rpc_call == "1":
            hello_request = greet_pb2.HelloRequest(greeting="Bonjour", name="YouTube")
            hello_reply = await stub.SayHello(hello_request)
            print("SayHello Response Received:")
            print(hello_reply)
        elif rpc_call == "2":
            hello_request = greet_pb2.HelloRequest(greeting="Bonjour", name="YouTube")
            async for hello_reply in stub.ParrotSaysHello(hello_request):
                print("ParrotSaysHello Response Received:")
                print(hello_reply)
        elif rpc_call == "3":
            delayed_reply = await stub.ChattyClientSaysHello(get_client_stream_requests())
            print("ChattyClientSaysHello Response Received:")
            print(delayed_reply)
        elif rpc_call == "4":
            async for response in stub.InteractingHello(get_client_stream_requests()):
                print("InteractingHello Response Received: ")
                print(response)
        else:
            print("Invalid option")

    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(run())
