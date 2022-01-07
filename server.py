from multiprocessing.connection import Listener

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
with Listener(address, authkey=b'secret password') as listener:
    listen=True
    while listen:
        with listener.accept() as conn:
            print('connection accepted from ', listener.last_accepted, flush=True)
            while True:
                try:
                    msg = conn.recv()
                except EOFError:
                    conn.close()
                    break
                else:    
                    # do something with msg
                    if msg == 'close':
                        conn.close()
                        listen=False
                        break
                    print("Received: ", msg)
    listener.close()