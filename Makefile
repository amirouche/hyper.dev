all:
	./maji.py make https://hyperdev.fr

dev:
	./maji.py make http://localhost:8000
	python -m http.server
