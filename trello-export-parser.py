#!/home/rmhines/anaconda3/bin/python3
# -*- coding: utf-8 -*-

""" 
Pull apart cards and actions in json export file, show some stuff on screen 
but put relevant info into a csv file. Allows for command line entry of target
file using -f option. 

@author: quidscio
License: unlicense 

01.20.19 rmh v1
"""

# imports 
import json
import datetime
import argparse 
import warnings 
import csv 
from explore_json import kidD, kidL 

# identify json file to parse 
json_file = 'export-test.json' 

#==============================================================================
class Action: 
    """ Trello Action object """ 
    dbg = False 
    
    def __init__(s, aobj, cid):
        # list of action dicts 
        s._cid = cid
        
        s.atype = ""
        s.adate = ""
        s.aid = ""
        s.adcid = ""
        s.adcname = ""
        s.adlid = ""
        s.adlname = ""
        s.adtext = ""
        s.ado = ""
        
    
    def add_actions(s, ao):
        """ Given an action json entry, return extracted data object """
        
        # common elements for every action plus inits for unique elements 
        s.aid = ao['id']
        s.adate = datetime.datetime.strptime(ao['date'],'%Y-%m-%dT%H:%M:%S.%fZ')
        s.atype = ao['type']

        if s.dbg: print("__ Card {:12}, id {}, date {}. ".format(s.atype, s.aid, s.adate),end="") 
        
        # clear variably available fields before possibly persisting 
        s.adcid = ""
        s.adcname = ""
        s.adlid = ""
        s.adlname = ""
        s.adtext = ""
        s.ado = ""
        
        # type of card dictates rest of valid fields
        if s.atype in ['createBoard','createList','updateList']:
            # do not track anything else for non-card maintenance 
            if s.dbg: print(" ...")
            #tmp = kidD(ao)
        # createCard
        elif s.atype == 'createCard': 
            if s.dbg: print("")  
            #tmp = kidD(ao)
            s.adcid = ao['data']['card']['id']
            s.adcname = ao['data']['card']['name']
            s.adlid = ao['data']['list']['id']
            s.adlname = ao['data']['card']['name']
        # copyCard (treat like createCard) 
        elif s.atype == 'copyCard': 
            if s.dbg: print("")  
            #tmp = kidD(ao)
            s.adcid = ao['data']['card']['id']
            s.adcname = ao['data']['card']['name']
            s.adlid = ao['data']['list']['id']
            s.adlname = ao['data']['card']['name']
        # moveCardToBoard (treat like createCard) 
        elif s.atype == 'moveCardToBoard': 
            if s.dbg: print("")  
            #tmp = kidD(ao)
            s.adcid = ao['data']['card']['id']
            s.adcname = ao['data']['card']['name']
            s.adlid = ao['data']['list']['id']
            s.adlname = ao['data']['card']['name']
        # commentCard
        elif s.atype == 'commentCard': 
            if s.dbg: print("")  
            #tmp = kidD(ao)
            s.adcid = ao['data']['card']['id']
            s.adcname = ao['data']['card']['name']
            s.adlid = ao['data']['list']['id']
            s.adlname = ao['data']['card']['name']
            
            s.adtext = ao['data']['text']
        # updateCard
        elif s.atype == 'updateCard': 
            if s.dbg: print("")   
            #tmp = kidD(ao)
            s.adcid = ao['data']['card']['id']
            s.ado =  ao['data']['old']
        else:
            if s.dbg: print("")
            raise Exception("** Unknown card {}".format(s.atype))
            # IF this exception occurs, add the proper card type to the list 
            # above as well as the if clause immediately below to persist 
    
        # persist the cards listed below and skip all others
        if s.dbg: print(".. Reviewing action {} for card {}".format(s._id,s.adcid))
        if s.atype in ('createCard', 'copyCard', 'moveCardToBoard', 
                     'commentCard', 'updateCard'): 
            #print(".. .. Examine!")
            if s._cid == s.adcid: 
                if s.dbg: print(".. Action {} for card {}".format(s.aid,s.adcid))
                # only need this next if we want the dict instead of object 
                action = {'atype' : s.atype, "adate" : s.adate, "aid" : s.aid, 
                          'adcid' : s.adcid, "adcname" : s.adcname, 
                          "adlid" : s.adlid, "adlname" : s.adlname, 
                          "adtext": s.adtext, "ado" : s.ado}
                
            else:
                # warn...this might be ok IF the card was moved/copied/or something...
                warnings.warn("** Trying to add Action {} for another Card {}".format(
                        s.adcid, s._cid))
        else:
            pass      # without saving anything 
            if s.dbg: print(".. Skipping card type {} id {}".format(s.atype, s.adcid))
        
        # return action dict BUT prefer to use the object...ok?
        return(action)

