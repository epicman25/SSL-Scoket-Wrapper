import socket # Import socket module
import random
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
name = "Tejeshwar"
ip = socket.gethostbyname(host) # Get local machine IP
port = 2508 # Reserve a port for your service.
#port = 2507
sock.bind((host, port)) # Bind to the port
print("Server started on ip: " + ip + " and port: " + str(port))
sock.listen(5) # Now wait for client connection.
print("Waiting for incoming connections...") # Now wait for client connection.
connection,address = sock.accept() # Establish connection with client.
print("Got connection from: " + str(address))
s_name = connection.recv(1024) # Receive from client.
s_name = s_name.decode() # Decode the received data
#print("Client name: " + s_name)
connection.send(name.encode()) # Send to client.
N = 49979687
pri_server = random.randint(1,2000)
print("KEY EXCHANGE IN PROGRESS")
pub_client_msg = connection.recv(1024).decode() # Receive from client.
base = int(pub_client_msg.split("|")[1])
pub_client = int(pub_client_msg.split("|")[0])
secret_key = (pub_client ** pri_server) % N
pub_server = (base ** pri_server) % N
connection.send(str(pub_server).encode()) # Send to client.
print("Public key of client: ",pub_client)
print("Public key of server: ",pub_server)
print("Shared secret key of client: ",secret_key)
print("Type "+"esc"+" to exit")
while True:
   message = input("Server : ")
   if message == "esc":
       message = "Server leaving chat room"
       connection.send(message.encode())
       print()
       exit()
   message = message + "|" + (hashlib.sha256(str.encode(message))).hexdigest()
   message = msg_encrypt(message,secret_key)
   # print(message)
   connection.send(message) # Send to client.
 
   message = connection.recv(1024) # Receive from client.
   message = msg_decrypt(message, secret_key)
   msg, _hash = message.split("|")
   _hash_calc = hashlib.sha256(str.encode(msg)).hexdigest()
   if _hash == _hash_calc:
 
           print(s_name,":",msg,"Integrity maintained")
   else:
       print("message tampered")
