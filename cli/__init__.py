import sys
import signal

def signal_handler(sig, frame):
    # Signal handler to handle SIGINT, usually when Ctrl+C is pressed.. or if SIGINT is sent.
    # Thanks to https://stackoverflow.com/a/1112350/92837
    print('\nCaught interrupt(did you press Ctrl+C?), stopping gitlab-bk')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)