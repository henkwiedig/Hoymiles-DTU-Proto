#!/usr/bin/env python3
import struct
import AppGetHistPower_pb2
import APPInfomationData_pb2
import APPHeartbeatPB_pb2
import AppGetHistED_pb2
import CommandPB_pb2
import NetworkInfo_pb2
import GetConfig_pb2
import SetConfig_pb2
import RealData_pb2
import AlarmData_pb2
import sys
import crcmod.predefined

def printfields(message):
    for field_descriptor, value in message.ListFields():
        field_name = field_descriptor.name
        field_value = value
        print(f"{field_name}: {field_value} ", end='')
    print('')

def decode_AppGetHistPowerRes(data):
    message = AppGetHistPower_pb2.AppGetHistPowerRes()
    message.ParseFromString(data)
    printfields(message)

def decode_AppGetHistPowerReq(data):
    message = AppGetHistPower_pb2.AppGetHistPowerReq()
    message.ParseFromString(data)
    printfields(message)

def decode_HBResDTO(data):
    message = APPHeartbeatPB_pb2.HBResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_HBReqDTO(data):
    message = APPHeartbeatPB_pb2.HBReqDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_APPInfoDataResDTO(data):
    message = APPInfomationData_pb2.APPInfoDataResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_APPInfoDataReqDTO(data):
    message = APPInfomationData_pb2.APPInfoDataResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_CommandResDTO(data):
    message = CommandPB_pb2.CommandResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_CommandReqDTO(data):
    message = CommandPB_pb2.CommandReqDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_AppGetHistEDRes(data):
    message = AppGetHistED_pb2.AppGetHistEDRes()
    message.ParseFromString(data)
    printfields(message)

def decode_AppGetHistEDReq(data):
    message = AppGetHistED_pb2.AppGetHistEDReq()
    message.ParseFromString(data)
    printfields(message)

def decode_CommandStatusResDTO(data):
    message = CommandPB_pb2.CommandStatusResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_CommandStatusReqDTO(data):
    message = CommandPB_pb2.CommandStatusReqDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_NetworkInfoRes(data):
    message = NetworkInfo_pb2.NetworkInfoRes()
    message.ParseFromString(data)
    printfields(message)

def decode_NetworkInfoReq(data):
    message = NetworkInfo_pb2.NetworkInfoReq()
    message.ParseFromString(data)
    printfields(message)

def decode_GetConfigRes(data):
    message = GetConfig_pb2.GetConfigRes()
    message.ParseFromString(data)
    printfields(message)

def decode_GetConfigReq(data):
    message = GetConfig_pb2.GetConfigReq()
    message.ParseFromString(data)
    printfields(message)

def decode_SetConfigRes(data):
    message = SetConfig_pb2.SetConfigRes()
    message.ParseFromString(data)
    printfields(message)

def decode_SetConfigReq(data):
    message = SetConfig_pb2.SetConfigReq()
    message.ParseFromString(data)
    printfields(message)

def decode_RealResRes(data):
    message = RealData_pb2.RealDataResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_RealResReq(data):
    message = RealData_pb2.RealDataReqDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_WInfoResRes(data):
    message = AlarmData_pb2.WInfoResDTO()
    message.ParseFromString(data)
    printfields(message)

def decode_WInfoResReq(data):
    message = AlarmData_pb2.WInfoReqDTO()
    message.ParseFromString(data)
    printfields(message)

crc16_modbus = crcmod.predefined.Crc('modbus')

# Open the binary file for reading
with open(sys.argv[1], "rb") as file:
    while True:
        # Read the 'HM' and header fields
        header_data = file.read(10)  # Adjusted for the 2-byte total length field

        # Break the loop if no more data is left
        if len(header_data) < 10:  # Adjusted for the 2-byte total length field
            break

        hm, command, sequence_counter, crc16, packet_length = struct.unpack(">2s H H H H", header_data)

        # Read the payload based on the packet_length
        payload = file.read(packet_length - 10)  # Subtract 10 for the header size

        if crc16 != crc16_modbus.new(payload).crcValue:
            print("CRC Error !!!")
            continue

        # Process the packet data as needed
        if command == 0xa315:
            print(f"0xa315 AppGetHistPowerRes: ", end='')
            decode_AppGetHistPowerRes(payload)
        elif command == 0xa215:
            print(f"0xa215 AppGetHistPowerReq: ", end='')
            decode_AppGetHistPowerReq(payload)
        elif command == 0xa301:
            print(f"0xa301 APPInfoDataResDTO: ", end='')
            decode_APPInfoDataResDTO(payload)
        elif command == 0xa201:
            print(f"0xa201 APPInfoDataReqDTO: ", end='')
            decode_APPInfoDataReqDTO(payload)
        elif command == 0xa302:
            print(f"0xa302 HBResDTO: ", end='')
            decode_HBResDTO(payload)
        elif command == 0xa202:
            print(f"0xa202 HBReqDTO: ", end='')
            decode_HBReqDTO(payload)
        elif command == 0xa305:
            print(f"0xa305 CommandResDTO: ", end='')
            decode_CommandResDTO(payload)
        elif command == 0xa205:
            print(f"0xa205 CommandReqDTO: ", end='')
            decode_CommandReqDTO(payload)
        elif command == 0xa316:
            print(f"0xa316 AppGetHistEDRes: ", end='')
            decode_AppGetHistEDRes(payload)
        elif command == 0xa216:
            print(f"0xa216 AppGetHistEDReq ", end='')
            decode_AppGetHistEDReq(payload)
        elif command == 0xa306:
            print(f"0xa306 CommandStatusResDTO: ", end='')
            decode_CommandStatusResDTO(payload)
        elif command == 0xa206:
            print(f"0xa206 CommandStatusReqDTO: ", end='')
            decode_CommandStatusReqDTO(payload)
        elif command == 0xa314:
            print(f"0xa314 NetworkInfoRes: ", end='')
            decode_NetworkInfoRes(payload)
        elif command == 0xa214:
            print(f"0xa214 NetworkInfoReq: ", end='')
            decode_NetworkInfoReq(payload)
        elif command == 0xa309:
            print(f"0xa309 GetConfigRes: ", end='')
            decode_GetConfigRes(payload)
        elif command == 0xa209:
            print(f"0xa209 GetConfigReq: ", end='')
            decode_GetConfigReq(payload)
        elif command == 0xa310:
            print(f"0xa310 SetConfigRes: ", end='')
            decode_SetConfigRes(payload)
        elif command == 0xa210:
            print(f"0xa210 SetConfigReq: ", end='')
            decode_SetConfigReq(payload)
        elif command == 0xa311:
            print(f"0xa311 RealResRes: ", end='')
            decode_RealResRes(payload)
        elif command == 0xa211:
            print(f"0xa211 RealResReq: ", end='')
            decode_RealResReq(payload)
        elif command == 0xa304:
            print(f"0xa304 WInfoRes: ", end='')
            decode_WInfoResRes(payload)
        elif command == 0xa204:
            print(f"0xa204 WInfoRes: ", end='')
            decode_WInfoResReq(payload)
        else:
            #print(f"HM: {hm.decode('utf-8')}, Command: {command}, Sequence Counter: {sequence_counter}, CRC16: {crc16}, Packet Length: {packet_length}")
            #print(f"Header: {header_data}")
            #print(f"Payload: {payload}")
            print(f"{command:x}: unsuppoted")

# Close the file when done
file.close()
