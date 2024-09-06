import socket
import os
import secrets

def generate_keys():
    # Gera uma chave AES de 256 bits e um IV aleatório de 128 bits
    chave_aes = secrets.token_bytes(32)  # 256 bits
    chave_iv = secrets.token_bytes(16)    # 128 bits
    return chave_aes.hex(), chave_iv.hex()  # Retorna como strings hexadecimais

def main():
    host = 'localhost'  # Endereço do servidor
    port = 65432        # Porta do servidor

    # Gera as chaves
    chave_aes_hex, chave_iv_hex = generate_keys()

    # Conecta ao servidor
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        
        # Prepara a mensagem para enviar
        message = f"{chave_aes_hex},{chave_iv_hex}"
        s.sendall(message.encode())  # Envia os dados como bytes
        print(f"Chaves enviadas: {message}")

if __name__ == '__main__':
    main()
