from src.config.database import lifespan
from src.config.exceptions import exception_handlers
from src.views.balance import CustomersBalance
from src.views.homepage import Homepage
from src.views.transactions import CustomersTransactions
from starlette.applications import Starlette
from starlette.routing import Route

routes = [
    Route("/", Homepage),
    Route("/clientes/{id}/transacoes", CustomersTransactions),
    Route("/clientes/{id}/extrato", CustomersBalance),
]

app = Starlette(
    routes=routes,
    lifespan=lifespan,
    exception_handlers=exception_handlers,
)
