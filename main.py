from cryptography.fernet import Fernet
import os

# Generate or load encryption key
KEY_FILE = "key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

def view_passwords():
    key = load_key()
    with open('passwords.txt', 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:", decrypt(passw, key))

def add_password():
    key = load_key()
    name = input('Account Name: ')
    pwd = input("Password: ")
    encrypted_pwd = encrypt(pwd, key)
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + encrypted_pwd + "\n")

if __name__ == "__main__":
    while True:
        mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
        if mode == "q":
            break
        elif mode == "view":
            view_passwords()
        elif mode == "add":
            add_password()
        else:
            print("Invalid mode.")