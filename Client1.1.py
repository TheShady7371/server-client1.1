import threading
import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Введите (ip:port)", end=' ')
connect = str(input())

ip, port = connect.split(':')
server_address = (ip, int(port))


print("Введите username:", end=' ')
username = str(input())

client.sendto(f"**JOIN|{username}".encode(), server_address)

def handlering(socket: socket.socket):
    while True:
        data = client.recvfrom(1024)
        print(data[0].decode())

def send_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            # Отправляем файл по частям
            while True:
                data = f.read(1024)  # Читаем 1024 байта
                if not data:
                    break
                client.sendto(data, server_address)
        client.sendto(b'**EOF', server_address)  # Отправляем сигнал конца файла
    else:
        print("Файл не найден!")

def user_input(socket: socket.socket):
    while True:
        message = input()
        if message.startswith("!sendfile "):  # Если ввод начинается с !sendfile
            file_path = message.split(" ", 1)[1]
            send_file(file_path)
        elif message:
            client.sendto(f"**SEND|{message}".encode(), server_address)


inp = threading.Thread(target=user_input, args=(client, ))
handler = threading.Thread(target=handlering, args=(client, ))

inp.start()
handler.start()

# import threading

# client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# print("Введите (ip:port)", end=' ')
# connect = str(input())

# ip, port = connect.split(':')
# server_address = (ip, int(port))


# print("Введите username:", end=' ')
# username = str(input())

# client.sendto(f"**join|{username}".encode(), server_address)

# def handlering(socket: socket.socket):
#     while True:
#         data = client.recvfrom(1024)
#         print(data[0].decode())
        
# def user_input(socket: socket.socket):
#     while True:
#         message = input()
#         if message:
#             client.sendto(f"**send|{username}|{message}".encode(), server_address)


# inp = threading.Thread(target=user_input, args=(client, ))
# handler = threading.Thread(target=handlering, args=(client, ))

# inp.start()
# handler.start()
