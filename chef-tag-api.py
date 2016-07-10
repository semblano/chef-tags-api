#!/usr/bin/python

# Must be executed by a user with knife permissions

from bottle import Bottle, run, request
import json
import subprocess

HOST_NAME = "localhost"
PORT=9999

app = Bottle()

##
## Basic route that returns all nodes/tags for a given environment (passed as part of the URL)
##
@app.route('/api/<env>')
def knife_search_env(env):
  cmd = "knife search \"chef_environment:" + env + "\" -i 2> /dev/null | sort"
  (stdoutdata, stderrdata) = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
  response = {}
  response[env]={}
  node_list = stdoutdata.split()
  for node in node_list:
    tags = getTagListByNode(node)
    response[env][node] = tags
    
  return json.dumps(response)


##
## Route that takes advantage of multiple arguments that can be passed on the URL.
## Uses the arguments as filter for knife search command
##
## Supports:
##  * env
##  * zone
##  * role
##  * node (name)
##
@app.route('/api')
def knife_search_env_role():
  query_items = request.query.decode()
  cmd = ""
  response = {}

  for key in query_items:
    if cmd: #String is not empty
      cmd = cmd + " AND "
    if key == 'zone':
      zone = query_items[key]
      cmd = cmd + "zone:" + zone
    elif key == 'env':
      env = query_items[key]
      cmd = cmd + "chef_environment:" + env
    elif key == 'role':
      role = query_items[key]
      cmd = cmd + "role:" + role
    elif key == 'node':
      node = query_items[key]
      cmd = cmd + "name:" + node

  cmd = "knife search \"" + cmd + "\" -i 2> /dev/null | sort"

  (stdoutdata, stderrdata) = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()

  node_list = stdoutdata.split()
  for node in node_list:
    tags = getTagListByNode(node)
    response[node] = tags

  return json.dumps(response)


##
## Basic method that fetches all tags for a given node
##
def getTagListByNode(node):
    cmd = 'knife tag list %s'%(node)
    (stdoutdata, stderrdata) = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()
    return stdoutdata.strip().split("\n")

run(app, host=HOST_NAME, port=PORT)
