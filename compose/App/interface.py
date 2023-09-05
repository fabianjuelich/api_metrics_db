from xmlrpc.server import SimpleXMLRPCServer
import app

class RPC_Server:
    def test(self):
        return '{"f": "foo", "b": "bar"}'
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900))
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()
