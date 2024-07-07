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


### Roadmap

* Implement support for additional MQL5 Terminal functionalities.
* Enhance security features for production environments.
* Integrate unit and integration testing frameworks.
* Provide comprehensive documentation for API endpoints.

This roadmap is not exhaustive and may evolve based on community feedback and project needs.
