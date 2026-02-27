import socket
from cryptography.fernet import Fernet
import threading
import time

KEY = b'PFFzFB5FAsCrMWwR5eq7WZ6oF3Qmbe536A7Mt-SIM14='

def client_session(client_id, messages):
    """Simulate a client session"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9999))
        print(f"[Client {client_id}] Connected!")

        fernet = Fernet(KEY)
        
        for msg in messages:
            print(f"[Client {client_id}] Sending: {msg}")
            client.send(fernet.encrypt(msg.encode()))
            
            encrypted_response = client.recv(1024)
            response = fernet.decrypt(encrypted_response).decode()
            print(f"[Client {client_id}] Received: {response}")
            time.sleep(0.5)

        client.close()
        print(f"[Client {client_id}] Closed")
        
    except Exception as e:
        print(f"[Client {client_id}] Error: {e}")

# Test with 3 simultaneous clients
if __name__ == '__main__':
    threads = []
    
    # Client 1
    t1 = threading.Thread(target=client_session, args=(1, [
        "Hello from Client 1",
        "Test message 1",
        "Goodbye Client 1"
    ]))
    
    # Client 2
    t2 = threading.Thread(target=client_session, args=(2, [
        "Hello from Client 2",
        "Test message 2"
    ]))
    
    # Client 3
    t3 = threading.Thread(target=client_session, args=(3, [
        "Hello from Client 3",
        "Test message 3",
        "Another test",
        "Goodbye Client 3"
    ]))
    
    threads = [t1, t2, t3]
    for t in threads:
        t.start()
    
    for t in threads:
        t.join()
    
    print("\n[✓] All tests completed!")
