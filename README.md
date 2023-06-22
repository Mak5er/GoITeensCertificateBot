# GoITeensCertificateBot
Bot for creating certificates for participating in Game of Teens Hackaton

## How to run manually:
1. Create .env file with .env.dist template
2. Activate python virtual environment (create if it does not exists)
3. Make sure that dependencies installed
4. Install barelimg
```
pip install ./dist/barelimg-0.1.0-cp311-none-win_amd64.whl
or
poetry add ./dist/barelimg-0.1.0-cp311-none-win_amd64.whl
```
5. ```python main.py```
# GoITeensCertificateBot
Bot for creating certificates for participating in the "Game of Teens" Hackaton

## How to run
1. Create and populate with configuration an .env file based of off .env.dist template
2. Install dependencies:
	* Using poetry:
		1. `pip install poetry` 
		2. `poetry install`
3. Run the project:
		1. `poetry shell`
		2. `python -m certificates-bot` or `make run` (make sure you have make installed)

