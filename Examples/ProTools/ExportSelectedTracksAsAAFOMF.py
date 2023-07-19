import json
import urllib.parse
import uuid
import time
import socket

def send_message_to_sweejhelper(message):
    print(f"Sending URL: {message}")

    print("Creating socket connection...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Connecting to the server...")
    client_socket.connect(('localhost', 65500))  # use the same port number as in your Swift application

    print("Sending message to the server...")
    client_socket.send(message.encode('utf-8'))

    print("Shutting down write part of the socket...")
    client_socket.shutdown(socket.SHUT_WR)

    # Set a timeout for receiving the response
    client_socket.setblocking(0)  # non-blocking mode

    start_time = time.time()
    response = b""

    while True:
        try:
            print("Attempting to receive data from the server...")
            chunk = client_socket.recv(4096)  # receive data from the server
            if chunk:
                print("Received data chunk from the server.")
                response += chunk
            else:
                # No more data to receive
                break
        except socket.error:
            # No data received, sleep for a bit before retrying
            print("No data received, sleeping for a bit before retrying...")
            time.sleep(2)  # Add a delay to allow server to finish receiving

    print("Closing client socket connection...")
    client_socket.close()

    # Parse the response as a JSON object
    if response:
        try:
            response_json = json.loads(response.decode('utf-8'))
            print(f"Received response: {response_json}")
        except json.JSONDecodeError:
            print("Did not receive a valid JSON response from the server")

# Generate a unique request id
request_id = str(uuid.uuid4())

# Prepare the arguments
arguments = {
    "fileType": "WAV",  # Choose from: "WAV", "AIFF", "MXF", "Embedded"
    "bitDepth": "Bit16",  # Choose from: "Bit16", "Bit24"
    "copyOption": "ConsolidateFromSourceMedia",  # Choose from: "ConsolidateFromSourceMedia", "CopyFromSourceMedia", "LinkFromSourceMedia"
    "enforceMediaComposerCompatibility": True,
    "quantizeEditsToFrameBoundaries": True,
    "exportStereoAsMultichannel": True,
    "containerFileName": "myContainerFile",  # Replace with desired file name for the exported container file
    "containerFileLocation": "/path/to/containerFileLocation/",  # Replace with actual container file location, make sure ends in /
    "assetFileLocation": "/path/to/assetFileLocation/",  # Replace with actual asset file location, make sure ends in /
    "comments": "These are my comments",  # Replace with actual comments
    "sequenceName": "mySequence"  # Replace with desired sequence name
}

# Convert the arguments to a JSON string
arguments_json = json.dumps(arguments)

# URL encode the JSON string
arguments_encoded = urllib.parse.quote(arguments_json, safe='')

# Prepare the message
message = f'sweejhelper://proToolsFunction/exportSelectedTracksAsAAFOMF/{request_id}?arguments={arguments_encoded}'

# Send a request to export the selected tracks as AAF/OMF
send_message_to_sweejhelper(message)