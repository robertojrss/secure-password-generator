#cyber1.py

import socket

# host = "INSERT YOUR TARGET HERE"
port = 80

s = socket.socket()
s.settimeout(5)

result = s.connect_ex((host, port))

if result == 0:
    print(f"\nPort {port} is open.\n")

    request = f"GET / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    s.send(request.encode())

    full_response = b""

    while True:
        try:
            data = s.recv(4096)
            if not data:
                break
            full_response += data
        except:
            break

    response_text = full_response.decode(errors="ignore")

    # Separar headers e body
    parts = response_text.split("\r\n\r\n", 1)

    headers = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    print("# HEADERS\n")
    print(headers)

    print("\n# BODY (first 500 chars)\n")
    print(body[:500])

    # Extrair informações úteis
    print("\n# PARSED INFO\n")

    for line in headers.split("\r\n"):
        if line.lower().startswith("server:"):
            print(f"Server detected: {line}")

        if line.lower().startswith("location:"):
            print(f"Redirect found: {line}")

else:
    print(f"Port {port} is closed.")

s.close()