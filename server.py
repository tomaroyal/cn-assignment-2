# Reference:
# 
# https://stackabuse.com/basic-socket-programming-in-python/
#


# load additional Python module
import socket

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
# ip_address = socket.gethostbyname(local_hostname)
ip_address = "192.168.55.132"

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 7889
server_address = (ip_address, 28099)
print ('starting up on %s port %s' % server_address)
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:
    # wait for a connection
    print ('Waiting for a connection ......')
    client_connection, client_address = sock.accept()

    try:
        # show who connected to us
        print ('Connection from', client_address)

        header = 0

        # receive the data in small chunks and print it
        while True:
            data = client_connection.recv(4020)
            if data:
                # output received data
                # print ("Data received on Server: %s" % data)

                # Decoding the data received from client
                rec_int = data.decode('utf8')


                # Extracting client time that was sent 
                time = rec_int[10:20]

                # Check if time is not corrupted, if not, continue sending acks
                if(time.isnumeric()):

                    ack = rec_int[0:10]

                    ack = int(ack)

                    # Checking the expected header value for corruption
                    if(header == ack):
                        print ("Data received on Server: %s" % data)
                        header = ack + 1


                    # Updating the value of ack
                    ack += 1

                    ack = f'{ack:<10}'


                    # Updating the ack value, final value to be sent = ack + timestamp recieved
                    final_send = ack + time 

                    final_send = final_send.encode('utf8')
                    client_connection.sendall(final_send)
            else:
                # no more data -- quit the loop
                print ("no more data.")
                break
    finally:
        # Clean up the connection
        client_connection.close()