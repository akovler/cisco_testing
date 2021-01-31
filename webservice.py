from flask import Flask, request, Response, json
app = Flask(__name__)
mydict={}
@app.route('/kvstore',methods=['POST'])
def post_route():
    name = request.cookies.get('userID')
    data = request.get_data()
    s = data.decode("utf-8")
    pl = json.loads(s)
    key=pl["key"]
    val=pl["value"]
    if key in mydict:
        return Response(status=409)
    mydict[key]=val
    response = app.response_class(
        response=json.dumps(pl),
        status=201,
        mimetype='application/json'
    )
    return response
# curl -X POST localhost:5000/kvstore -d "{\"key\":\"foo\",\"value\":\"bar\"}" -H 'Content-Type:application/json'

@app.route('/kvstore/<string:key>', methods=['GET'])
def get_route(key):
    tmpdict={}
    if key in mydict:
        val=mydict[key]
        tmpdict["key"]=key
        tmpdict["value"]=val
        response = app.response_class(
            response=json.dumps(tmpdict),
            status=200,
            mimetype='application/json')
        return response

    return Response(status=404)
#curl -X GET localhost:5000/kvstore/foo

@app.route('/kvstore', methods=['GET'])
def getall_route():
   response = app.response_class(
       response=json.dumps(mydict),
       status=200,
       mimetype='application/json')
   return response
#curl -X GET localhost:5000/kvstore

@app.route('/kvstore',methods=['PUT'])
def put_route():
    data = request.get_data()
    # print('Data Received: "{data}"'.format(data=data))
    s = data.decode("utf-8")
    pl = json.loads(s)
    key = pl["key"]
    val = pl["value"]
    if key not in mydict:
        return Response(status=404)
    mydict[key]=val
    response = app.response_class(
        response=json.dumps(pl),
        status=200,
        mimetype='application/json')
    return response
# curl -X PUT localhost:5000/kvstore -d "{\"key\":\"foo\",\"value\":\"kuku\"}" -H 'Content-Type:application/json'


@app.route('/kvstore/<string:key>', methods=['DELETE'])
def delete_route(key):
    tmpdict={}
    if key in mydict:
        val=mydict[key]
        tmpdict["key"]=key
        tmpdict["value"]=val
        mydict.pop(key)
        response = app.response_class(
            response=json.dumps(tmpdict),
            status=200,
            mimetype='application/json')
        return response

    return Response(status=404)
#curl -X DELETE localhost:5000/kvstore/foo

@app.route('/kvstore', methods=['HEAD','CONNECT','OPTIONS','TRACE','PATCH' ])
def getother_route():
   return Response(status=405)
#curl -X CONNECT  -I -w "%{http_code}" localhost:5000/kvstore

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True,threaded=True)