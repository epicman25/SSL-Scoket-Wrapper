import random
import socket # Import socket module
from aes import AESCipher
import hashlib
 
def msg_encrypt(msg,key):
   key = str(key)
   aesCipher = AESCipher(key)
   return aesCipher.encrypt(msg)
def msg_decrypt(msg,key):
   key = str(key)
   aesCipher = AESCipher(key)
   return aesCipher.decrypt(msg)
 
sock = socket.socket() # Create a socket object
print("Welcome to the chat room")
host = "localhost" # Get local machine name
ip = socket.gethostbyname(host) # Get local machine I
port = 2508
#port = 2507
name = "Client"
print("Trying to connect to ",host," on port ",port)
sock.connect((host, port)) # Now wait for client connection.
print("Connected to ",host," on port ",port)
sock.send(name.encode()) # Send to client.
s_name = sock.recv(1024) # Receive from client.
s_name = s_name.decode() # Decode the received data
N = 49979687
pri_client = random.randint(1,2000)
base = random.randint(1,2000)
print("Server name : ",s_name)
print("KEY EXCHANGE IN PROGRESS")
pub_client = (base ** pri_client) % N
key_msg = str(pub_client) + "|" + str(base)
sock.send(key_msg.encode()) # Send to client.
pub_server = sock.recv(1024).decode() # Receive from client.
secret_key = (int(pub_server) ** pri_client) % N
print("Public key of client: ",pub_client)
print("Public key of server: ",pub_server)
print("Shared secret key of client: ",secret_key)
print("Type "+"esc"+" to exit")
while True:
   message = sock.recv(1024) # Receive from client.
   message = msg_decrypt(message, secret_key)
   msg, _hash = message.split("|")
   _hash_calc = hashlib.sha256(str.encode(msg)).hexdigest()
   if _hash == _hash_calc:
           print(s_name,":",msg)
   else:
       print("message tampered")
 
   message = input("Client : ")
   if message == "esc":
       # print(s_name,":",lis[0][2:-2].encode())
       message = "Client leaving chat room"
       sock.send(message.encode())
       print()
       exit()
      
   _hash    = hashlib.sha256(str.encode(message)).hexdigest()
   message = message + "|" + _hash
   message = msg_encrypt(message,secret_key)
 
   sock.send(message)
