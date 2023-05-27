from socket import * # import modul socket
import sys # import modul system untuk terminasi program

# procedure untuk meminta file tertentu dari server
def get(server, file):
    clientSocket = socket(AF_INET, SOCK_STREAM) # inisialisasi socket
    clientSocket.connect(server) # memulai koneksi dengan server berdasarkan alamat dan port milik server

    clientSocket.send((('GET /' + file + ' HTTP/1.1\r\nHost: ' + server[0] + ':' + str(server[1]) + '\r\n\r\n').encode())) # mengirim permintaan file tertentu dengan protokol dan header yang berisi alamat dan nomor port milik server 

    data = "" # deklarasi variabel yang akan menyimpan respons permintaan dari server
    while True:
        clientSocket.settimeout(5) # jika setelah 5 detik client tidak menerima data dari server, maka stop menunggu data baru
        new = clientSocket.recv(1024).decode() # menerima data baru dari server yang berukuran 1024 yang kemudian didecode menjadi string
        data = data + new # menambahkan data baru yang telah didecode ke akhir data lama
        if len(new) == 0: # jika panjang data baru yang diterima adalah 0, maka keluar dari loop karena semua data telah selesai diterima
            break # keluar (paksa) dari loop

    print(data) # cetak data yang telah diterima dari looping di atas
    clientSocket.close()

if __name__ == "__main__": # main program
    get(("localhost", 1805), "index.html") # pemanggilan procedure get untuk meminta file index.html dari server yang mempunyai address localhost
