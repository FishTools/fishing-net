from typing import Optional
from pydantic import BaseModel


class MQLAccountInfo(BaseModel):
    login: int
    trade_mode: int
    leverage: int
    limit_orders: int
    margin_so_mode: int
    trade_allowed: bool
    trade_expert: bool
    margin_mode: int
    currency_digits: int
    fifo_close: bool
    balance: float
    credit: float
    profit: float
    equity: float
    margin: float
    margin_free: float
    margin_level: float
    margin_so_call: float
    margin_so_so: float
    margin_initial: float
    margin_maintenance: float
    assets: float
    liabilities: float
    commission_blocked: float
    name: str
    server: str
    currency: str
    company: str


class MQLTerminalInfo(BaseModel):
    community_account: bool
    community_connection: bool
    connected: bool
    dlls_allowed: bool
    trade_allowed: bool
    tradeapi_disabled: bool
    email_enabled: bool
    ftp_enabled: bool
    notifications_enabled: bool
    mqid: int
    build: int
    maxbars: int
    codepage: int
    ping_last: int
    community_balance: float
    retransmission: int
    company: str
    name: str
    language: str
    path: str
    data_path: str
    commondata_path: str


class MQLSymbolInfo(BaseModel):
    custom: bool
    chart_mode: int
    select: bool
    visible: bool
    session_deals: int
    session_buy_orders: int
    session_sell_orders: int
    volume: int
    volumehigh: int
    volumelow: int
    time: int
    digits: int
    spread: int
    spread_float: bool
    ticks_bookdepth: int
    trade_calc_mode: int
    trade_mode: int
    start_time: int
    expiration_time: int
    trade_stops_level: int
    trade_freeze_level: int
    trade_exemode: int
    swap_mode: int
    swap_rollover3days: int
    margin_hedged_use_leg: bool
    expiration_mode: int
    filling_mode: int
    order_mode: int
    order_gtc_mode: int
    option_mode: int
    option_right: int
    bid: float
    bidhigh: float
    bidlow: float
    ask: float
    askhigh: float
    asklow: float
    last: float
    lasthigh: float
    lastlow: float
    volume: int
    volumehigh_real: int
    volumelow_real: int
    option_strike: float
    point: float
    trade_tick_value: float
    trade_tick_value_profit: float
    trade_tick_value_loss: float
    trade_tick_size: float
    trade_contract_size: float
    trade_accrued_interest: float
    trade_face_value: float
    trade_liquidity_rate: float
    volume_min: int
    volume_max: int
    volume_step: int
    volume_limit: int
    swap_long: float
    swap_short: float
    margin_initial: float
    margin_maintenance: float
    session_volume: int
    session_turnover: float
    session_interest: float
    session_buy_orders_volume: int
    session_sell_orders_volume: int
    session_open: int
    session_close: int
    session_aw: int
    session_price_settlement: int
    session_price_limit_min: int
    session_price_limit_max: int
    margin_hedged: float
    price_change: float
    price_volatility: float
    price_theoretical: float
    price_greeks_delta: float
    price_greeks_theta: float
    price_greeks_gamma: float
    price_greeks_vega: float
    price_greeks_rho: float
    price_greeks_omega: float
    price_sensitivity: float
    basis: Optional[float] = None
    category: Optional[str] = None
    currency_base: str
    currency_profit: str
    currency_margin: str
    bank: Optional[str] = None
    description: str
    exchange: Optional[str] = None
    formula: Optional[str] = None
    isin: Optional[str] = None
    name: str
    page: str
    path: str


class MQLSymbolTick(BaseModel):
    time: int
    bid: float
    ask: float
    last: float
    volume: int
    time_msc: int
    flags: int
    volume_real: int


class MQLSymbolRates(BaseModel):
    time: int
    open: float
    high: float
    low: float
    close: float
    tick_volume: int
    spread: int
    real_volume: int


class MQLOrder(BaseModel):
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_expiration: int
    type: int
    type_time: int
    type_filling: int
    state: int
    magic: int
    volume_current: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    symbol: str
    comment: str
    external_id: int


class MQLTradeRequest(BaseModel):
    action: str
    magic: int
    order: int
    symbol: str
    volume: float
    price: float
    stoplimit: float
    sl: float
    tp: float
    deviation: int
    type: int
    type_filling: int
    type_time: int
    expiration: int
    comment: str
    position: int
    position_by: int


class MQLLoginCredentials(BaseModel):
    login: int
    password: str | None = None
    server: str | None = None
    timeout: int | None = None


class MQLPosition(BaseModel):
    ticket: int
    time: int
    type: int
    magic: int
    identifier: int
    reason: int
    volume: float
    price_open: float
    sl: float
    tp: float
    price_current: float
    swap: float
    profit: float
    symbol: str
    comment: Optional[str] = None


class MQLHistoryOrder(BaseModel):
    ticket: int
    time_setup: int
    time_setup_msc: int
    time_done: int  # datetime
    time_done_msc: int
    type: int
    type_filling: int
    magic: int
    position_id: int
    volume_initial: float
    price_open: float
    price_current: float
    symbol: str
    comment: str
    external_id: int


class MQLHistoryDeal(BaseModel):
    ticket: int
    order: int
    time: int
    time_msc: int
    type: int
    entry: float
    magic: int
    position_id: int
    reason: int
    volume: float
    price: float
    commission: float
    swap: float
    profit: float
    fee: float
    symbol: str
    comment: str
    external_id: int
