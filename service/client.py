import grpc
import user_pb2
import user_pb2_grpc

def get_user_info(email):
    try:
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.UserRequest(email=email)
            response = stub.GetUserInfo(request)
            return response.name, response.age
    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.NOT_FOUND:
            print("User not found")
        else:
            print("Unexpected error:", e)
        return None, None

if __name__ == "__main__":
    name, age = get_user_info("Hai1@gmail.com")
    print(f"Name: {name}, Age: {age}")
