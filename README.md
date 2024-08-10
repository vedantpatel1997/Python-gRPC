Here is the updated README with the revised Azure deployment instructions:

---

# README

## Overview

This project demonstrates a basic setup using gRPC and aiohttp in Python. The project consists of:

1. **gRPC Server (`greet_server.py`)**: A standalone server handling gRPC requests.
2. **Integrated Server (`app.py`)**: An application combining an aiohttp HTTP server and a gRPC server.
3. **Client Code (`greet_client.py`)**: A script to interact with the gRPC server.
4. **Protocol Definition (`greet.proto`)**: Defines the gRPC service and messages.

## Project Structure

- `app.py`: Contains the combined aiohttp HTTP server and gRPC server implementation.
- `greet_server.py`: Contains the standalone gRPC server implementation.
- `greet_client.py`: A client script to interact with the gRPC server.
- `greet.proto`: Protocol buffer file defining the gRPC service.

## Setup and Installation

### Prerequisites

- Python 3.7 or higher
- `pip` for package management

### Install Dependencies

Ensure you have the necessary Python packages installed. Run:

```bash
pip install grpcio grpcio-tools aiohttp
```

### Generate Python Code from Protobuf

The `greet.proto` file defines the gRPC service. Generate the Python code for the gRPC service:

1. **Create a `protos` directory** to hold `greet.proto`.
2. **Save the `greet.proto` file** in the `protos` directory.

Run the following command to generate the gRPC Python files:

```bash
python -m grpc_tools.protoc -I./protos --python_out=./ --grpc_python_out=./ protos/greet.proto
```

This command generates `greet_pb2.py` and `greet_pb2_grpc.py`.

## Running Locally

### Running the Combined Server (`app.py`)

`app.py` integrates an aiohttp HTTP server with a gRPC server.

1. **Start the Application**

   Run the `app.py` file:

   ```bash
   python app.py
   ```

   This starts the HTTP server on port 8000 and the gRPC server on port 50051.

2. **Verify the HTTP Server**

   Open your browser or use `curl` to access:

   ```bash
   curl http://localhost:8000
   ```

   You should see a JSON response:

   ```json
   {"msg": "Hello world, from aiohttp HTTP server"}
   ```

### Running the Standalone gRPC Server (`greet_server.py`)

`greet_server.py` provides a standalone gRPC server implementation.

1. **Start the gRPC Server**

   Run the `greet_server.py` file:

   ```bash
   python greet_server.py
   ```

   This starts the gRPC server on port 50051.

### Running the Client (`greet_client.py`)

`greet_client.py` is used to test gRPC interactions. You can run the client locally while the server is hosted on the cloud.

1. **Update Client Configuration**

   Modify `greet_client.py` to point to your cloud server's hostname and port. For a secure connection, configure SSL/TLS as needed.

2. **Start the Client**

   Run the `greet_client.py` file:

   ```bash
   python greet_client.py
   ```

   Follow the prompts to select an RPC call and interact with the gRPC server.

#### Secure Connection

If the gRPC server on the cloud uses SSL/TLS:

1. Update `greet_client.py` to use SSL/TLS credentials.
2. Make sure to provide the correct certificate paths or configurations.

#### Insecure Connection

If the gRPC server does not use SSL/TLS:

1. Ensure that `greet_client.py` is configured to connect without SSL/TLS.

## Azure Deployment Configuration

### Environment Variables

Set the following environment variables for your Azure deployment:

- **WEBSITES_PORT**: Set to `8000`
- **HTTP20_ONLY_PORT**: Set to `50051`

### HTTP Settings

1. **Configuration -> General Settings**

   - Set **HTTP Version** to `2.0`
   - Set **HTTP 2.0 Proxy** to `"gRPC ONLY"`

2. **Startup Command**

   Set the startup command to:

   ```bash
   python app.py
   ```

## Troubleshooting

- **Connection Issues**: Ensure that the server is running and accessible at the specified port.
- **Dependency Errors**: Verify that all required packages are installed and compatible.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to modify any sections as needed!
