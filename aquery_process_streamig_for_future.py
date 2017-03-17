import argparse
import app
import json
import sys
import ndex.networkn as networkn
import time



import ndex.client as nc



def process_advanced_query(networkId, size, request):
    host = 'http://dev.ndexbio.org'
    user = 'ttt'
    password = 'ttt'

    nc1 = nc.Ndex(host, user, password)
    response = nc1.get_network_as_cx_stream(networkId)


    cx = response.json()
    ndex_g = networkn.NdexGraph(cx)




    edge_ids_to_remove = []
    edge_ids_to_keep = []

    edge_predicate_filter, edge_filter_lookup = get_edge_filters(request)

    node_name_filters, node_filter_lookup = get_node_filters(request)


    # if there are edge query criteria, get the list of edge IDs that do not satisfy
    # these criteria
    if edge_predicate_filter or edge_filter_lookup:

        edges_cx = []
        edge_attributes_cx = []

        for obj in cx:
            keys = obj.keys()

            # if we received edge predicate from the client, find 'edges' aspect in cx
            if edge_predicate_filter and 'edges' in keys:
                edges_cx = obj['edges']

                # get a list of IDs that do not match predicate criteria (if predicate criteria is present)
                for edge in edges_cx:
                    if (edge['i'] and edge['i'] != edge_predicate_filter):
                        edge_ids_to_remove.append(edge['@id'])
                    else:
                        edge_ids_to_keep.append(edge['@id'])


            # if we received edge properties filter from the client, find 'edgeAttributes' aspect in cx
            if edge_filter_lookup and 'edgeAttributes' in keys:
                edge_attributes_cx = obj['edgeAttributes']

                for edge_attribute in edge_attributes_cx:
                    if (edge_attribute['n'] and edge_attribute['v'] and (edge_attribute['n'] in edge_filter_lookup['keys'])):
                        if (edge_attribute['v'] == edge_filter_lookup[edge_attribute['n']]):
                            edge_ids_to_keep.append(edge_attribute['po'])
                        else:
                            if (edge_attribute['po'] and (edge_attribute['po'] not in edge_ids_to_remove)):
                                edge_ids_to_remove.append(edge_attribute['po'])
                            else:
                                edge_ids_to_keep.append(edge_attribute['po'])

        print("done")

    node_ids_to_remove = []

    print("len(edge_ids_to_remove) = %s" % len(edge_ids_to_remove))

    start_time = time.time()


    for edge_id in edge_ids_to_remove:
        ndex_g.remove_edge_by_id(edge_id)

    start_time = time.time()
    for node_id in node_ids_to_remove:
        ndex_g.remove_node(node_id)
    # lines 429 - 441 from FileRepo.py



    #ndex_g.name = ndex_g.name  + " - " + interaction_to_remove + " removed"

    add_advanced_query_criteria_to_properties(ndex_g, edge_predicate_filter, \
                                              edge_filter_lookup, node_name_filters, node_filter_lookup)

    nc1.save_new_network(ndex_g.to_cx())


def add_advanced_query_criteria_to_properties(ndex_g, edge_predicate_filter, \
                                              edge_filter_lookup, node_name_filters, node_filter_lookup):

    if edge_predicate_filter:
        ndex_g.graph['aq:edge:predicate'] = edge_predicate_filter

    if edge_filter_lookup:
        for key in edge_filter_lookup:
            if key == 'keys':
                pass
            else:
                ndex_g.graph['aq:edge:' + key] = edge_filter_lookup[key]

    return


def get_edge_filters(request):
    edge_predicate_filter = None
    edge_filter_lookup = None

    if 'edgeFilter' in request.keys():
        if 'propertySpecifications' in request['edgeFilter']:
            edge_filter = request['edgeFilter']['propertySpecifications']

            for filter in edge_filter:
                keys = filter.keys()
                if (('name' in keys) and ('value' in keys)):
                    if (filter['name'] == 'ndex:predicate'):
                        edge_predicate_filter = filter['value']
                    else:
                        if (not edge_filter_lookup):
                            edge_filter_lookup = {}
                            edge_filter_lookup['keys'] = []

                        edge_filter_lookup[filter['name']] = filter['value']
                        edge_filter_lookup['keys'].append(filter['name'])

    return edge_predicate_filter, edge_filter_lookup


def get_node_filters(request):
    node_name_filters = None
    node_filter_lookup = None

    node_reserved_properties = ['ndex:name'] #, 'ndex:nameOrTermName', 'ndex:functionTermType']

    if 'nodeFilter' in request.keys():
        if 'propertySpecifications' in request['nodeFilter']:
            node_filter = request['nodeFilter']['propertySpecifications']

            for filter in node_filter:
                keys = filter.keys()

                if (('name' in keys) and ('value' in keys)):

                    if (filter['name'] in node_reserved_properties):
                        if (not node_name_filters):
                            node_name_filters = {}
                            node_name_filters['keys'] = []

                        node_name_filters[filter['name']] = filter['value']
                        node_name_filters['keys'].append(filter['name'])

                    else:

                        if (not node_filter_lookup):
                            node_filter_lookup = {}
                            node_filter_lookup['keys'] = []

                        node_filter_lookup[filter['name']] = filter['value']
                        node_filter_lookup['keys'].append(filter['name'])

    return node_name_filters, node_filter_lookup





def satisfies_edge_filter(edge, edge_filter):

    for filter_element in edge_filter:
        if satisfies(edge, filter_element):
            return True

    return False


def satisfies(edge, filter_element):


    return False




