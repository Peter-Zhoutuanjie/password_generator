from Crypto.Cipher import AES
import base64

class AESEncryptor():
    BLOCK_SIZE = 16

    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, data):
        data = self.pad(data)
        cipher = AES.new(self.key, AES.MODE_ECB)
        result = cipher.encrypt(data.encode())
        encodestrs = base64.b64encode(result)
        enctext = encodestrs.decode('utf8')
        return enctext


    def decrypt(self, data):
        data = base64.b64decode(data)
        cipher = AES.new(self.key, AES.MODE_ECB)

        # 去补位
        text_decrypted = self.unpad(cipher.decrypt(data))
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted
