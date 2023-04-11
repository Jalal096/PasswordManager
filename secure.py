from cryptography.fernet import Fernet

class SecurePassword:
    def generate_key(self):
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as key_file:
            key_file.write(key)
            print('Key is generated')

    def load_key(self):
        return open('secret.key', 'rb').read()

    def encrypt_message(self, message):
        key = self.load_key()
        encoded_msg = message.encode()
        f = Fernet(key)
        encrypted_msg = f.encrypt(encoded_msg)
        return encrypted_msg

    def decrypt_message(self, message):
        key = self.load_key()
        f = Fernet(key)
        dec_msg = f.decrypt(message)
        return dec_msg.decode()

s = SecurePassword()
s.generate_key()