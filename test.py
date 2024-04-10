from cryptography.fernet import Fernet
import os
import json

class PasswordManager:
    def __init__(self, key_path='key.key', data_path='passwords.json'):
        self.key_path = key_path
        self.data_path = data_path
        self.key = None
        self.load_key()

    def load_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_path, 'wb') as f:
                f.write(self.key)

    def encrypt(self, data):
        cipher = Fernet(self.key)
        return cipher.encrypt(data.encode())

    def decrypt(self, data):
        cipher = Fernet(self.key)
        return cipher.decrypt(data).decode()

    def save_passwords(self, passwords):
        with open(self.data_path, 'wb') as f:
            f.write(self.encrypt(json.dumps(passwords)))

    def load_passwords(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'rb') as f:
                return json.loads(self.decrypt(f.read()))
        else:
            return {}

    def add_password(self, service, username, password):
        passwords = self.load_passwords()
        passwords[service] = {'username': username, 'password': password}
        self.save_passwords(passwords)

    def get_password(self, service):
        passwords = self.load_passwords()
        if service in passwords:
            return passwords[service]
        else:
            return None

    def delete_password(self, service):
        passwords = self.load_passwords()
        if service in passwords:
            del passwords[service]
            self.save_passwords(passwords)
            return True
        else:
            return False

# Example usage
password_manager = PasswordManager()

# Adding a password
password_manager.add_password('example.com', 'user123', 'password123')

# Retrieving a password
print(password_manager.get_password('example.com'))

# Deleting a password
password_manager.delete_password('example.com')

#Hejhej