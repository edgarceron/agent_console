#!/usr/bin/env python3

import socket
import selectors
import types
import json

class AgentConsoleSocketClient():
    sel = selectors.DefaultSelector()
    message = 0

    def __init__(self, verbosity=False):
        self.verbosity = verbosity

    def start_connection(self, host, port, data):
        server_addr = (host, port)
        if self.verbosity:
            print("starting connection to", server_addr)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(server_addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(sock, events, data=data)

    def service_connection(self, key, mask):
        sock = key.fileobj
        try:
            if mask & selectors.EVENT_READ:
                recv_data = sock.recv(1024)  # Should be ready to read
                if recv_data:
                    if self.verbosity:
                        print("Client: received", repr(recv_data))
                if recv_data == "close":
                    if self.verbosity:
                        print("Client: closing connection")
                    self.sel.unregister(sock)
                    sock.close()
            if mask & selectors.EVENT_WRITE:
                if self.message:
                    if self.verbosity:
                        print("sending", repr(self.message), "to connection")
                    sock.send(self.message)  # Should be ready to write
                    self.message = 0
        except BlockingIOError:
            if self.verbosity:
                print("Socket bloqueado")

    def set_message(self, data):
        json_data = json.dumps(data)
        self.message = bytes(json_data, 'utf-8')

    def start_client(self):
        host = '127.0.0.1'
        port = 16899
        
        self.start_connection(host, int(port), None)

        try:
            while True:
                events = self.sel.select(timeout=1)
                if events:
                    for key, mask in events:
                        self.service_connection(key, mask)
                # Check for a socket being monitored to continue.
                if not self.sel.get_map():
                    break
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
