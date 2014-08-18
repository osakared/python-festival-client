#!/usr/bin/env python3

# Python client for festival_server

import argparse
import socket
import sys
import festival_command

newline_bytes = b'\n'
ok_bytes = b'OK\n'

class FestivalClient(object):
    """Represents a socket connection to a festival_server"""

    def __init__(self, host, port):
        super(FestivalClient, self).__init__()
        self.host = host
        self.port = port
        self.socket = None

    def __del__(self):
        if self.socket:
            self.socket.close()
            self.socket = None

    def connect(self):
        """Tries to connect to given server and, if successful, sets self.socket to the socket connection"""

        for result in socket.getaddrinfo(self.host, self.port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, socket_type, proto, canonical_name, socket_address = result
            try:
                self.socket = socket.socket(af, socket_type, proto)
            except OSError as msg:
                self.socket = None
                continue
            try:
                self.socket.connect(socket_address)
            except OSError as msg:
                self.socket.close()
                self.socket = None
                continue
            break

        if self.socket is None:
            print('could not open socket')
            return False

        return True

    def send_message(self, message):
        """Sends a message to festival_server and returns a tuple of a list of scheme responses and a list of audio responses ([], [])"""

        if not self.socket: return

        # Send message
        self.socket.sendall(bytes(message, 'UTF-8'))

        # Always get response
        scheme_responses = []
        audio_responses = []
        current_response = bytes()
        # Can be 'get_type', 'get_scheme' or 'get_wav'
        state = 'get_type'
        while True:
            current_response += self.socket.recv(4096)
            if not current_response: break
            if state == 'get_type':
                if newline_bytes not in current_response: continue
                type_str, _, current_response = current_response.partition(newline_bytes)
                if type_str == b'WV': state = 'get_wav'
                elif type_str == b'LP': state = 'get_scheme'
                elif type_str == b'ER':
                    print("Received an error from festival")
                    break
                else:
                    print("Error: got unexpected response")
                    break
            if ok_bytes not in current_response: continue
            data_dump, _, current_response = current_response.partition(ok_bytes)
            if state == 'get_scheme':
                current_scheme_responses = data_dump.split(newline_bytes)
                current_scheme_responses.remove(b'ft_StUfF_key')
                scheme_responses += current_scheme_responses
            elif state == 'get_wav':
                audio_responses.append(data_dump)
            break
            # state = 'get_type'

        return scheme_responses, audio_responses


parser = argparse.ArgumentParser()
parser.description = 'A client for festival_server written in Python'
parser.add_argument('-a', '--address', help='Address to bind to', default='localhost')
parser.add_argument('-p', '--port', help='Port to listen on', type=int, default=1314) # same default port as festival_server
configuration = parser.parse_args()

festival_client = FestivalClient(configuration.address, configuration.port)
# If we can't connect, just spit out error and abort
if not festival_client.connect(): sys.exit(1)

# Startup console to forward commands to festival_server and show responses
festival_command.FestivalCommand(festival_client).cmdloop()