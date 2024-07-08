from fastapi import FastAPI
import MetaTrader5 as mt5
import fishing_net.routes.security as security
import fishing_net.routes.account as account
import fishing_net.routes.terminal as terminal
import fishing_net.routes.symbols as symbols
import fishing_net.routes.ticks as ticks
import fishing_net.routes.rates as rates
import fishing_net.routes.orders as orders
import fishing_net.routes.position as position
import fishing_net.routes.history as history

mt5.initialize()
app = FastAPI()
app.include_router(security.router, prefix="/security")
app.include_router(account.router, prefix="/account")
app.include_router(terminal.router, prefix="/terminal")
app.include_router(symbols.router, prefix="/symbols")
app.include_router(ticks.router, prefix="/ticks")
app.include_router(rates.router, prefix="/rates")
app.include_router(orders.router, prefix="/orders")
app.include_router(position.router, prefix="/position")
app.include_router(history.router, prefix="/history")
