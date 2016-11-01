#import the necessary methods from tweepy library
import json

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#variables that contains the user credentials to access Twitter API 
access_token        = "56302544-yTJo5Z5YvK4ZGSgn7wlL4cQxY3KdSoXzjZH75gfXI"
access_token_secret = "23y7XGc3OxAAfSGFQUvH8XZ0ILO4vshkCowu68E5lilJY"
consumer_key        = "Mxhf5XdVpUofoVuy9XDq91cXt"
consumer_secret     = "Im5z7Kx4VzeXOgxYyuoiBb0eeYSkknOvYLgIjdvlBZg3zyMfBn"

#basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    
	def on_data(self, data):
		print(data)
		return True
		
	def on_error(self, status):
		print(status)
		if status == 420:
			return False

if __name__ == "__main__":
    #handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)	
	
    #filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=["Hillary Clinton"])