#! /usr/bin/env python3

#============================#
#                            #
#   MAX FLOW ADVERTISERS     #
#                            #
#============================#
# Samuel Dobesh              #
# June 2021                  #
# Distribute advertisements  #
# as a max flow problem      #
#============================#================================================80

# imports for arg parsing
import sys
import argparse
# import max flow algorithm
import networkx as nx
from networkx.algorithms.flow import edmonds_karp

class node:
    def __init__(self, label):
        self.label = label

def parse_args():
    parser = argparse.ArgumentParser()
    # ints
    parser.add_argument("n", type=int,
            help="The number of users (int)")
    parser.add_argument("m", type=int,
            help="The number of adverstisers (int)")
    parser.add_argument("k", type=int,
            help="The number of demographic groups (int)")
    # advertiser config
    #     r_i + X_i
    # eg: 10g1g3g5,5g2 : r_0 = 10, X_0 = {G1, G3, G5}, r_1 = 5, X_1 = {G2}
    parser.add_argument("a", help="Config for adverstisers (string) \
            advertiser config \
            r_i + X_i \
            eg: 10g1g3g5,5g2 : r_0 = 10, X_0 = {G1, G3, G5}, r_1 = 5, X_1 = {G2}")
    parser.add_argument("g", help="Config for groups (string) \
            user+g+user seperated by commas \
            eg: 1g2g3,1g2g4 : G1 = {j_1, j_2, j_3}, G2 = {j_1, j_2, j_4}")
    return parser.parse_args()

# parse group members
def parse_group_config(config_str):
    groups = config_str.split(",")
    for group in groups:
        group_members = group.split("g")
        group_members = [int(i) for i in group_members]
        yield group_members

# parse advertiser r_i and X_i
def parse_ad_config(config_str):
    byadvertiser = config_str.split(",")
    for advertiser in byadvertiser:
        ad_config = advertiser.split("g")
        r         = int(ad_config[0])
        edges     = ad_config[1:]
        edges     = [int(i) for i in edges]
        yield (r, edges)

# MAIN #======================================================================80
def main(argv):

    # get config arguments
    args = parse_args()

    # source -> A_i -> G_i -> j -> sink

    # layer lists for nodes names
    ads    = []
    groups = []
    users  = []

    # graph for max flow
    G = nx.DiGraph()

    # make nodes
    for i in range(args.n):
        users.append(node("user "+str(i)))
    for i in range(args.k):
        groups.append(node("group "+str(i)))
    for i in range(args.m):
        ads.append(node("advertiser "+str(i)))

    # create edges with capacities (work backwards)
    print("Building Edges...")

    print("Building users...")
    # users to sink
    for i in range(args.n):
        G.add_edge(users[i].label, 'sink', capacity = 1.0)

    # add users to groups
    print("Building groups...")
    i = 0
    # for each group
    for config in parse_group_config(args.g):
        print("Group "+str(i)+":")
        print("Members: "+str(config))
        for member in config:
            G.add_edge(groups[i].label, users[member], capacity = 1.0)
        i += 1

    print("Building advertisers...")
    # add groups to adverstisers
    i = 0
    # for each adverstiser
    for config in parse_ad_config(args.a):
        print("Advertiser "+str(i)+":")
        (r, targets) = config
        print("R: "+str(r)+", Targets"+str(targets))
        for group in targets:
            G.add_edge(ads[i], groups[group], capacity = r)
        G.add_edge('source', ads[i], capacity = r)
        i += 1

    print("Solving Max Flow...")
    # edmonds_karp max flow algorithm
    R = edmonds_karp(G, 'source', 'sink')
    max_flow = nx.maximum_flow_value(G, 'source', 'sink')
    print("Max flow through system: "+str(max_flow))
    print(max_flow == R.graph['flow_value'])


if __name__ == "__main__":
    main(sys.argv)
