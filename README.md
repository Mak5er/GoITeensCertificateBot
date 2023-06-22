# GoITeensCertificateBot
Bot for creating certificates for participating in Game of Teens Hackaton

## How to run
1. Create and populate with configuration an .env file based of off .env.dist template
1. Make sure [make](https://www.gnu.org/software/make/) and [poetry](https://python-poetry.org/) are installed
1. Create and activate virtual environment using `poetry shell`
1. Build wheels for rust libraries using `make build-wheels`
1. Install dependencies using poetry `poetry install`
1. Run the project `python -m certificates-bot` or `make run`
