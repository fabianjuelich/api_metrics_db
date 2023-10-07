from xmlrpc.server import SimpleXMLRPCServer
import app
from datetime import datetime
from sort import Sort
from api import Api
import findata as findata
import json

# RPC procedures #

class RPC_Server:
    def metrics(self, typ: int, symbol: str, country: str, api: int):
        api = Api(api)
        api = findata.AlphaVantage() if api is Api.ALPHA_VANTAGE else \
            findata.Leeway() if api is Api.LEEWAY else \
            findata.FinancialModelingPrep() if api is Api.FINANCIAL_MODELING_PREP \
            else None
        doc = {}
        doc['timestamp'] = str(datetime.now())
        doc['data'] = app.document(Sort(typ), symbol, country, api)
        return (json.dumps(doc))
    
# server setup #
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900), allow_none=True)
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()
