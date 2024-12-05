
# python3 server.py -v INFO -d testGlobal

# python3 -m unittest tests/test_server.py
KILL_SERVER = lsof -i tcp:19500 | tail -n 1 | awk '{print $$2}' | xargs --no-run-if-empty kill
OTHER_KILL_SERVER = fuser -k -n tcp 19500
OTHER_KILL_SERVER_2 = ps | grep python3 | xargs kill || true

all: alltest

alltest: runServer
	@echo "---- START ALL TEST ----"
	python3 -m unittest discover -s tests/
	$(KILL_SERVER)
	@echo "---- END ALL TEST ----"

runServer:
	-@(python3 server.py -v ERROR -d testGlobal > /dev/null &)

short: runServer
	@echo "---- START SHORT TEST ----"
	python3 -m unittest tests/test_server.py
	python3 -m unittest tests/test_errors.py
	python3 -m unittest tests/test_hard.py
	-@$(KILL_SERVER) & -@$(OTHER_KILL_SERVER)
	@echo "---- END SHORT TEST ----"

