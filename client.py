from multiprocessing.connection import Client
import sys

address = ('localhost', 6000)
conn = Client(address, authkey=b'blahblah')
test={'msg': sys.argv[1] }
conn.send(test)
conn.send(sys.argv[1])
# conn.send('close')
# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])
conn.close()