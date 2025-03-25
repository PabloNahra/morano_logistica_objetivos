from cryptography.fernet import Fernet

# Proceso para encriptar y desencriptar
## 2- Generar una clave
key = Fernet.generate_key()
print(f"Generada clave: {key.decode()}")

## Fijar la clave
key_generada = "vCpxjxZ3RiFHUI6GDOozI-NXAebX1a8r2GnjVBBifnI="

## 3-Encriptar la contraseña
# Crear una instancia de Fernet
fernet = Fernet(key_generada)

# La contraseña a encriptar
password = "Swatch2021%"

# Encriptar la contraseña
encrypted_password = fernet.encrypt(password.encode())
print(f"Contraseña encriptada: {encrypted_password.decode()}")

## 4-Guardar la clave y la contraseña en el JSON

## 5-Cargar el Json y desencriptar
