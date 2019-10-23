import threading
import tcpdump_flask
import time

x = threading.Thread(target=tcpdump_flask.tcpdump_run())
x.start()
time.sleep(10)
x.join()