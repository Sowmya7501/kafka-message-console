import argparse
import os
from google.protobuf import json_format, descriptor_pb2, descriptor_pool, message_factory

def load_message_descriptor(fd_path, msg_name):
    # Read the file descriptor
    if not os.path.exists(fd_path):
        raise FileNotFoundError(f"File not found: {fd_path}")
    
    with open(fd_path, 'rb') as f:
        file_content = f.read()

    # Unmarshal the file descriptor set
    file_set = descriptor_pb2.FileDescriptorSet()
    file_set.ParseFromString(file_content)

    # Create a descriptor pool and add the file descriptors
    pool = descriptor_pool.DescriptorPool()
    for fd_proto in file_set.file:
        pool.Add(fd_proto)

    # Find the message descriptor
    try:
        message_descriptor = pool.FindMessageTypeByName(msg_name)
        return message_descriptor
    except KeyError:
        raise ValueError(f"Unable to find message named {msg_name} in file descriptor")

def validate_message_with_descriptor(json_message, msg_descriptor):
    # Create a message factory
    factory = message_factory.MessageFactory()

    # Get the message class from the descriptor
    message_class = factory.GetPrototype(msg_descriptor)

    # Create an instance of the message
    dymsg = message_class()

    # Unmarshal JSON string into the message
    try:
        json_format.Parse(json_message, dymsg)
        return True, None
    except json_format.ParseError as e:
        return False, str(e)

def protobuf_validate_message(descriptor, name):
    # Load the message descriptor
    message_descriptor = load_message_descriptor(descriptor, name)
    
    user_input = input("Enter the message in JSON format (or q to quit): ")
    
    # Validate the message
    is_valid, error = validate_message_with_descriptor(user_input, message_descriptor)
    if is_valid:
        print("Message validated successfully.")
    else:
        print(f"Message validation failed with json error: {error}")

# def parse_arguments():
#     parser = argparse.ArgumentParser(description='Validate JSON message against Protobuf schema')
#     parser.add_argument('--descriptor', type=str, required=True, help='File descriptor path')
#     parser.add_argument('--name', type=str, required=True, help='Fully qualified Proto message name')
#     parser.add_argument('--message', type=str, required=True, help='JSON message to validate')
#     return parser.parse_args()

# def main():
#     args = parse_arguments()
    
#     # Load the message descriptor
#     message_descriptor = load_message_descriptor(args.descriptor, args.name)
    
#     # Validate the message
#     is_valid, error = validate_message(args.message, message_descriptor)
#     if is_valid:
#         print("Message validated successfully.")
#     else:
#         print(f"Validation failed: {error}")