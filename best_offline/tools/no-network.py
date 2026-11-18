"""Run a Python module with Python socket connections and DNS forbidden."""
import runpy
import socket
import sys


def blocked(*args, **kwargs):
    raise RuntimeError("Network access is forbidden during this offline operation")


socket.socket.connect = blocked
socket.socket.connect_ex = blocked
socket.create_connection = blocked
socket.getaddrinfo = blocked
if len(sys.argv) < 2:
    raise SystemExit("Usage: python no-network.py MODULE [arguments]")
module = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_module(module, run_name="__main__", alter_sys=True)
