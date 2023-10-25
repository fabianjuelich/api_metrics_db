from xmlrpc.server import SimpleXMLRPCServer
import app
from sort import Sort
from api import Api
import findata as findata
import json

# RPC procedures #

class RPC_Server:
    def metrics(self, sort: int, symbols: str, country_codes: str, api: int):
        try:
            api = Api(api)
            api = findata.AlphaVantage() if api is Api.ALPHA_VANTAGE else \
                findata.Leeway() if api is Api.LEEWAY else \
                findata.FinancialModelingPrep() if api is Api.FINANCIAL_MODELING_PREP \
                else None
            return json.dumps(app.document(Sort(sort), symbols, country_codes, api))
        except Exception as e:
            print(e)
            help()
    
    def help(self):
        return f'''
lazy-investor - Help (server.help())

Cardinality:
sort        symbols country_codes api
SORT.INDEX     1..*             0   1
SORT.MARKET       0          1..*   1
SORT.STOCK     1..*             1   1

Values:
{[{c.__name__:dict([(o.value, o.name) for o in c])} for c in (Sort, Api)]}
'''

# server setup #
    
rpc_server = SimpleXMLRPCServer(("0.0.0.0", 2900), allow_none=True)
rpc_server.register_instance(RPC_Server())
rpc_server.serve_forever()