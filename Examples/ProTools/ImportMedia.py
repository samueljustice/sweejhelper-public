import sys
import socket
import json
import uuid
import time
import urllib.parse
import os

print(sys.version)
print(sys.executable)

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

# Arguments to pass to the 'importMedia' function
# Available argument options:
# "sessionPath" [type: str, example: "/path/to/session"],
# "importType" [type: str, options: "Session", "Audio", "Video", "MIDI", "ClipGroups" (default)],
# "audioOptions" [type: str, options: "LinkToSource", "CopyFromSource", "ConsolidateFromSource", "ForceToTargetSessionFormat" (default)],
# "audioHandleSize" [type: int, example: 1024],
# "videoOptions" [type: str, options: "LinkToSource", "CopyFromSource" (default)],
# "matchOptions" [type: str, options: "None", "MatchTracks", "ImportAsNewTrack" (default)],
# "playlistOptions" [type: str, options: "ImportReplaceExistingPlaylists", "ImportOverlayNewOnExistingPlaylists", "DoNotImport" (default)],
# "trackDataPresetPath" [type: str, example: "/path/to/preset"],
# "clipGain" [type: bool, example: True],
# "clipsAndMedia" [type: bool, example: True],
# "volumeAutomation" [type: bool, example: True],
# "timeCodeMappingOptions" [type: str, options: "MaintainAbsoluteTimeCodeValues", "MaintainRelativeTimeCodeValues", "MapStartTimeCodeTo" (default)],
# "timeCodeMappingStartTime" [type: str, example: "00:00:00:00"],
# "adjustSessionStartTimeToMatchSource" [type: bool, example: True],
# "filesList" [type: list, example: ["/path/to/media/file1", "/path/to/media/file2"]],
# "audioOperations" [type: str, options: "Add", "Copy", "Convert", "Default" (default)],
# "destination" [type: str, options: "None", "MainVideoTrack", "NewTrack", "ClipList" (default)],
# "location" [type: str, options: "None", "SessionStart", "SongStart", "Selection", "Spot" (default)]
arguments = {
    "sessionPath": "/path/to/session",
    "importType": "Audio",
    "audioOptions": "ForceToTargetSessionFormat",
    "audioHandleSize": 1024,
    "videoOptions": "CopyFromSource",
    "matchOptions": "ImportAsNewTrack",
    "playlistOptions": "DoNotImport",
    "trackDataPresetPath": "/path/to/preset",
    "clipGain": True,
    "clipsAndMedia": True,
    "volumeAutomation": True,
    "timeCodeMappingOptions": "MapStartTimeCodeTo",
    "timeCodeMappingStartTime": "00:00:00:00",
    "adjustSessionStartTimeToMatchSource": True,
    "filesList": ["/path/to/media/file1", "/path/to/media/file2"]
    "audioOperations": "Default",
    "destination": "ClipList",
    "location": "Spot"
}

# Convert the arguments to a JSON string
json_arguments = json.dumps(arguments)

# URL encode the JSON arguments
encoded_arguments = urllib.parse.quote(json_arguments)

# Send a request to import media, including the request id and arguments in the URL
send_message_to_sweejhelper(f'sweejhelper://proToolsFunction/importMedia/{request_id}?arguments={encoded_arguments}')
