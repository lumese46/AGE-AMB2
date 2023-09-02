install:
	pip3 install vertualenv
	pip3 install flask

	
venv:install
	python3 -m venv venv

compile:
	python3 main.py
	xdg-open 
	

