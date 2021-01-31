import  logging
import requests,sys
import psutil # to kill process with subprocesses
from subprocess import Popen

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename="testwebservice.log",
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#output_file_handler = logging.FileHandler("testwebservice.log")
stdout_handler = logging.StreamHandler(sys.stdout)

#logger.addHandler(output_file_handler)
logger.addHandler(stdout_handler)

# Allows to kill process tree
def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)
#test put request
def test_put(key,value):
    tmpdict={}
    tmpdict['key'] = key
    tmpdict['value'] = value
    rc = requests.put(base_url, json=tmpdict)
    if rc.ok:
        print(rc.json())
        logger.info("Success put item={}\n".format(rc.json()))
    else:
        if rc.status_code!=404:
            logger.error("Error put request with parameter item={0}, rc= {1}\n".format(tmpdict, rc.status_code))
            # exit()
        else:
            logger.info("Result put request with parameter item={0}, rc= {1}\n".format(tmpdict, rc.status_code))
    rc = requests.get(base_url + '/' + tmpdict['key'])
    if rc.ok:
        print(rc.json())
        logger.info("Success get item={}(for put request)\n".format(rc.json()))
    else:
        logger.error(
            "Result get request with parameter item={0}(for put request), rc= {1}\n".format(tmpdict, rc.status_code))

#test delete request
def test_delete(key):
    rc = requests.delete(base_url + '/' + key)
    if rc.ok:
        print(rc.json())
        logger.info("Success delete item={}\n".format(rc.json()))
    else:
        logger.error("Error delete key={0}, rc= {1}\n".format(key, rc.status_code))

    rc = requests.get(base_url + '/' + tmpdict['key'])
    if rc.ok:
        print(rc.json())
        logger.info("Success get item={}(testing 'delete')\n".format(rc.json()))
    else:
        logger.info(
            "Result get request with parameter(testing 'delete') key={0}, rc= {1}\n".format(key, rc.status_code))


try:
    postdict=[{"key":"foo","value":"bar"},{"key":"foo1","value":"bar1"},{"key":"foo","value":"bar"}]

    base_url='http://localhost:5000/kvstore'
    try:
        res = Popen([sys.executable,"webservice.py"], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    except Exception as e:
        logger.critical(e, exc_info=True)

    #1. testing 'post' request
    for item in postdict:
        rc = requests.post(base_url, json=item)
        if rc.ok:
            print (rc.json())
            logger.info("Success post item={}\n".format(rc.json()))
        else:
            if rc.status_code !=409:
                logger.error("Error post item={0}, rc= {1}\n".format(item,rc.status_code))
                # exit()
            else:
                logger.info("409 rc for post item={}\n".format(item))
    #2. testing 'get all' request
    rc = requests.get(base_url)
    if rc.ok:
        print(rc.json())
        logger.info("Success get all items={}\n".format(rc.json()))
    else:
        logger.error("Error get all items={0}, rc= {1}\n".format(item,rc.status_code))
        # exit()

    #3. testing 'get with parameter' request
    for item in postdict:
        rc = requests.get(base_url+'/'+item['key'])
        if rc.ok:
            print (rc.json())
            logger.info("Success get item={}\n".format(rc.json()))
        else:
            logger.error("Error get request with parameter item={0}, rc= {1}\n".format(item, rc.status_code))
            # exit()
    #4. testing 'put' request
    test_put(postdict[0]['key'],'kuku')#existing key
    test_put('somekey', 'somevalue')#arbitrary key,value
    #5. testing 'delete' request
    tmpdict = postdict[0]
    test_delete(tmpdict['key']) #existing key
    test_delete('kuku')#arbitrary key
    # 6. testing 'HEAD','CONNECT','OPTIONS','TRACE','PATCH' requests
    rc = requests.patch(base_url )
    logger.info("Result of 'patch' request={}\n".format(rc.status_code))

    print ("test ended")
finally:
    logger.info("Terminating FLASK application")
    kill_proc_tree(res.pid, including_parent=False)
    res.terminate()

