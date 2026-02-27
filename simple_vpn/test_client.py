import socket
from cryptography.fernet import Fernet
import time

KEY = b'PFFzFB5FAsCrMWwR5eq7WZ6oF3Qmbe536A7Mt-SIM14='

def test_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 9999))
        print('[✓] Connected to server!')

        fernet = Fernet(KEY)
        
        # Send test message
        test_msg = "Hello VPN Server!"
        client.send(fernet.encrypt(test_msg.encode()))
        print(f'[✓] Sent: {test_msg}')

        # Receive response (with timeout for server input)
        client.settimeout(2)
        try:
            encrypted_response = client.recv(1024)
            if encrypted_response:
                response = fernet.decrypt(encrypted_response).decode()
                print(f'[✓] Received: {response}')
        except socket.timeout:
            print('[!] Server did not respond (waiting for input)')

        client.close()
        print('[✓] Connection closed')
        
    except Exception as e:
        print(f'[✗] Error: {e}')

if __name__ == '__main__':
    test_client()
