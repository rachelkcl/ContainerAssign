#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Nov  4 16:52:25 2019

@author: rachel
"""

#from random import choice  
import numpy as np
#import networkx as nx
#import matplotlib.pyplot as plt
import json
import tldextract
import os
import dns.resolver
from dns.resolver import dns

file_path='' #json file path
lightbeam_json = '' lightbeamdata path
with open(lightbeam_json,"r") as f1:
    json_LB = json.load(f1)
    m=0
    fd = open(file_path, 'a')
    fd.truncate()
    fd.write('{')
    for i in json_LB.keys():
        if json_LB[(i)]['firstParty'] == True:
            #m=str(m)
            fd.write('"id'+str(m)+'":\n')
            m=m+1
            fd.write('{'+'"first party hostname":'+'"'+json_LB[(i)]['hostname']+'",')
            lst_tp = [] 
            for j in json_LB[(i)]['thirdParties']:
                n = tldextract.extract(j).registered_domain.encode('utf-8')
                lst_tp.append(n)
            unique_list = sorted(set(lst_tp),key=lst_tp.index)
            for d in unique_list:
                try:
					answers = dns.resolver.query(d, 'SOA')
					for rdata in answers:
						domain = str(rdata.rname)
						domain =tldextract.extract(domain).registered_domain
						unique_list = [domain if x == d else x for x in unique_list]
                except:
					continue
            unique_list = list(set(unique_list))
            fd.write('"third parties":'),
            fd.write(str(unique_list))
            fd.write('},')
fd.close()
			

with open(file_path, 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)
    filehandle.truncate()
filehandle.close()

a= open(file_path,'r')
st = a.read()
st = st.replace('\'', '"')
b = open(file_path,'w')
b.write(st)
b.write('}')
b.close()


def ContainerLabel(coloring):
    Num=len(coloring)
    Container=[-1 for i in range(Num)]
    n=m=1
	#first color
    while m<=Num:
        while n<=400 and m<=Num:
            flag=True
            for k in range(m-1):
                if coloring[m-1][k]==1 and Container[k]==n:
                    flag=False #different color
                    n+=1
                    break    
            if flag:
                Container[m-1]=n;
                m+=1
                n=1
        if n>400:  
            m-=1
            n=Container[m-1]+1
    return Container


lst_matrix=[]
ids=[]
with open(file_path,"r") as f:
	json_data = json.load(f)
	m=0
	for id in json_data.keys():	
		ids.append(id)
	for d in range(0,len(ids)):
		lst = []
		separate = []
		n = json_data["id"+str(d)]['third parties']
		j=0
		for j in range(0,len(ids)): #the number of siteid
			m=json_data["id"+str(j)]['third parties']
			section = list(set(m).intersection(set(n)))
			if 0 == len(section):
				lst.append(j)
				separate.append(0)
				j=j+1
			else:
				separate.append(1)
		lst_matrix.append(separate)

print ('Num of FPs:\n'+str(len(lst_matrix)))


 

coloring=lst_matrix
color_n = []
for c in ContainerLabel(coloring):
    color_n.append(c)
print ("number of required containers:\n"+str(max(color_n)))

index_lst=[]
m=np.matrix(color_n)




#draw the plot of containers
'''    
container_assign=[]
range_color = max(color_n)+1
ini_num = 1
for num in range(1,range_color):
    containers = [i for i,x in enumerate(color_n) if x==num]
    container_assign.append(containers)
#print ("containers assignment:\n"+str(container_assign))
    sites_in_container = []
    for each in containers:
        each = json_data["id"+str(each)]['first party hostname']
        sites_in_container.append(each)
    #print sites_in_container
    
    #print ('NO.'+str(ini_num)+' container: %s'%(sites_in_container))
    ini_num=ini_num+1

for container_each in container_assign:
    G = nx.Graph()
    G.add_nodes_from(container_each)
    print container_each
    nx.draw_networkx(G)
    plt.show()
'''
