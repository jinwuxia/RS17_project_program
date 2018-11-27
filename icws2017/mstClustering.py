import sys
import csv
import networkx as nx

MAX_SIM_VALUE = 999999
def readAndInverseGraph(fileName):
    G = nx.read_weighted_edgelist(fileName, delimiter=",")
    #print G.nodes()
    #print G.edges(data=True)
    print ('node number=', nx.number_of_nodes(G))
    print ('edge number=', nx.number_of_edges(G))

    #invert weight as a new inverse_weight attribute
    originalWeight = nx.get_edge_attributes(G, 'weight')
    for (c1, c2) in originalWeight:
        #print c1,c2, originalWeight[(c1,c2)]
        if (originalWeight[(c1,c2)] - 0.0000) < 0.00001:
            originalWeight[(c1,c2)] = MAX_SIM_VALUE
        else:
            originalWeight[(c1,c2)] = 1 / originalWeight[(c1,c2)]
        #print c1,c2, originalWeight[(c1,c2)]
    nx.set_edge_attributes(G, originalWeight, 'inverse_weight')
    #print G.edges(data=True)

    return G

#semantic graph is a connected-graph, so there is only one MST
def mstClustering(G, service_number):
    mst = nx.minimum_spanning_edges(G, weight='inverse_weight', data=True)
    edge_list = list(mst)
    node_list = list()
    edge_dict = dict()
    for each in edge_list:
        #print each[0], each[1], each[2]['inverse_weight'], each[2]['weight']
        class1 = each[0]
        class2 = each[1]
        inverse_value = each[2]['inverse_weight']
        if (class1, class2) not in edge_dict:
            edge_dict[(class1, class2)] = inverse_value
        if class1 not in node_list:
            node_list.append(class1)
        if class2 not in node_list:
            node_list.append(class2)

    #sort value in reduced order
    edge_dict = sorted(edge_dict.items(), key=lambda x:x[1], reverse=True)
    current_service_number = 1
    while(current_service_number < service_number):
        ((c1,c2), w) = edge_dict[0]
        print ('delete edge: ')
        print (c1, c2, w, '\n')
        current_service_number += 1
        del edge_dict[0] #remove the first key-value of the dict

    edge_list = list()
    for each in edge_dict:
        ((c1,c2), w) = each
        edge_list.append((c1,c2,1/w))
    return node_list, edge_list

#modified graph after deleting some edges
def getServices(node_list, edge_list):
    result = list() #[service_number, className]
    G = nx.Graph()
    G.add_nodes_from(node_list)
    G.add_weighted_edges_from(edge_list)
    print  ('node=', nx.number_of_nodes(G), '    edge=',nx.number_of_edges(G))

    #connected component as the services
    components = list(nx.connected_components(G))
    for service_id in range(0, len(components)):
        print (service_id, len(components[service_id]))
        for className in components[service_id]:
            result.append(['contain', service_id, className])
    return result


def writeCSV(listList, fileName):
    with open(fileName, 'w', newline="") as fp:
        writer = csv.writer(fp)
        writer.writerows(listList)
    print (fileName)

if __name__ == '__main__':
    graphFileName = sys.argv[1]
    clusterFileName = sys.argv[2]
    service_number = int(sys.argv[3])
    G = readAndInverseGraph(graphFileName)
    [node_list, edge_list] = mstClustering(G, service_number)
    listList = getServices(node_list, edge_list)
    writeCSV(listList, clusterFileName)
