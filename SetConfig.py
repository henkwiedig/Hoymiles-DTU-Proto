#!/usr/bin/env python3
import socket
from protobuf_inspector.types import StandardParser
import GetConfig_pb2
import SetConfig_pb2
import time
import crcmod

print("Warning !!! This is not tested. Remove this if you are brave")
exit(0)

# Define the server address and port
server_address = ('192.168.1.203', 10081)

crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
sequence = 1

try:
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect(server_address)

    request = GetConfig_pb2.GetConfigRes()
    request.offset = 28800
    request.time = int(time.time())

    header = b'\x48\x4d\xa3\x09'
    crc = crc16(request.SerializeToString())
    length = len(request.SerializeToString())+10

    # Send the data
    print(f"Sending: {header}{sequence.to_bytes(2,byteorder='big')}{crc.to_bytes(2, byteorder='big')}{length.to_bytes(2, byteorder='big')}{request.SerializeToString()}")
    client_socket.send(header+sequence.to_bytes(2,byteorder='big')+crc.to_bytes(2, byteorder='big')+length.to_bytes(2, byteorder='big')+request.SerializeToString())

    sequence=sequence+1
    # Receive the response
    response_data = client_socket.recv(1024)
    print(f"Response: {response_data}")
    response = GetConfig_pb2.GetConfigReq()
    response.ParseFromString(response_data[10:])
    for field_descriptor, value in response.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')

    setconfig = SetConfig_pb2.SetConfigRes()
    setconfig.offset = 28800
    setconfig.time = int(time.time())
    setconfig.lock_time = response.lock_time
    setconfig.limit_power_mypower = response.limit_power_mypower
    setconfig.netmode_select = 1
    setconfig.server_send_time = 15
    setconfig.serverport = 10081
    setconfig.apn_set = 'NONE'.encode('utf-8')
    setconfig.meter_kind = response.meter_kind
    setconfig.meter_interface = response.meter_interface
    setconfig.wifi_ssid = 'change_me'.encode('utf-8')
    setconfig.wifi_passward = 'change_me'.encode('utf-8')
    setconfig.server_domain_name = 'dataeu.hoymiles.com'.encode('utf-8')
    setconfig.dtu_sn = response.dtu_sn
    setconfig.access_model = 1
    setconfig.apn_name = 'NONE'.encode('utf-8')
    setconfig.apn_passward = 'NONE'.encode('utf-8')
    setconfig.cable_dns_0 = 1
    setconfig.cable_dns_1 = 1
    setconfig.cable_dns_2 = 1
    setconfig.cable_dns_3 = 1
    setconfig.dtu_ap_ssid = response.dtu_ap_ssid
    setconfig.dtu_ap_pass = response.dtu_ap_pass
    setconfig.app_page = 1

    print(f"SetConfig: ",end='')
    for field_descriptor, value in setconfig.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')

    header = b'\x48\x4d\xa3\x10'
    crc = crc16(setconfig.SerializeToString())
    length = len(setconfig.SerializeToString())+10

    print(f"Sending: {header}{sequence.to_bytes(2,byteorder='big')}{crc.to_bytes(2, byteorder='big')}{length.to_bytes(2, byteorder='big')}{setconfig.SerializeToString()}")
    client_socket.send(header+sequence.to_bytes(2,byteorder='big')+crc.to_bytes(2, byteorder='big')+length.to_bytes(2, byteorder='big')+setconfig.SerializeToString())


    sequence=sequence+1
    # Receive the response
    response_data = client_socket.recv(1024)
    print(f"Response: {response_data}")
    response = SetConfig_pb2.SetConfigReq()
    response.ParseFromString(response_data[10:])
    for field_descriptor, value in response.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')

except Exception as e:
    print(f'Error: {e}')

finally:
    # Close the socket
    client_socket.close()
