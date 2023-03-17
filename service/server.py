import grpc
from concurrent import futures
from neo4j import GraphDatabase
import user_pb2
import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def GetUserInfo(self, request, context):
        email = request.email
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "hai1"))
        with driver.session() as session:
            result = session.run("MATCH (e:Email {address: $email})<-[:HAS_EMAIL]-(u:User) RETURN u.name, u.age", email=email)
            record = result.single()
            if record:
                name = record[0]
                age = record[1]
                return user_pb2.UserResponse(name=name, age=age)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.UserResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
