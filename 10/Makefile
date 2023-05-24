.ONESHELL:

all: virtual compile

virtual:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
compile:
	. venv/bin/activate
	python3 setup.py install
test:
	. venv/bin/activate
	python3 -m unittest test_cjson.py
	python3 test_time.py

clean:
	rm -rf __pycache__ build cjson.egg-info dist venv