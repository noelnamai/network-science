
# coding: utf-8

# In[789]:

import re
import json
import time
import random
import warnings
import requests
import itertools
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime


# In[790]:

#Read in the symbol title dataframe
symbol_title = pd.read_csv("symbol_title.csv", index_col=2, sep=",")
symbol_title = symbol_title[["symbol","sector","industry"]]; symbol_title.head()


# In[791]:

#Allows an application to request user authorization. 
def oauth_authorize():    
    url = "https://api.stocktwits.com/api/2/oauth/authorize"                
    params = urllib.parse.urlencode({"client_id": "f453d9d2f6316db9", 
                                     "response_type": "token",
                                     "redirect_uri": "https://sites.google.com/site/noelnamai/",
                                     "scope": "read,watch_lists,publish_messages,publish_watch_lists,follow_users,follow_stocks"
                                    })    
    oauth = urllib.request.urlopen(url, params.encode("UTF-8"))    
    return oauth


# In[792]:

#Returns the most recent 30 messages for the specified symbol. Includes symbol object in response.
def stream_symbol(symbol):
    url = "https://api.stocktwits.com/api/2/streams/symbol/" + str(symbol) + ".json"
    try:
        content = requests.get(url).json()
    except Exception as error:
        raise Exception("stream_symbol: " + error)
    return content


# In[793]:

#Returns the most recent 30 messages with trending symbols in the last 5 minutes.
def stream_trending():             
    url = "https://api.stocktwits.com/api/2/streams/trending.json"
    payload = {"access_token": "e6f40cf7aad1e2aa5dcb14ca6003968495cf8bb3"}
    try:    
        content = requests.get(url, params=payload).json()
    except Exception as error:
        raise Exception("stream_trending: " + error) 
    return content


# In[794]:

#Creates a dataframe from JSON data returned by the API.
def create_dataframe(data):    
    code = data["response"]["status"]  
    response = []                                 
    if code == 200: 
        for tweet in data["messages"]:
            for symbol in tweet["symbols"]:
                utc = tweet["created_at"]
                row = {"symbol": symbol["symbol"],
                       "title": symbol["title"],
                       "tweet_id": tweet["id"],
                       "text": tweet["body"],
                       "date": datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ").strftime("%d-%m-%Y"),
                       "time": datetime.strptime(utc, "%Y-%m-%dT%H:%M:%SZ").strftime("%H:%M:%S"),
                       "official": tweet["user"]["official"],
                       "name": tweet["user"]["name"],
                       "user_id": str(tweet["user"]["id"]),
                       "user_name": str(tweet["user"]["username"])}
                response.append(row)
                print(row)
    else: 
        raise Exception("create_dataframe: " + data["errors"]) 
    df = pd.DataFrame(response)
    return code, df


# In[795]:

#Clean the data frame and fill in the missing data
def clean_dataframe(df):
    df = df.drop_duplicates()    
    df = df.dropna() 
    df["index"] = range(len(df))
    df = df.set_index("index")
    df["count"] = df.groupby(["symbol"])["user_name"].transform("count")
    df.to_csv("stocktwits_df.csv", index=False, encoding="utf-8")
    return df


# In[ ]:

#Get trending symbols and start building a dataframe from them.
def do_stuff(code):
    symbols = symbol_title["symbol"].values
    np.random.shuffle(symbols)
    for symbol in symbols:
        if code == 200:
            data = stream_symbol(symbol)
            code, df = create_dataframe(data)
            try:
                sdf = pd.read_csv("stocktwits_df.csv", encoding="utf8")
                dfx = pd.concat([df, sdf]) 
            except:
                pass        
            time.sleep(20)
            dfx = clean_dataframe(dfx)  
    return code, dfx


# In[ ]:

#Call the do_stuff()
oauth = oauth_authorize()
code = oauth.getcode()
try:
    code, df = do_stuff(code)
except Exception as error:
    print(error) 


# In[ ]:

#Fill in the data "sector" and "industry" to the main dataframe.
def fill_dataframe(x):   
    symbol = list(set(x["symbol"].values))[0]
    sector = symbol_title["sector"][symbol_title["symbol"] == symbol].values
    industry = symbol_title["industry"][symbol_title["symbol"] == symbol].values
    x["sector"] = sector[0] if len(sector) == 1 else np.nan
    x["industry"] = industry[0] if len(industry) == 1 else np.nan   
    return x


# In[ ]:

df = df.groupby("symbol").apply(fill_dataframe); df.head()


# In[ ]:

{"df_size": len(df.index), 
 "users": len(list(set(df["user_id"]))), 
 "df_symbols": len(list(set(df["symbol"]))), 
 "all_symbols": len(symbol_title)}


# In[ ]:

network = nx.Graph()

#create a dictionary of {tweet_id : [symbols]}
dict1 = {}
rdf = df.groupby("tweet_id")
for tweet_id in list(set(df.tweet_id.values)):
    dict1[tweet_id] = list(rdf.get_group(tweet_id).title.values) 

#Create and save the weighted graph for use in Gephi
for key, value in dict1.items():
    for tup in list(itertools.combinations(value, 2)):        
        source = tup[0]
        target = tup[1] 
        if source != target:
            if network.has_edge(source, target) == True:            
                network[source][target]["weight"] += 1
                pass
            else:
                network.add_nodes_from([source, target])
                network.add_edge(source, target, weight = 1, date = df["date"][df["tweet_id"]==key].values[0])
                
nx.write_gexf(network, "symbol_graph.gexf")


# In[ ]:

#save the unweighted graph for use in R
data = []
node_list = list(network.nodes()) 

for (source, target) in network.edges():
    data.append({"value": 1.0, 
                 "date": network[source][target]["date"],
                 "source": node_list.index(source), 
                 "target": node_list.index(target)
                })    

links = pd.DataFrame(data)
links.to_csv("Rlinks.csv", index=False, encoding="utf-8")

nodes = pd.DataFrame(node_list, columns=["name"])
nodes.to_csv("Rnodes.csv", index=False, encoding="utf-8")


# In[ ]:

min(links.date)

