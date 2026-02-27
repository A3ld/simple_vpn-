# Simple VPN 🔐

A lightweight encrypted VPN server and client built with Python using Fernet encryption from the cryptography library.

## Features

✅ **Multi-client support** - Handle multiple clients simultaneously with threading
✅ **End-to-end encryption** - All messages encrypted with Fernet (symmetric encryption)
✅ **Simple architecture** - Easy to understand and modify
✅ **Echo responses** - Server echoes back received messages for verification
✅ **Error handling** - Graceful error handling and disconnection management

## Requirements

```
cryptography>=41.0.0
```

Install dependencies:
```bash
pip install cryptography
```

## Usage

### Start the Server

```bash
cd simple_vpn
python server.py
```

Server will listen on `localhost:9999`

### Connect a Client

```bash
cd simple_vpn
python client.py
```

Then type messages and press Enter. Type `exit` to disconnect.

### Multiple Clients

You can connect multiple clients simultaneously in different terminal windows:

```bash
# Terminal 1: Server
python server.py

# Terminal 2: Client 1
python client.py

# Terminal 3: Client 2
python client.py

# Terminal 4: Client 3
python client.py
```

## Files

- **server.py** - VPN server with multi-client support
- **client.py** - VPN client for connecting to the server
- **test_client.py** - Single client test script
- **test_multi_client.py** - Test script for multiple simultaneous clients

## How It Works

### Encryption
- Uses **Fernet** (symmetric encryption) from the cryptography library
- Both server and client share the same encryption key
- All messages are encrypted before transmission

### Architecture
```
Client → [Encrypted Message] → Server
                ↓
         Server Decrypts & Processes
                ↓
Server → [Encrypted Response] → Client
```

### Threading
- Server runs in main thread
- Each client connection handled in separate daemon thread
- Allows multiple simultaneous connections

## Example Session

```
Server says:
[*] VPN Server listening on localhost:9999
[✓] Client 1 connected from ('127.0.0.1', 12345)

Client says:
[✓] Connected to VPN server at localhost:9999
[You]: Hello Server
[Server]: Echo: Hello Server
[You]: exit
[!] Closing connection...
[✓] Disconnected
```

## Security Notes

⚠️ **Development Only** - This is a simplified example for educational purposes.

For production use, consider:
- Using asymmetric encryption (RSA, ECC)
- Implementing user authentication
- Using TLS/SSL for transport
- Key exchange protocols
- Rate limiting and DOS protection

## License

Free to use and modify.

## Author

Simple VPN Project
