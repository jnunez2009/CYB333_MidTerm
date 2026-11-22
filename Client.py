"""Midterm Part 1: Client Communication to Server"""
import socket

HOST = "127.0.0.1"
PORT = 5000
TIMEOUT = 5

def main():
    try:
        # Connect to the TCP server.
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as client:
            print(f"Connected to server at {HOST}:{PORT}")

            with client.makefile("r", encoding="utf-8") as reader:
                while True:
                    message = input(
                        "Enter a message (or 'exit' to disconnect): "
                    )

                    # Send the message to the server.
                    client.sendall((message + "\n").encode("utf-8"))

                    # Receive the server's response.
                    reply = reader.readline()

                    if not reply:
                        print("Server disconnected.")
                        break

                    print(f"Server: {reply.rstrip()}")

                    if message.lower() == "exit":
                        print("Disconnected from server cleanly.")
                        break

    except ConnectionRefusedError:
        print("Connection failed: server is not running. Start server.py first.")
    except socket.timeout:
        print("Connection timed out: server did not respond in time.")
    except (ConnectionResetError, BrokenPipeError):
        print("Connection lost: server closed the connection unexpectedly.")
    except (EOFError, KeyboardInterrupt):
        print("\nClient stopped by user.")
    except OSError as error:
        print(f"Network error: {error}")

if __name__ == "__main__":
    main()