class Card:
    """ Trello Card object """
    dbg = False 
        
    def __init__(s, cobj):
        """ Convert JSON card into python object represenation """
        
        if s.dbg: print(".. C_Card id %s, name %s" % (cobj['id'], cobj['name']))
        s.id = cobj['id']
        s.desc = cobj['desc']
        s.name = cobj['name']
        s.dateLastActivity = datetime.datetime.strptime(cobj['dateLastActivity'],'%Y-%m-%dT%H:%M:%S.%fZ')
        s.idBoard = cobj['idBoard']
        s.idList = cobj['idList']
        s.actions = []      #empty list for action objects 
        
    def __repr__(s): 
        return(f'{s.__class__.__name__}('
               f'{s.name!r}, {s.desc!r}, {s.id!r}, {s.idBoard!r}, {s.idList!r}, \
               {s.dateLastActivity!r}, #Actions={len(s.actions)})')
    
    def __reprx__(s):
        rs = "Card   {}: {}: {}".format(s.id, s.name, s.desc)
        rs = rs + "\n Board {}: List {}".format(s.idBoard, s.idList)
        rs = rs + "\n Last  {}".format(s.dateLastActivity)
        return rs
    
    def add_actions(s, asobj): 
        """ Given the top actions json node, extract those for this card """
        s.dbg = False 
        if s.dbg: print("__ C_Add Actions: ")
        
        # cycle thru actions and select those matching this card 
        s.actions = []
        for ao in asobj: 
            if s.dbg: tmp = kidD(ao)
            if ao['type'] not in ('createBoard','createList', 'updateList'):
                aid = ao['data']['card']['id']
                if s.id == aid:
                    a = Action(ao, s.id) 
                    a.add_actions(ao)
                    s.actions.append(a)
        
        # sort then return # actions found in case of curiosity 
        s.actions = sorted(s.actions, key=lambda x: x.adate, reverse=True)
        return(len(s.actions))
    
    def print_actions(s): 
        """ Print actions for this card """ 
        
        for a in s.actions: 
            print(".. A date({}), id({}), type({}), name({})".format(
                    a.adate, a.aid, a.atype, a.adtext))
            
            
        

#==============================================================================
if __name__ == "__main__":
    
    # setup argument parser (p)
    p = argparse.ArgumentParser(description="Output Trello Cards with Actions by Date")
    p.add_argument('-f', '--file', help='json input file')
    p.add_argument('-p', '--print', default=False, action='store_true', help='set to print console output')
    args = p.parse_args()
    if args.file:
        json_file = args.file 
    
    print("== Examine input Trello file {}. Printing is {}".format(json_file, args.print))
        
    # read the file 
    with open(json_file) as data_file:
        jdata = json.load(data_file)
    
    # gather global attributes such as current board 
    for k,v in jdata.items():
        if k == 'id': 
            idBoard = v
        if k == 'name':
            nameBoard = v
    if args.print: print("== Board {}, Name {}".format(idBoard, nameBoard))
    
    # create cards
    jcards = jdata['cards']
    cards = []
    for jcard in jcards: 
        c = Card(jcard)
        cards.append(c)
    
    # add actions 
    jactions = jdata['actions']
    for c in cards: 
        l = c.add_actions(jactions)
        if args.print: 
            print(".. C added {} actions".format(l))
            c.print_actions() 
    cards = sorted(cards, key=lambda x: x.dateLastActivity)
    
    # output time 
    if args.print: 
        print("== Printing")
        for c in cards: 
            print("-- [{}] {:8.8} | {:12.12} | {} | {:20.20} | {:8.8} |".format(
                    "C", c.id,c.name,c.dateLastActivity,c.desc,c.idList))
            for a in c.actions: 
                print("-- [{}] {:8.8} | {:12.12} | {} | {:20.20} | {:8.8} |".format(
                        "a", a.adcid, "", a.adate, "", a.adlid),end='') 
                print(" {:12.12} | {:20.20} | {} |".format(
                        a.atype, a.adtext, a.ado))
                print("")
    
    # always output a csv 
    print("== CSV Output")
    flds = ['item',
        'cDate',
        'cId',
        'cName',
        'cDesc',
        'cBoardId',
        'cListId',
        'cListName',
        'aType',
        'aText',
        'aId',
        'aOldValue',]
    
    with open(json_file+".csv", mode='w') as csv_file: 
        w = csv.DictWriter(csv_file, fieldnames=flds)
        w.writeheader()
        
        for c in cards:
            pass
            # card row
            rval = { 'item' : "card",
                    'cDate' : c.dateLastActivity, 
                    'cId': c.id,
                    'cName' : c.name,
                    'cDesc' : c.desc,
                    'cBoardId' : c.idBoard,
                    'cListId' : c.idList,
                    'cListName' : "",
                    'aType' : "",
                    'aText' : "",
                    'aId' : "",
                    'aOldValue' : ""}
            w.writerow(rval)
            
            # action rows
            for a in c.actions:
                rval = { 'item' : "action",
                    'cDate' : a.adate, 
                    'cId': a.adcid,
                    'cName' : a.adcname,
                    'cDesc' : "",
                    'cBoardId' : "",
                    'cListId' : a.adlid,
                    'cListName' : a.adlname,
                    'aType' : a.atype,
                    'aText' : a.adtext,
                    'aId' : a.aid,
                    'aOldValue' : a.ado}
                #print(rval)
                w.writerow(rval)
    print("== Done ")            