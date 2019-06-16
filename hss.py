import sys
import socket
import diameter
import binascii


# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port
server_address = ('10.0.1.5', 3868)

print('listening')
sock.bind(server_address)


# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        print('connection from' + str(client_address))
        data_sum = b''
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(32)
            packet_length = diameter.decode_diameter_packet_length(data)
            print("Packet Length is: " + str(packet_length))
            print(data)
            data_sum = data + connection.recv(packet_length - 32)

            if data == 7:
                data_sum = data_sum + data
                pass
            else:
                print("Got All Data: " + str(data_sum))
                
                print("Decoding complete packet: " + str(data_sum))
                packet_vars, avps = diameter.decode_diameter_packet(data_sum)
                print(packet_vars)
                print('\n\n\nno more data from' + str(client_address))

                #Send CEA response to CER
                if packet_vars['command_code'] == 257 and packet_vars['ApplicationId'] == 0:            
                    #Generate AVPs
                    avp = diameter.generate_avp(268, 40, "000007d1")    #Result Code
                    avp = avp + diameter.generate_avp(264, 40, str(binascii.hexlify(b'nickpc.localhost'),'ascii')) #Origin Host
                    avp = avp + diameter.generate_avp(278, 40, diameter.AVP_278_Origin_State_Incriment(avps)) #Origin State (Has to be incrimented (Handled by AVP_278_Origin_State_Incriment))
                    avp = avp + diameter.generate_avp(257, 40, diameter.ip_to_hex("10.0.0.5")) #Host-IP-Address
                    avp = avp + diameter.generate_avp(266, 40, "00000000") #Vendor-Id
                    avp = avp + diameter.generate_avp(269, 40, diameter.string_to_hex("PyHSS")) #Product-Name
                    avp = avp + diameter.generate_avp(267, 40, "000027d9") #Firmware-Revision
                    avp = avp + diameter.generate_avp(260, 40, "000001024000000c010000160000010a4000000c000028af") #Vendor-Specific-Application-ID
                    avp = avp + diameter.generate_avp(258, 40, "ffffffff") #Auth-Application-ID
                    avp = avp + diameter.generate_avp(265, 40, "0000159f") #Supported-Vendor-ID (3GGP v2)
                    avp = avp + diameter.generate_avp(265, 40, "000028af") #Supported-Vendor-ID (3GPP)
                    avp = avp + diameter.generate_avp(265, 40, "000032db") #Supported-Vendor-ID (ETSI)
                    #Generate Diameter packet
                    response = diameter.generate_diameter_packet("01", "00", 257, 0, packet_vars['hop-by-hop-identifier'], packet_vars['end-to-end-identifier'], avp)
                    #Send it
                    connection.sendall(bytes.fromhex(response))
                    break
                else:
                    print("Recieved packet with Command Code: " + str(packet_vars['command_code']) + " and ApplicationID: " + str(packet_vars['ApplicationId']))
                    break
    finally:
        # Clean up the connection
        connection.close()
