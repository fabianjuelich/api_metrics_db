from xmlrpc.server import SimpleXMLRPCServer
import app
from sort import Sort
from api import Api
import findata as findata
import json

# RPC procedures #

class RPC_Server:
    def metrics(self, sort: int, symbols: str, country_codes: str, api: int):
        api = Api(api)
        api = findata.AlphaVantage() if api is Api.ALPHA_VANTAGE else \
            findata.Leeway() if api is Api.LEEWAY else \
            findata.FinancialModelingPrep() if api is Api.FINANCIAL_MODELING_PREP \
            else None
        return json.dumps(app.document(Sort(sort), symbols, country_codes, api))
    
    def help(self):
        return '\t\tsymbols\tcountry_codes\nSORT.INDEX:\t1..*\t0\nSORT.MARKET:\t0\t1..*\nSORT.STOCK:\t1..*\t1'
    
# server setup #
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900), allow_none=True)
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()
