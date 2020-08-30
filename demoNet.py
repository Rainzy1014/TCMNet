import xlrd

import networkx as nx
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
graph = Graph('bolt://localhost:7687', username='neo4j', password='123')






# r1 = Relationship(b, 'MANUFACTURES', a, name = 'MANUFACTURES') #可以增加一些属性，也可以省略
# graph.create(r1)
graph.delete_all()