import unittest
import subprocess, os, signal
from context import arkouda as ak
from util.test.util import get_arkouda_server

'''
ArkoudaTest defines the base Arkouda test logic for starting up the arkouda_server at the 
launch of a unittest TestCase and shutting down the arkouda_server at the completion of
the unittest TestCase.

Note: each Arkouda TestCase class extends ArkoudaTest and encompasses 1..n test methods, the 
names of which match the pattern 'test*' (e.g., ArkoudaTest.test_arkouda_server).
'''
class ArkoudaTest(unittest.TestCase):

    verbose = True if os.getenv('ARKOUDA_VERBOSE') == 'True' else False
    port = int(os.getenv('ARKOUDA_SERVER_PORT', 5566))
    server = os.getenv('ARKOUDA_SERVER_HOST', 'localhost')
    full_stack_mode = True if os.getenv('ARKOUDA_FULL_STACK_TEST') == 'True' else False
    
    @classmethod
    def setUpClass(cls):
        '''
        Configures and starts the arkouda_server process via the util.get_arkouda_server (host) 
        and ARKOUDA_SERVER_PORT env variable, defaulting to 5566
        
        :return: None
        :raise: RuntimeError if there is an error in configuring or starting arkouda_server
        '''
        if ArkoudaTest.full_stack_mode:
            print('starting in full stack mode')
            try: 
                arkouda_path = get_arkouda_server() 
                ArkoudaTest.ak_server = subprocess.Popen([arkouda_path, 
                                              '--ServerPort={}'.format(ArkoudaTest.port), '--quiet'])
                print('Started arkouda_server in full stack test mode')
            except Exception as e:
                raise RuntimeError('in configuring or starting the arkouda_server: {}, check ' +
                         'environment and/or arkouda_server installation', e)
        else:
            print('in client stack test mode')
        

    def setUp(self):
        '''
        Connects an Arkouda client for each test case
        
        :return: None
        :raise: ConnectionError if exception is raised in connecting to arkouda_server
        '''
        try:
            ak.client.connect(server=ArkoudaTest.server, port=ArkoudaTest.port)
        except Exception as e:
            raise ConnectionError(e)
    
    def tearDown(self):
        '''
        Disconnects the client connection for each test case
        :return: None
        :raise: ConnectionError if exception is raised in connecting to arkouda_server
        '''
        try:
            ak.client.disconnect()
        except Exception as e:
            raise ConnectionError(e)

    @classmethod
    def tearDownClass(cls):
        '''
        Shuts down the arkouda_server started in the setUpClass method if test is run
        in full stack mode, noop if in client stack mode.

        :return: None
        :raise: RuntimeError if there is an error in shutting down arkouda_server
        '''
        if ArkoudaTest.full_stack_mode:
            try:
                os.kill(ArkoudaTest.ak_server.pid, signal.SIGTERM)
            except Exception as e:
                raise RuntimeError(e)