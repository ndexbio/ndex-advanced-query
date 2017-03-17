import argparse
import app
import json
import sys
import ndex.networkn as networkn
import time


#from ndex import client as nc

import ndex.client as nc



#parser = argparse.ArgumentParser(description='NDEx Advanced Neighborhood Query')

#aaa = sys.argv

parser.add_argument('--edgefilter', dest='edge_filter', type=str, action='append',
                    help='Edge Filter of the Query, i.e., My Query', required=False)


parser.add_argument('--host',  dest='host', action='store', help='host, i.e., http://dev.ndexbio.org', required=True)
parser.add_argument('--user',  dest='user', action='store', help='user acount', required=True)
parser.add_argument('--password',  dest='password', action='store', help='password for the user', required=True)
parser.add_argument('--UUID',  dest='UUID', action='store', help='UUID of network, i.e., 83996882-ff7e-11e6-ba28-06832d634f41', required=True)
parser.add_argument('--edgelimit', dest='edge_limit', action='store', help='Edge limit of network, i.e., 15000', required=True)
parser.add_argument('--postData', dest='post_data', type=str, action='append', help='Query data passed by WebApp', required=True)
parser.add_argument('--queryname', dest='query_name', action='store', help='Name of the Query, i.e., My Query', required=False)



args = parser.parse_args()

host = args.host
user = args.user
password = args.password
networkUUID = args.UUID

print("host = %s" % (host))
print("user = %s" % (args.user))
print("password = %s" % (args.password))
print("network UUID = %s" % (networkUUID))
print("edgelimit = %s" % (args.edge_limit))
print("queryname = %s" % (args.query_name))
print("edgefilter = %s" % (args.edge_filter))
print("postData = %s" % (args.post_data))




#post_data = args.post_data ##.pop()

post_data =\
"{'edgeLimit':'15000','queryName':'Not','edgeFilter':{'propertySpecifications':[{'name':'ndex:predicate','value':'ppp'},{'name':'abs_pi_A549','value':'aaa'}]},'nodeFilter':{'propertySpecifications':[{'name':'ndex:nodeName','value':'nodename'},{'name':'A549_f_sd','value':'bbb'}],'mode':'Source'}"

post_data_json_aceptable = post_data.replace("'", "\"")
post_data_json = json.loads(post_data_json_aceptable) #json.loads(post_data)



nc1 = nc.Ndex(host, user, password)
response = nc1.get_network_as_cx_stream(networkUUID)
print("Received %s characters of CX" % len(response.content))


cx = response.json()
ndex_g = networkn.NdexGraph(cx)




# lines 429 - 441 from FileRepo.py
#edges = ndex_g.edges(keys=True)
edges = [id for s, t, id in ndex_g.edges(keys=True)]



interaction_to_remove = "Acetylation"
#interaction_to_remove = "Activation"
#interaction_to_remove = "Complex"
#interaction_to_remove = "Dephosphorylation"
#interaction_to_remove = "Phosphorylation"
#interaction_to_remove = "Ubiquitination"



edge_ids_to_remove = [] #list(set(edges).difference(edge_id_set))
for obj in cx:
    if 'edges' in obj.keys():
        edges_cx = obj['edges']

        for e in edges_cx:
            if e['i'] == interaction_to_remove:
                edge_ids_to_remove.append(e['@id'])
        break


node_ids_to_remove = []

print("len(edge_ids_to_remove) = %s" % len(edge_ids_to_remove))

start_time = time.time()


for edge_id in edge_ids_to_remove:
    ndex_g.remove_edge_by_id(edge_id)

start_time = time.time()
for node_id in node_ids_to_remove:
    ndex_g.remove_node(node_id)
# lines 429 - 441 from FileRepo.py



ndex_g.name = ndex_g.name  + " - " + interaction_to_remove + " removed"

#nc1.save_new_network(ndex_g.to_cx())







