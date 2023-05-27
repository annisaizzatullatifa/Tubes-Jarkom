# import socket module
from socket import *
import sys  # In order to terminate the program

serverSocket = socket(AF_INET, SOCK_STREAM) # Membuat server socket, AF_INET berarti menggunakan protokol IPv4,
                                            # dan SOCK_STREAM berarti tipe socket yang dipakai adalah TCP bukan UDP
serverPort = 1805 # Menentukan nomor port server dengan 1805
serverSocket.bind(("", serverPort)) # Menetapkan/mengikat nomor port ke socket
serverSocket.listen(1)  # Membuat server mendengarkan permintaan koneksi TCP dari klien dengan jumlah maksimum
                        # koneksi antrian (setidaknya 1)

def response_status(code): # Membuat fungsi untuk menentukan respon status berdasarkan kode respon
    if code == 200: # Jika kode respon adalah 200
        return "HTTP/1.1 200 OK" # Maka akan mengembalikan string berikut
    elif code == 404: # Jika kode respon adalah 404
        return "HTTP/1.1 404 Not Found" # Maka akan mengembalikan string berikut

while True: # Digunakan agar perintah dijalankan selama kondisi di atas adalah True atau benar
    print("ready to serve...") # Mencetak string "ready to serve..."
    connectionSocket, addr = serverSocket.accept() # Membuat socket baru pada server khusus untuk klien dengan
                                                   # memanggil metode accept() untuk serverSocket. Setelah klien dan
                                                   # server menyelesaikan handshake, akan terbuat koneksi TCP antara
                                                   # clientSocket klien dan connectionSocket server
    try:
        message = connectionSocket.recv(1024).decode() # Menerima paket pesan request dari klien dan dimasukkan ke
                                                       # dalam variabel message
        filename = message.split()[1] # Memecah pesan request klien untuk mengambil nama file html yang diminta

        # Extract the path from the filename by removing the leading '/'
        filepath = filename[1:] 

        with open(filepath, 'rb') as f: # Membuka file yang diminta dalam bentuk binary
            outputdata = f.read() # Membaca file dan memasukkannya pada variabel outputdata

        # Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\nContent-Type: text/html\r\n\r\n".encode())
        print("Response:", response_status(200)) # Mengeprint pesan respon

        # Send the content of the requested file to the client
        connectionSocket.sendall(outputdata)
        connectionSocket.send("\r\n".encode()) # Mengirimkan baris kosong
        connectionSocket.close() # Menutup koneksi socket

    except IOError: # Jika terjadi error maka akan dilakukan hal di bawah
        print("Response:", response_status(404)) # Mengeprint pesan respon

        # Send a 404 Not Found HTTP response message to the client
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode()) # Mengirimkan kode html
                                                                                           # agar terlihat pesan
                                                                                           # error pada browser

        # Close the client connection socket
        connectionSocket.close()
        
serverSocket.close() # Menutup socket server
sys.exit() # Keluar dari program
