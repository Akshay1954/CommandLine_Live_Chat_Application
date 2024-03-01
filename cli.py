import socket
import threading

SERVER_IP = "192.168.56.1"
PORT = 5051
HEADER = 64
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER_IP,PORT)
FORMAT = "utf-8"

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(ADDR)
        print("Successfullly connected too server.")
    except:
        print(f"Unable to connect to the server {SERVER_IP}:{PORT}")
    
    communicate_to_server(client)


# def send_message(message):
#     msg = message.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(msg)


def listen_for_messages_from_server(client,username):
    while True:
        msg_length = client.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            message = client.recv(msg_length).decode(FORMAT)
            
            if message:
                if "entered" or "left" in message:
                    print(message)
                else:
                    u_name = message.split("~")[0]
                    msg = message.split("~")[1]
                    print(f"[{u_name}] : {msg}")
            else:
                print("Empty message.")


def send_message_to_server(client):
    while True:
        msg = input()
        if msg != "":
            message = msg.encode(FORMAT)
            msg_len = len(message)
            send_length = str(msg_len).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
        else:
            print("Empty Message.")
            exit(0)



def communicate_to_server(client):
    username = input("Enter the username : ")
    if username != "":
        message = username.encode(FORMAT)
        msg_len = len(message)
        send_length = str(msg_len).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
    else:
        print("Username cant be empty.")
        exit(0)
    thread = threading.Thread(target=listen_for_messages_from_server,args=(client,username,))
    thread.start()
    send_message_to_server(client)


main()
