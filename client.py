# Reference:
# 
# https://stackabuse.com/basic-socket-programming-in-python/
#


# load additional Python modules
import socket
import time

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#open file
f=open("mainFile.txt", "r")

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = '192.168.55.132'

# bind the socket to the port 23456, and connect
server_address = (ip_address, 28099)
sock.connect(server_address)
print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# defining various variables and initial loop


# Variable to track the sum of the times to calculate the avg RT delay
sum=0

# Variable to store the value of the header
head=0

# Variable to store the total number of packets that we wish to divide our file in
counter_data = 5

# Variable to track the number of times a packet is resend after no ack is recieved
resend_data = 0

# Outer loop to run the amount of packets * packet size time.
for entry in range(counter_data):
    
    # To calculate the number of times before the packet has to be discarded if wrong ack is received
    discard = 0
    print ("data: %s" % entry)
    
    # Flag to store whether ack is received when data is sent
    flag = False

    # Flag to store whether the same file was sent before, so that same type of 
    # file is not read and sent again when the timeout occurs
    flagfilesent=True
    
    # Loop to handle timeout situation when ack is not received
    while flag==False:

        # Checking if data is sent a number of times so that infinite loop condition does not occur
        # when the packets get repeatedly dropped and acks are not received.
        resend_data += 1
        if resend_data > 5:
            print("Not able to resend packets (tried 5 times) -> PACKET DROPPED !!!")
            break

        # Check if file was sent again
        if flagfilesent:
            filematerial=f.read(4000)

        # Calculating the time the packet was sent 
        clientTime = str(time.time())[0:10]
        print("time length",len(clientTime))
        
        # Adding the value of header to make it 10 byte long
        header=f'{head:<10}'
        print("see this",len(header))

        # Building the total message that has to be sent
        tosend = header+clientTime + filematerial
        #print("message sent=",tosend)

        # Finally encoding the data and sending through the socket 
        new_data = tosend.encode()
        sock.sendall(new_data)
        sock.settimeout(3)


    # We check if the packet has not been resent again and if the ack received is not
    # consistent or if the packet has to be discarded due to non-receiveing of acks
    while(resend_data < 6 and head != int(recAck) - 1 and discard < 6):
        discard=discard+1
        print("head=",head,"recAck=",recAck)
        
        # Resending data
        sock.sendall(new_data)
        
        time.sleep(1)
        
        # Ack computation
        rec_data = sock.recv(21)
        
        recdata = rec_data.decode("utf-8")
        # print(recdata)

        if(str(rec_data[0]).isnumeric()):

            recAck = rec_data[0:10]
            recAck=float(recAck)

            print("2nd recAck = ", recAck)

            recTime = rec_data[10:20]

        # To discard the packets if not received
        if discard == 6:
            print("Ack not received for 5 times -> PACKET DISCARDED !!!")

    # Calculating the round trip delay only when the acks were received earlier
    if(discard != 6):
        print("Round Trip Delay :" , time.time()-recTime)
        sum += tim
    
    head += 1
    # wait for two seconds
    time.sleep(2)


# close connection
print("average=",sum/counter_data)
sock.close()