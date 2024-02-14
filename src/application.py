from src.views.customers_balance import CustomersBalance
from src.views.customers_transactions import CustomersTransactions
from src.views.homepage import Homepage
from starlette.applications import Starlette
from starlette.routing import Route

app = Starlette(
    debug=True,
    routes=[
        Route("/", Homepage),
        Route("/clientes/{id}/transacoes", CustomersTransactions),
        Route("/clientes/{id}/extrato", CustomersBalance),
    ],
)
