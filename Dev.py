import socket, ssl, requests

# Step 1: DNS Lookup
host = "www.google.com"
ip = socket.gethostbyname(host)
print(f"[DNS] {host} -> {ip}")

# Step 2: TCP Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, 443))
print(f"[TCP] Connected to {ip}:443")

# Step 3: TLS Handshake
context = ssl.create_default_context()
tls_sock = context.wrap_socket(sock, server_hostname=host)
print(f"[TLS] Handshake complete, cipher: {tls_sock.cipher()}")

# Step 4: HTTP Request
request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
tls_sock.send(request.encode())

# Step 5: HTTP Response
response = b""
while True:
    data = tls_sock.recv(4096)
    if not data:
        break
    response += data

tls_sock.close()

# Show response headers
headers, _, body = response.partition(b"\r\n\r\n")
print("[HTTP Response Headers]")
print(headers.decode(errors="ignore").split("\r\n")[0:10])  # first 10 lines
