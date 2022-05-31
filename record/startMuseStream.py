"""
Starting a Stream
This example shows how to search for available Muses and
create a new stream
"""
from muselsl import stream, list_muses

if __name__ == "__main__":

    muses = list_muses(backend='bleak')

    if not muses:
        print('No Muses found')
    else:
        stream(muses[0]['address'], backend='bleak', timeout=10)

        # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
        print('Stream has ended')