import grpc
import greet_pb2
import greet_pb2_grpc
import asyncio
from flask import Flask, request, jsonify

app = Flask(__name__)

async def handle_rpc_call(rpc_call):
    try:
        # Connect to the gRPC server
        channel = grpc.aio.insecure_channel('greet-server:50051')
        stub = greet_pb2_grpc.GreeterStub(channel)

        if rpc_call == "1":
            hello_request = greet_pb2.HelloRequest(greeting="Bonjour", name="YouTube")
            hello_reply = await stub.SayHello(hello_request)
            return {"response": hello_reply.message}
        elif rpc_call == "2":
            hello_request = greet_pb2.HelloRequest(greeting="Bonjour", name="YouTube")
            responses = []
            async for hello_reply in stub.ParrotSaysHello(hello_request):
                responses.append(hello_reply.message)
            return {"responses": responses}
        elif rpc_call == "3":
            def get_client_stream_requests():
                requests = [
                    greet_pb2.HelloRequest(greeting="Hello", name="Client1"),
                    greet_pb2.HelloRequest(greeting="Hello", name="Client2")
                ]
                for req in requests:
                    yield req

            delayed_reply = await stub.ChattyClientSaysHello(get_client_stream_requests())
            return {"response": delayed_reply.message}
        elif rpc_call == "4":
            def get_client_stream_requests():
                requests = [
                    greet_pb2.HelloRequest(greeting="Hello", name="Client1"),
                    greet_pb2.HelloRequest(greeting="Hello", name="Client2")
                ]
                for req in requests:
                    yield req

            responses = []
            async for response in stub.InteractingHello(get_client_stream_requests()):
                responses.append(response.message)
            return {"responses": responses}
        else:
            return {"error": "Invalid option"}

    except grpc.RpcError as e:
        return {"error": f"gRPC error: {e.code()} - {e.details()}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

@app.route("/rpc", methods=["POST"])
def rpc_handler():
    data = request.get_json()
    rpc_call = data.get("rpc_call")
    if not rpc_call:
        return jsonify({"error": "rpc_call is required"}), 400

    # Run the gRPC call asynchronously and return the result
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(handle_rpc_call(rpc_call))
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
