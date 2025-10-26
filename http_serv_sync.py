# simple sync http 

import socket 

HOST = '127.0.0.1'
PORT = 8080

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen(5) 
    print(f"Serving sync on http://{HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            request = conn.recv(1024).decode('utf-8')
            print(request.splitlines()[0]) # show the HTTP request line

            # Always reply with the same page
            responce = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Hi!"
            )
            conn.sendall(responce.encode('utf-8'))
