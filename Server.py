"""Midterm Part 1: Server Communnication to Client"""
import socket

HOST = "127.0.0.1"
PORT = 5000
BUFFER_SIZE = 1024

def main():
    try:
        # Create the TCP server socket.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((HOST, PORT))
            server.listen(1)

            print(f"Server listening on {HOST}:{PORT}")
            print("Waiting for a client...")

            # Accept a connection from the client.
            with server.accept()[0] as connection:
                print("Client connected.")

                with connection.makefile("r", encoding="utf-8") as reader:
                    while True:
                        message = reader.readline()

                        if not message:
                            print("Client disconnected.")
                            break

                        message = message.rstrip("\r\n")

                        if message.lower() == "exit":
                            connection.sendall(b"Goodbye!\n")
                            print("Client requested disconnection.")
                            break

                        print(f"Client: {message}")

                        # Send a response back to the client.
                        reply = f"Server received: {message}\n"
                        connection.sendall(reply.encode("utf-8"))

            print("Connection closed. Server shutting down.")

    except OSError as error:
        print(f"Server error: {error}")
    except KeyboardInterrupt:
        print("\nServer stopped by user.")

if __name__ == "__main__":
    main()
