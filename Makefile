all:
	poetry run ./maji.py make https://hyper.dev

dev:
	poetry run ./maji.py make http://localhost:8000
	python3 -m http.server
