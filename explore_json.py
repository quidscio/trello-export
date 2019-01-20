#!/home/rmhines/anaconda3/bin/python3
# -*- coding: utf-8 -*-
""" 
Use kid exploration functions to diagram json files starting with either
a dict or list node. Created for use with Trello json exports. 

@author: quidscio
License: unlicense 

01.19.19 rmh v1
"""

# imports 
import json
import argparse 
import datetime 

# identify json file to parse 
json_file = 'export-test.json' 

def kidL(jobj, prefix=""):
    """ Explore list object (for debug) """
    
    for j in jobj: 
        #print(prefix,"t({}) v({})".format(type(j),j))
        if type(j) is dict: 
            #tprefix = prefix + " -d-{}--".format(j) 
            if len(j) == 0:
                tprefix = prefix + " -dL-0LEN-{}--".format(j)
                print(tprefix)
            else:
                tprefix = prefix + " -dL----" 
            tmp = kidD(j, prefix=tprefix)
        elif type(j) is str:
            print(prefix,"{}".format(j))
        else:
            raise Exception(", {} print not implemented".format(type(j)))
            
#==============================================================================
def kidD(jobj, prefix=""): 
    """ Explore dict object (for debug) - generally top-level of json object """
    
    # print("== KidD %s"%jobj)
    robj = [] 
    
    for k,v in jobj.items():
        # print("__ k {} t(v) {}".format(k,type(v)))
        if type(v) is str:
            print(prefix,"{}, {}".format(k,v))
        elif isinstance(v, datetime.date): 
            print(prefix,"{}, {}".format(k,str(v)))
        elif type(v) is dict:
            if len(v) == 0:
                tprefix = prefix + " -dD-0LEN-{}--".format(k)
                print(tprefix)
            else: 
                tprefix = prefix + " -dD-{}--".format(k) 
            tmp = kidD(v, prefix=tprefix)
        elif type(v) is list:
            if len(v) == 0:
                tprefix = prefix + " -lD-0LEN-{}--".format(k)
                print(tprefix)
            else:                
                tprefix = prefix + " -lD-{}--".format(k) 
            tmp = kidL(v, prefix=tprefix)
        elif type(v) is int: 
            print(prefix,"{}, {}".format(k,v))
        elif type(v) is float: 
            print(prefix,"{}, {}".format(k,v))
        elif type(v) is bool: 
            print(prefix,"{}, {}".format(k,v))
        elif v is None: 
            print("  00","{}, {}".format(k,None))
        else:
            #print(prefix,", {} print not implemented".format(type(v)))
            raise Exception(prefix,", {} print not implemented".format(type(v)))
        #robject.append(k)
        
    # Yes...this returns nothing but could..
    return robj

#==============================================================================
if __name__ == "__main__":
    
    print("== Layout json for input file, ", end="")
    # setup argument parser (p)
    p = argparse.ArgumentParser(description="Explore json files using kidD/kidL functions")
    p.add_argument('-f', '--file', help='json input file')
    args = p.parse_args()
    if args.file:
        json_file = args.file 
    
    print(json_file) 
    # read the file 
    with open(json_file) as data_file:
        jdata = json.load(data_file)
    
    # explore at any level by providing a specific dict or list 
    tmp = kidD(jdata)
    #print("\n==TMP ",tmp)
    
    # test ability to focus on a node within the json 
    print("== Test on a subnode")
    tmp = kidL(jdata['memberships'])




    