#!/usr/bin/env python3
import socket
from protobuf_inspector.types import StandardParser
import CommandPB_pb2
import time
import crcmod

#0xa305 CommandResDTO: time: 1695572445 action: 8 package_nub: 1 tid: 1695572445 data: b'A:800,B:0,C:0\r'
#0xa205 CommandReqDTO: dtu_sn: b'xxxxxxxxxxxxx' time: 1695572469 action: 8 tid: 1695572445
#0xa306 CommandStatusResDTO: time: 1695572446 action: 8 tid: 1695572446
#0xa206 CommandStatusReqDTO: dtu_sn: b'xxxxxxxxxxxxx' time: 1695572471 action: 8 package_nub: 1 tid: 1695572445 mi_mOperatingStatus: [mi_sn: 22069994934680
#...
#0xa306 CommandStatusResDTO: time: 1695572450 action: 8 tid: 1695572450
#0xa206 CommandStatusReqDTO: dtu_sn: b'xxxxxxxxxxxxx' time: 1695572474 action: 8 package_nub: 1 tid: 1695572445 mi_sns_sucs: [22069994934680]

# Define the server address and port
server_address = ('192.168.1.203', 10081)

crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
sequence = 1

def SendPowerLevelCommand(client_socket,sequence):
    request = CommandPB_pb2.CommandResDTO()
    request.time = int(time.time())
    request.tid = int(time.time())
    request.action = 8
    request.package_nub = 1
    request.data = 'A:1000,B:0,C:0\r'.encode('utf-8')

    header = b'\x48\x4d\xa3\x05'
    crc = crc16(request.SerializeToString())
    length = len(request.SerializeToString())+10

    # Send the data
    #print(f"Sending: {header}{sequence.to_bytes(2,byteorder='big')}{crc.to_bytes(2, byteorder='big')}{length.to_bytes(2, byteorder='big')}{request.SerializeToString()}")
    print(f"Sending: ", end ='')
    for field_descriptor, value in request.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')
    client_socket.send(header+sequence.to_bytes(2,byteorder='big')+crc.to_bytes(2, byteorder='big')+length.to_bytes(2, byteorder='big')+request.SerializeToString())

    sequence=sequence+1
    # Receive the response
    response_data = client_socket.recv(1024)
    #print(f"Response: {response_data}")
    response = CommandPB_pb2.CommandReqDTO()
    response.ParseFromString(response_data[10:])
    print(f"Response: ", end ='')
    for field_descriptor, value in response.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')

def GetCommandStatus(client_socket,sequence):

    ret = False

    request = CommandPB_pb2.CommandResDTO()
    request.time = int(time.time())
    request.tid = int(time.time())
    request.action = 8

    header = b'\x48\x4d\xa3\x06'
    crc = crc16(request.SerializeToString())
    length = len(request.SerializeToString())+10

    # Send the data
    #print(f"Sending: {header}{sequence.to_bytes(2,byteorder='big')}{crc.to_bytes(2, byteorder='big')}{length.to_bytes(2, byteorder='big')}{request.SerializeToString()}")
    print(f"Sending: ", end ='')
    for field_descriptor, value in request.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')
    client_socket.send(header+sequence.to_bytes(2,byteorder='big')+crc.to_bytes(2, byteorder='big')+length.to_bytes(2, byteorder='big')+request.SerializeToString())

    sequence=sequence+1
    # Receive the response
    response_data = client_socket.recv(1024)
    #print(f"Response: {response_data}")
    response = CommandPB_pb2.CommandReqDTO()
    response.ParseFromString(response_data[10:])
    for field_descriptor, value in response.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
        if field_name == 'mi_mOperatingStatus':
            ret = False
        elif field_name == 'mi_sns_sucs':
            ret = True
        elif field_name == 'package_now':
            #assume no change done or status already requested, returning ok
            ret = True
    print('')
    return ret

try:
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    SendPowerLevelCommand(client_socket,sequence)

    print(f'Waiting for command processing ', end='')
    while not GetCommandStatus(client_socket,sequence):
        print(f'.', end='')
        time.sleep(1)

except Exception as e:
    print(f'Error: {e}')

finally:
    # Close the socket
    client_socket.close()
