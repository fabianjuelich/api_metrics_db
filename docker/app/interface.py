from xmlrpc.server import SimpleXMLRPCServer
import app
from datetime import datetime
from type import TYPE
from api import API
import findata as findata
import json

# RPC procedures #

class RPC_Server:
    def metrics(self, typ: int, symbol: str, country: str, api: int):
        api = API(api)
        api = findata.AlphaVantage() if api is API.ALPHA_VANTAGE else \
            findata.Leeway() if api is API.LEEWAY else \
            findata.FinancialModelingPrep() if api is API.FINANCIAL_MODELING_PREP \
            else None
        doc = {}
        doc['timestamp'] = str(datetime.now())
        doc['data'] = app.document(TYPE(typ), symbol, country, api)
        return (json.dumps(doc))
    
# server setup #
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900), allow_none=True)
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()
