import argparse
import subprocess
import shutil

def generate_descriptor(proto_file, descriptor_file):
    # Ensure the protoc compiler is available
    if not shutil.which("protoc"):
        raise EnvironmentError("protoc compiler not found. Please install it from https://github.com/protocolbuffers/protobuf/releases")

    # Run the protoc command to generate the descriptor file
    command = [
        "protoc",
        "--descriptor_set_out={}".format(descriptor_file),
        "--include_imports",
        proto_file
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        print("Error generating descriptor file:")
        print(result.stderr)
    else:
        print("Descriptor file generated successfully at {}".format(descriptor_file))
