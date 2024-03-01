import socket
import threading

HEADER = 64
SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5051
ADDR = (SERVER_IP,PORT)
FORMAT ='utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"

active_users = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def listen_for_messages(client, username):
    try:
        while True:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                message = client.recv(msg_length).decode(FORMAT)
            
                if message and message == "disconnect":
                    prompt = "SERVER~ "+f"{username} left the chatroom."
                    send_message_to_all(prompt)
                    break
                if message:
                    final_message = "@"+username+" : "+message
                    send_message_to_all(final_message)
                else:
                    print("Send a valid message!")
    
        client.close()
    except Exception as e:
        exit()
    # print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
            


def send_message_to_client(client, message):
    msg = message.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(msg)

    # client.send(message.encode(FORMAT))



def send_message_to_all(message):
    for user in active_users:
        send_message_to_client(user[1],message)



def handle_client(client, addr):
    try:
        print(f"[CONNECTION RECIEVED] new connection from {addr}")
        while True:
            username_length = client.recv(HEADER).decode(FORMAT)
            if username_length:
                username_length = int(username_length)
                username = client.recv(username_length).decode(FORMAT)
                if username:
                    active_users.append([username, client])
                    prompt = "SERVER~ " + f"{username} entered the chatroom."
                    send_message_to_all(prompt)
                    break
                else:
                    print("Please enter a username!")
        thread = threading.Thread(target=listen_for_messages, args=(client, username,))
        thread.start()
    except Exception as e:
        exit()




    # connected = True
    # while connected:
    #     msg_length = client.recv(HEADER).decode(FORMAT)
    #     if msg_length:
    #         msg_length = int(msg_length)
    #         message = server.recv(msg_length).decode(FORMAT)
    #         if message == DISCONNECT_MESSAGE:
    #             connected = False
    #         print(f"{addr}: {message}")

    # client.close()



def start():
    try:
        server.listen()
        print(f"[LISTENING] server is listening on {SERVER_IP}...")
        while True:
            client, addr = server.accept()
            thread = threading.Thread(target= handle_client,args=(client, addr,))
            thread.start()
            print(f"ACTIVE CONNECTIONS : {threading.active_count() - 1}")
    except Exception as e:
        exit()
print("[STARTING] server is starting...")
start()
