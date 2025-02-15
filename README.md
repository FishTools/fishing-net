## Fishing Net: Python MQL5 Terminal REST API Server

This project provides a Python-based REST API server for interacting with the MQL5 Terminal. 


### Overview

Fishing Net acts as a bridge between your applications and the MQL5 Terminal, a powerful environment for developing, testing, and deploying trading algorithms on MetaTrader platforms. 

Through this API, you can send commands, retrieve data, and manage your MQL5 applications directly from your Python code or Programming language of your choice.

### Runs on Any Computer (But MQL5 Needs Windows)

This program works on your computer, no matter Windows, Mac, or Linux, as long as you have Python. However, to connect to the MQL5 program (it only runs on Windows), you'll need a separate Windows machine. Once connected, Fishing Net uses regular web stuff (HTTP) to talk to MQL5, so you can use any coding language you like.



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

Note:
- :white_check_mark: - Implemented and working
- :x: - Not yet implemented in the server

| Completed<br> | Function<br> | Action<br> |
|---|---|---|
| :white_check_mark: | login<br> | Connect to a trading account using specified parameters<br> |
| :white_check_mark: | version<br> | Return the MetaTrader 5 terminal version<br> |
| :white_check_mark: | account_info<br> | Get info on the current trading account<br> |
| :white_check_mark: | terminal_Info<br> | Get status and parameters of the connected MetaTrader 5 terminal<br> |
| :white_check_mark: | symbols_total<br> | Get the number of all financial instruments in the MetaTrader 5 terminal<br> |
| :white_check_mark: | symbols_get<br> | Get all financial instruments from the MetaTrader 5 terminal<br> |
| :white_check_mark: | symbol_info<br> | Get data on the specified financial instrument<br> |
| :white_check_mark: | symbol_info_tick<br> | Get the last tick for the specified financial instrument<br> |
| :white_check_mark: | symbol_select<br> | Select a symbol in the MarketWatch window or remove a symbol from the window<br> |
| :x: | market_book_add<br> | Subscribes the MetaTrader 5 terminal to the Market Depth change events for a specified symbol<br> |
| :x: | market_book_get<br> | Returns a tuple from BookInfo featuring Market Depth entries for the specified symbol<br> |
| :x: | market_book_release<br> | Cancels subscription of the MetaTrader 5 terminal to the Market Depth change events for a specified symbol<br> |
| :white_check_mark: | copy_rates_from<br> | Get bars from the MetaTrader 5 terminal starting from the specified date<br> |
| :white_check_mark: | copy_rates_from_pos<br> | Get bars from the MetaTrader 5 terminal starting from the specified index<br> |
| :white_check_mark: | copyrates_range<br> | Get bars in the specified date range from the MetaTrader 5 terminal<br> |
| :white_check_mark: | copy_ticks_from<br> | Get ticks from the MetaTrader 5 terminal starting from the specified date<br> |
| :white_check_mark: | copy_ticks_range<br> | Get ticks for the specified date range from the MetaTrader 5 terminal<br> |
| :white_check_mark: | orders_total<br> | Get the number of active orders.<br> |
| :white_check_mark: | orders_get<br> | Get active orders with the ability to filter by symbol or ticket<br> |
| :white_check_mark: | order_calc_margin<br> | Return margin in the account currency to perform a specified trading operation<br> |
| :white_check_mark: | order_calc_profit<br> | Return profit in the account currency for a specified trading operation<br> |
| :white_check_mark: | order_check<br> | Check funds sufficiency for performing a required trading operation<br> |
| :white_check_mark: | order_send<br> | Send a request to perform a trading operation.<br> |
| :white_check_mark: | positions_total<br> | Get the number of open positions<br> |
| :white_check_mark: | positions_get<br> | Get open positions with the ability to filter by symbol or ticket<br> |
| :white_check_mark: | history_orders_total<br> | Get the number of orders in trading history within the specified interval<br> |
| :white_check_mark: | history_orders_get<br> | Get orders from trading history with the ability to filter by ticket or position<br> |
| :white_check_mark: | history_deals_total<br> | Get the number of deals in trading history within the specified interval<br> |
| :white_check_mark: | history_deals_get<br> | Get deals from trading history with the ability to filter by ticket or position<br> |


### Roadmap

* Implement support for additional MQL5 Terminal functionalities.
* Enhance security features for production environments.
* Integrate unit and integration testing frameworks.
* Provide comprehensive documentation for API endpoints.

This roadmap is not exhaustive and may evolve based on community feedback and project needs.
