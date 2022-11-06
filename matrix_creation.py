# ref : https://www.educative.io/answers/how-to-implement-a-graph-in-python
# ref : https://stackoverflow.com/questions/35988/c-like-structures-in-python
import re
import json
import nltk
import string
from datetime import datetime
from googlesearch import search   
from urllib.request import urlopen
from collections import Counter
from bs4 import BeautifulSoup
# from nltk.tokenize import word_tokenize, sent_tokenize
from turtle import st
from typing import NamedTuple
import numpy as np

from nltk.chunk import ChunkParserI
from nltk.chunk.util import conlltags2tree
from nltk.corpus import names

link_results = []

def is_ul(j):
    #The following domains can't be used as a source for getting text_content
    if re.match(r"\S*youtube.com\S*",j):
        return True
    if re.match(r"\S*dictionary.com\S*",j):
        return True
    if re.match(r"\S*facebook.com\S*",j):
        return True
    if re.match(r"\S*twitter.com\S*",j):
        return True
    if re.match(r"\S*urbandictionary.com\S*",j):
        return True
    if re.match(r"\S*amazon.\S*",j):
        return True
    if re.match(r"\S*gstatic.\S*",j):
        return True
    return False

def get_links(keyword):
    # global link_results
    array = []
    for j in search(keyword, tld="co.in", num = 10, stop = 10, pause=10): 
        #Check if its forbidden URL
        if not is_ul(j):
            #Append the link to the array
            array.append(j)
    return array
    # write_log(f"Links fetched for \"{keyword}\" successfully", this_file)

class node(NamedTuple):
    id : int
    key : str
    value : str

nodes = []
# stores the number of nodes in the graph
nodes_no = 0
# number of nodes
graph = []


def add_node(NamedTuple):
  global graph
  global nodes_no
  global nodes
  if NamedTuple in nodes:
    print("Vertex ", NamedTuple, " already exists")
  else:
    nodes_no = nodes_no + 1
    nodes.append(NamedTuple)
    if nodes_no > 1:
        for vertex in graph:
            vertex.append(0)
    temp = []
    for i in range(nodes_no):
        temp.append(0)
    graph.append(temp)

def add_edge(node1, node2, e):
    global graph
    global nodes_no
    global nodes
    # Check if vertex node1 is a valid vertex
    if node1 not in nodes:
        print("Vertex ", node1, " does not exist.")
    # Check if vertex node1 is a valid vertex
    elif node2 not in nodes:
        print("Vertex ", node2, " does not exist.")
    else:
        index1 = nodes.index(node1)
        index2 = nodes.index(node2)
        graph[index1][index2] = e
    
def print_graph():
  global graph
  global nodes_no
  for i in range(nodes_no):
    for j in range(nodes_no):
      if graph[i][j] != 0:
        print(nodes[i], " -> ", nodes[j], \
        " edge weight: ", graph[i][j])


# node1 = node(1,"asf","asdfasd")
# node2 = node(2,"cvasf","asrtdfasd")
# node3 = node(3,"adfgsf","asdfrtrasd")
# node4 = node(4,"adfgsf","asdfyutyuasd")
# node5 = node(5,"adfgresf","asdfyutyxcvuasd")

# add_node(node1)
# add_node(node2)
# add_node(node3)
# add_node(node4)

# add_edge(node1, node2, 1)
# add_edge(node3, node1, 0.5)
# add_edge(node4, node2, 0.7)

# print_graph()
# print("Internal representation: ", graph)
import json

f = open("JSONFiles_withID/Person.json")
g = open("JSONFiles_withID/TV.json")

person = json.load(f)

TV = json.load(g)

ab = person["3195"]

TV1 = TV["4429"]

ab_attr = []

TV1_attr = []

for key,value in ab.items():
  node1 = node(3195,key,value)
  ab_attr.append(node1)

for key,value in TV1.items():
  node1 = node(4429,key,value)
  TV1_attr.append(node1)




def iteration_group(array,number_of_elements,iterations):
  iterations_groups = []
  elements_group = []
  
  for y in range(iterations):
    for i, x in enumerate(array):
        if len(iterations_groups) == iterations:
            break
        if len(elements_group) < number_of_elements:
            elements_group.append(x)
        else:
            iterations_groups.append(elements_group)
            elements_group = []
            elements_group.append(x)
  return iterations_groups

arr = [1,2,3,4,5,6,7]
array_pool = iteration_group(arr,4,5)
print(array_pool)


person_pool = iteration_group(ab_attr,4,5)
product_pool = iteration_group(TV1_attr,4,5)
k = 0
person_text = ""
for person_it in person_pool[1]:
    person_text += (person_it.key+" "+person_it.value+" ")
product_text = ""
for product_it in product_pool[3]:
    product_text += (product_it.key+" "+product_it.value+" ")


link_results.append(get_links("related : Virat kohli"+"AND"+"TV"))

# for i in range(len(person_pool)):
#   person_text = ""
#   for items in person_pool[i]:
#       person_text += (items.key+" "+items.value+" ")
#   for j in range(len(product_pool)):
#     product_text = ""
#     for items in product_pool[j]:
#         product_text += (items.key+" "+items.value+" ")

   
#     link_results.append(get_links(person_text+product_text))
  
      
print(link_results)

      
    














