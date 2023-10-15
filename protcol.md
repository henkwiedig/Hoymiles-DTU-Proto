# Message Structure

## Header
```
\x48\x4d #HM
```
##  Command

App -> DTU start with 0xa3, responses start 0xa2

2 Byte one of:

| Command Data | Command
--- | ---
-23807 -> \xa3\x01 | Request: APPInfoDataResDTO, Response APPInfoDataReqDTO
-23806 -> \xa3\x02 | Request: HBResDTO, Response HBReqDTO
-23805 -> \xa3\x03 | Request: RealDataResDTO   
-23804 -> \xa3\x04 | Request: WInfoResDTO  
-23803 -> \xa3\x05 | Request: CommandResDTO
-23802 -> \xa3\x06 | Request: CommandStatusResDTO, Response: CommandStatusReqDTO
-23801 -> \xa3\x07 | Request: DevConfigFetchResDTO
-23800 -> \xa3\x08 | Request: DevConfigPutResDTO
-23799 -> \xa3\x09 | Request: GetConfig
-23792 -> \xa3\x10 | Request: SetConfig
-23791 -> \xa3\x11 | Request: RealResDTO
-23790 -> \xa3\x12 | Request: GPSTResDTO
-23789 -> \xa3\x13 | Request: AutoSearch 
-23788 -> \xa3\x14 | Request: NetworkInfoRes, Response: NetworkInfoReq
-23787 -> \xa3\x15 | Request: AppGetHistPowerRes, Response: AppGetHistPowerReq
-23786 -> \xa3\x16 | Request: AppGetHistEDRes, Response: AppGetHistEDReq
-31999 -> \x83\x01 | Request: HBResDTO
-31998 -> \x83\x02 | Request: RegisterResDTO
-31997 -> \x83\x03 | Request: StorageDataRes
-31995 -> \x83\x05 | Request: CommandResDTO
-31994 -> \x83\x06 | Request: CommandStatusResDTO
-31993 -> \x83\x07 | Request: DevConfigFetchResDTO
-31992 -> \x83\x08 | Request: DevConfigPutResDTO
-9464  -> \xdb\x08 | Request: GetConfigRes
-9465  -> \xdb\x07 | Request: SetConfigRes

## Sequence-Counter
```
2 Byte increment per message
```
## CRC-16/MODBUS of payload
```
2 Byte
```
CRC Params:
| Check	| Poly | Init	| RefIn	| RefOut | XorOut
| --- | --- | --- | --- | --- | ---
0x4B37 | 0x8005 | 0xFFFF | true | true | x0000

##  Total length 
```
2 Byte
```
##  Payload (protobuf)
```protobuf message```




# compile prot files to python code
```
for file in $(ls protobuf/*.proto)
do
  protoc -I=protobuf --python_out=. $file
done
```