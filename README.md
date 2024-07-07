## Fishing Net: Python MQL5 Terminal REST API Server

This project provides a Python-based REST API server for interacting with the MQL5 Terminal. 


### Overview

Fishing Net acts as a bridge between your applications and the MQL5 Terminal, a powerful environment for developing, testing, and deploying trading algorithms on MetaTrader platforms. 

Through this API, you can send commands, retrieve data, and manage your MQL5 applications directly from your Python code or Programming language of your choice.


### Installation

**Requirements:**

* Python (3.12.4) or above 
* Poetry (package manager) - [https://pypi.org/project/poetry/](https://pypi.org/project/poetry/)

**Instructions:**

1. Clone this repository:

```bash
git clone https://github.com/FishTools/Fishing-net
```

2. Navigate to the project directory:

```bash
cd fishing-net
```

3. Install dependencies using Poetry:

```bash
poetry install
```


### Running the Program

**Development Mode:**

Start the server in development mode for interactive testing and debugging:

```bash
poetry run fastapi dev fishing_net/main.py
```

This will launch the API server and provide a user interface (Swagger) for exploring available endpoints at `http://127.0.0.1:8000/docs`.

**Production Mode:**

For production use, run the server in production mode:

```bash
poetry run fastapi run fishing_net/main.py
```


### License

This project is licensed under the MIT License. See the `LICENSE` file for details.


### Contribution

We welcome contributions to this project! Please refer to the `CONTRIBUTING.md` file for guidelines on how to submit pull requests and report issues.

### MQL5 Python Functions needs to implement

| Completed<br> | Function<br> | Action<br> |
|---|---|---|
| :x: | login<br> | Connect to a trading account using specified parameters<br> |
| version<br> | Return the MetaTrader 5 terminal version<br> |
| account_info<br> | Get info on the current trading account<br> |
| terminal_Info<br> | Get status and parameters of the connected MetaTrader 5 terminal<br> |
| symbols_total<br> | Get the number of all financial instruments in the MetaTrader 5 terminal<br> |
| symbols_get<br> | Get all financial instruments from the MetaTrader 5 terminal<br> |
| symbol_info<br> | Get data on the specified financial instrument<br> |
| symbol_info_tick<br> | Get the last tick for the specified financial instrument<br> |
| symbol_select<br> | Select a symbol in the MarketWatch window or remove a symbol from the window<br> |
| market_book_add<br> | Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol<br> |
| market_book_get<br> | Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol<br> |
| market_book_release<br> | Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol<br> |
| copy_rates_from<br> | Get bars from the MetaTrader 5 terminal starting from the specified date<br> |
| copy_rates_from_pos<br> | Get bars from the MetaTrader 5 terminal starting from the specified index<br> |
| copyrates_range<br> | Get bars in the specified date range from the MetaTrader 5 terminal<br> |
| copy_ticks_from<br> | Get ticks from the MetaTrader 5 terminal starting from the specified date<br> |
| copy_ticks_range<br> | Get ticks for the specified date range from the MetaTrader 5 terminal<br> |
| orders_total<br> | Get the number of active orders.<br> |
| orders_get<br> | Get active orders with the ability to filter by symbol or ticket<br> |
| order_calc_margin<br> | Return margin in the account currency to perform a specified trading operation<br> |
| order_calc_profit<br> | Return profit in the account currency for a specified trading operation<br> |
| order_check<br> | Check funds sufficiency for performing a required trading operation<br> |
| order_send<br> | Send a request to perform a trading operation.<br> |
| positions_total<br> | Get the number of open positions<br> |
| positions_get<br> | Get open positions with the ability to filter by symbol or ticket<br> |
| history_orders_total<br> | Get the number of orders in trading history within the specified interval<br> |
| history_orders_get<br> | Get orders from trading history with the ability to filter by ticket or position<br> |
| history_deals_total<br> | Get the number of deals in trading history within the specified interval<br> |
| history_deals_get<br> | Get deals from trading history with the ability to filter by ticket or position<br> |


### Roadmap

* Implement support for additional MQL5 Terminal functionalities.
* Enhance security features for production environments.
* Integrate unit and integration testing frameworks.
* Provide comprehensive documentation for API endpoints.

This roadmap is not exhaustive and may evolve based on community feedback and project needs.
