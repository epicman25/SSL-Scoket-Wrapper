import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

#code help took from 
# https://medium.com/quick-code/aes-implementation-in-python-a82f582f51c2

class AESCipher(object):

    def __init__(self, key): 

        self.sz = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, msg):
        msg = self._pad(msg)
        iv = Random.new().read(self.sz)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        encryptCipher = cipher.encrypt(msg.encode())
        return base64.b64encode(iv + encryptCipher) 

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:self.sz]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decryptCipher = cipher.decrypt(enc[self.sz:])
        return self._unpad(decryptCipher).decode('utf-8')

    def _pad(self, text):
        padding = self.sz - len(text) % self.sz
        charToPad = chr(padding)
        return text + padding * charToPad

    @staticmethod
    def _unpad(text):
        charPadded = text[len(text) - 1:]
        paddingLen = ord(charPadded)
        return text[:-paddingLen]

#driver code
if __name__ == "__main__":
    key = "somekey"
    cipher = AESCipher(key)
    message = "fdads"
    enc = cipher.encrypt(message)
    dec = cipher.decrypt(enc)

    print(message, enc, dec)