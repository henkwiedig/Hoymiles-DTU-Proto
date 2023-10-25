import os

Import('env')

global_env = DefaultEnvironment()

def callback():
    print("Generate Protobuf headers....")
    os.system('protoc --plugin=protoc-gen-nanopb=./.pio/libdeps/esp32doit-devkit-v1/Nanopb/generator/protoc-gen-nanopb --nanopb_out=. include/proto/AppGetHistPower.proto')

global_env.AddPostAction("Run", callback())
