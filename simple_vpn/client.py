import socket
from cryptography.fernet import Fernet

KEY = b'PFFzFB5FAsCrMWwR5eq7WZ6oF3Qmbe536A7Mt-SIM14='

def start_client(host='localhost', port=9999):
    """Connect to VPN server and communicate"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print(f"[✓] Connected to VPN server at {host}:{port}")

        fernet = Fernet(KEY)

        while True:
            try:
                message = input("[You]: ").strip()
                if message.lower() == 'exit':
                    print("[!] Closing connection...")
                    break
                    
                if not message:
                    continue

                client.send(fernet.encrypt(message.encode()))

                encrypted_response = client.recv(1024)
                if not encrypted_response:
                    print("[!] Server closed connection")
                    break

                response = fernet.decrypt(encrypted_response).decode()
                print(f"[Server]: {response}")
                
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user")
                break
            except Exception as e:
                print(f"[✗] Error: {e}")
                break

    except ConnectionRefusedError:
        print(f"[✗] Could not connect to server at {host}:{port}")
    except Exception as e:
        print(f"[✗] Connection error: {e}")
    finally:
        client.close()
        print("[✓] Disconnected")

if __name__ == "__main__":
    start_client()
