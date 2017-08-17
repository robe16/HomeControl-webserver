from multiprocessing import Process, Manager
import sys
import cfg
from port_listener import start_bottle
from cache.get_cache import create_cache
from log.console_messages import print_msg


################################
# Receive sys arguments
################################
try:
    self_port = sys.argv[1]
except:
    self_port = 8080
#
################################
# Shared variable for processes
################################
cache = Manager().dict()
cache['setup'] = {}
cache['users'] = {}
cache['tvchannels'] = {}
#
################################

if __name__ == "__main__":
    #
    ################################
    # Process for building caches
    ################################
    print_msg('Starting process: Cache')
    process_cache = Process(target=create_cache, args=(cache, ))
    process_cache.start()
    print_msg('Process started: Cache')
    #
    ################################
    # Process for port_listener
    ################################
    print_msg('Starting process: "bottle" server on port {port}'.format(port=self_port))
    process_bottle = Process(target=start_bottle, args=(cache, self_port, ))
    process_bottle.start()
    print_msg('Process started: "bottle" server on port {port}'.format(port=self_port))
    #
    ################################
    # Use .join() to ensure main process with Manager() items remains open
    ################################
    process_cache.join()
    process_bottle.join()
    #
    ################################
