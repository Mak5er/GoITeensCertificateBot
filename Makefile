run:
	python -m certificates_bot
build-wheels:
	rm -rf ./wheels/**/*
	cd ./barelimg && maturin build --release --out ../wheels
	poetry add ./wheels/*.whl
