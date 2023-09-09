from xmlrpc.server import SimpleXMLRPCServer
import app

class RPC_Server:
    def metrics(self):
        return app.document()
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900))
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()
