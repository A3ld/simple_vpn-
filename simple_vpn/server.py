import socket
import threading
from cryptography.fernet import Fernet
import time

KEY = b'PFFzFB5FAsCrMWwR5eq7WZ6oF3Qmbe536A7Mt-SIM14='
fernet = Fernet(KEY)
client_counter = 0
clients = {}

def handle_client(conn, addr, client_id):
    """Handle individual client connection"""
    print(f"[✓] Client {client_id} connected from {addr}")
    clients[client_id] = {'addr': addr, 'conn': conn}
    
    try:
        while True:
            encrypted_data = conn.recv(1024)
            if not encrypted_data:
                print(f"[!] Client {client_id} disconnected")
                break

            try:
                message = fernet.decrypt(encrypted_data).decode()
                print(f"[Client {client_id}]: {message}")
                
                # Echo response for testing
                response = f"Echo: {message}"
                conn.send(fernet.encrypt(response.encode()))
                
            except Exception as e:
                print(f"[✗] Error decrypting message from Client {client_id}: {e}")
                conn.send(fernet.encrypt(b"Error: Invalid message"))

    except Exception as e:
        print(f"[✗] Error handling Client {client_id}: {e}")
    finally:
        conn.close()
        del clients[client_id]
        print(f"[✓] Client {client_id} session closed")

def start_server(host='localhost', port=9999):
    """Start VPN server with multi-client support"""
    global client_counter
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)  # Allow up to 5 clients in queue
        print(f"[*] VPN Server listening on {host}:{port}")
        print(f"[*] Active clients: {len(clients)}")
        
        while True:
            try:
                conn, addr = server.accept()
                client_counter += 1
                client_id = client_counter
                
                # Handle each client in a separate thread
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(conn, addr, client_id),
                    daemon=True
                )
                client_thread.start()
                print(f"[*] Active clients: {len(clients)}")
                
            except KeyboardInterrupt:
                print("\n[!] Server shutting down...")
                break
            except Exception as e:
                print(f"[✗] Error accepting connection: {e}")
                
    except Exception as e:
        print(f"[✗] Server error: {e}")
    finally:
        server.close()
        print("[✓] Server closed")

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[!] Server terminated by user")
    except Exception as e:
        print(f"[✗] Fatal error: {e}")