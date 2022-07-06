from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from hashlib import sha256
keyPair = RSA.generate(1024)
publicKey = keyPair.e
privateKey = keyPair.d
n = keyPair.n

# print("Public Key : ",publicKey)
# print("Private Key : ",privateKey)
# print("N : ",n)

message_to_be_signed = input("Enter the message to be signed : ")

message_to_be_signed = bytes(message_to_be_signed, 'utf-8')

hash_of_message_to_be_signed = int.from_bytes(sha256(message_to_be_signed).digest(), byteorder='big')

signature_generated = pow(hash_of_message_to_be_signed, privateKey, n)

print("Signature Generated : ",signature_generated)

message_to_be_sent = message_to_be_signed.decode('utf-8') + "*****" + str(signature_generated)

print("Message to be sent : ",message_to_be_sent)


message_recieved = input("Enter the message recieved : ")

message_part, signature_recieved = message_recieved.split("*****")

print("Message recieved : ",message_part)
print("Signature recieved : ",signature_recieved)

message_recieved = bytes(message_recieved, 'utf-8')

hash_of_message_recieved = int.from_bytes(sha256(message_recieved).digest(), byteorder='big')

hash_from_signature_recieved = pow(int(signature_recieved), publicKey, n)

if hash_of_message_to_be_signed == hash_from_signature_recieved:
    print("Message is authentic")
else:
    print("Message is not authentic")




