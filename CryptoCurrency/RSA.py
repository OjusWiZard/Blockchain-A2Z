from binascii import hexlify, unhexlify

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15


def generate_key(secret_code: str, modulus_length=256*4) -> RsaKey:
	key = RSA.generate(modulus_length)
	encrypted_key = key.export_key(passphrase=secret_code, pkcs=8, protection="scryptAndAES128-CBC")

	file_out = open("CryptoCurrency/private_key.pem", "wb")
	file_out.write(encrypted_key)
	file_out.close()

	return key

def fetch_key(secret_code: str) -> RsaKey:
	key_file = open("CryptoCurrency/private_key.pem", "rb")
	encrypted_key = key_file.read()
	key_file.close()

	try:
		key = RSA.import_key(encrypted_key, passphrase=secret_code)
	except ValueError:
		return None
	return key

def sign(message: str , key: RsaKey) -> str:
	hashed_msg = SHA256.new(message.encode("utf-8"))
	signature = pkcs1_15.new(key).sign(hashed_msg)
	return hexlify(signature).decode("utf-8")

def verify(message: str, signature: str, key: RsaKey) -> bool:
	hashed_msg = SHA256.new(message.encode("utf-8"))
	signature = unhexlify(signature.encode("utf-8"))
	try:
		pkcs1_15.new(RSA.import_key(key)).verify(hashed_msg, signature)
		return True
	except (ValueError, TypeError):
		return False
