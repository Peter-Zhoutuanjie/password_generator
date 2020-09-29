import hashlib

from aes_encryptor import AESEncryptor

admin_pwd = '123456'
ip_enc = 'DM7Y1VpJ0uysj1a3ECymlA=='
key = hashlib.md5(admin_pwd.encode(encoding='UTF-8')).hexdigest()
enc = AESEncryptor(key.encode('utf-8'))
print(enc.decrypt(ip_enc))