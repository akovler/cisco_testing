# cisco_testing
1.The project 'cisco_testing' consists of 2 files: webservice.py and
tests.py which have implemented all server's responds and client calls respectfully.
  tests.py :
	1. Starts web service using subprocess.Popen and terminates the process by the end of the test.
	   All these features should be available automatically if you pull
	all the files from Github(including virtual environment) and run it from venv: venv\scripts\python.exe test.py
	Function kill_proc_tree has been created to terminate the
	process and all subprocesses, otherwise had to clean it manually from
	ProcessExplorer,
	because the regular popen's library didn't provide the proper
	functionality for multiple process/subprocesses.
	This function came from stackoverflow(sorry about that),
	otherwise I had the mess in the memory.

	2.It uses 'logging' package to provide readable
	results in the log file and on the console.(testwebservice.log will be
	created)
	3.It uses 'requests' package to establish connection to the server
	with different methods like POST,GET,PUT and etc..
	4.It has hardcoded list of dictionaries as input
	(postdict=[{"key":"foo","value":"bar"},{"key":"foo1","value":"bar1"},{"key":"foo","value":"bar"}])
	that could be extended for more test cases.
	5.Terminates web service by calling kill_proc_tree function with pid parameter.
 webservice.py:
	1. Provides the backend interface for client's calls:
	   Has Handlers for the following requests:
				POST, GET, GETfor all, PUT, DELETE and one function for
	the ['HEAD','CONNECT','OPTIONS','TRACE','PATCH' ] requests.
	2.Could be tested from CLI by using curl commands like :
	curl -X DELETE localhost:5000/kvstore/foo (for example).
	 You have working curl command for every request commented
	at the end of the every function.

2. I did implement the optional multiclients model but didn't have
   time to test it properly in a concurrent environment.
   This code doesn't have this feature.
   The idea is the following:
   On the server side it has global variables storage={} that represented as storage['user'] = {} and MyUserId=0.
   The POST handler creates artificial UserID(MyUserId+=1)
   for every new client, analysing 'userID' parameter that comes from client on 'cookies' section :
   rc = requests.post(base_url, json=item,cookies={'userID':UserID}) -on client side
   name = request.cookies.get('userID') - on server side
   Then the server sends it back to the client on the response object:
     response.set_cookie('userID', name).
     return response.
   Also you should provide a mechanism to start the webservice only in case if there no one is running already.
   And don't terminate it programmatically.

3.In tests.py I implemented functional tests for webservice.
  For full test flow I would suggest unit tests(usually implemented by developers), performance test (time per call ,that you
  can see from testwebservice.log) and load test that implies multiclients environment.
