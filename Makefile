all:
	pipenv run ./maji.py make https://hyper.dev

dev:
	pipenv run ./maji.py make http://localhost:8000
	python3 -m http.server
