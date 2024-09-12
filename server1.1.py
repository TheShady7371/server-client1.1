import socketserver

class MyUDPHandlers(socketserver.BaseRequestHandler):
    def handle_file(self, data):
        file_name = f"received_file_{self.client_address[1]}.bin"
        with open(file_name, 'wb') as f:
            while data != b'**EOF':
                f.write(data)
                data, _ = self.request  # Продолжаем получать данные
        print(f"Файл получен от {self.client_address} и сохранен как {file_name}")

    def handle(self):
        data, socket = self.request
        
        if data.decode().startswith('**JOIN'):
            username = data.decode().split('|')[1]
            print(f"{username} присоединился из {self.client_address}")
        
        elif data.decode().startswith('**SEND'):
            message = data.decode().split('|')[1]
            print(f"Сообщение от {self.client_address}: {message}")
        
        elif data.startswith(b'**EOF'):
            return  # Конец передачи файла
        
        else:
            # Если это не команда, значит это данные файла
            self.handle_file(data)  # Обрабатываем файл

HOST, PORT = '192.168.1.8', 50005

with socketserver.UDPServer((HOST, PORT), MyUDPHandlers) as server:
    print(f"Сервер запущен на {HOST}:{PORT}")
    server.serve_forever()
