# grpc_client_serve
1. Tạo file mô tả message và service -> user.proto
2. Compile file này để sinh ra các class stub sử dụng trong client và server
   python3 -m grpc_tools.protoc --proto_path=./proto --python_out=./service --grpc_python_out=./serservice user.proto

