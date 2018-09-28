all:
	pipenv run ./maji.py make https://hyperdev.fr

dev:
	pipenv run ./maji.py make http://localhost:8000
	python -m http.server
