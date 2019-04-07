from textblob import TextBlob     #library to analyse sentiment
import re
import sys,tweepy                   #library to extract twitter data
import matplotlib.pyplot as plt     #library to plot graph

#percentage function
def percentage(part,whole):
	return 100* float(part)/float(whole)

# keys and tokens from the Twitter Dev Console
consumerKey='mgbOcqvdyJD3uh5pPQfPKtsWM'
consumerSecret='3DSpBeQB2IegVzFICK6a08w3TTCoNKFQ6H7q6WafBQgUirtJpC'
accessToken='923927317470093312-DhzXggAVIzISaCbtVEadhWtViYXaooN'
accessTokenSecret='l5SnMQuJuWP1oCEbIqAdWkLydR2qr7VWTKj2pGoUIhTVN'

# attempt authentication
try:
  # create OAuthHandler object
	auth=tweepy.OAuthHandler(consumer_key=consumerKey,consumer_secret=consumerSecret)
   # set access token and secret
	auth.set_access_token(accessToken,accessTokenSecret)
  # create tweepy API object to fetch tweets
	api=tweepy.API(auth)
except:
	print("Error: Authentication Failed")

 #taking input
searchTerm=input("Enter Keyword/hashtag to search about:")
noOfSearchTerms=int(input("Enter how many tweets to analyze:"))

#extracting tweets
tweets=tweepy.Cursor(api.search,q=searchTerm).items(noOfSearchTerms)

# defining positive, negative, neutral, polarity
positive=0
negative=0
neutral=0
polarity=0

# removing links, special characters
def clean_tweets(tweet): 
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

#defining counters and list
pcount=0
ncount=0
nucount=0
ptweets=[]
ntweets=[]
nutweets=[]
for tweet in tweets:
  # cleaning tweet and analysis the polarity of tweet
	analysis = TextBlob(clean_tweets(tweet.text))
	polarity+=analysis.sentiment.polarity

   # count positive tweet and storing it in list
	if(analysis.sentiment.polarity>0.00):
		positive=positive+1
		if(pcount<5):
			pcount+=1;
			ptweets.append(tweet)
      # count negative tweet and storing it in list
	elif(analysis.sentiment.polarity<0.00):
		negative=negative+1
		if(ncount<5):
			ncount+=1;
			ntweets.append(tweet)
      # count neutral tweet and storing it in list
	elif(analysis.sentiment.polarity==0):
		neutral=neutral+1
		if(nucount<5):
			nucount+=1;
			nutweets.append(tweet)
	
# calculating percentage of positive, negative and neutral tweet
positive= percentage(positive,noOfSearchTerms)
negative = percentage(negative,noOfSearchTerms)
neutral= percentage(neutral,noOfSearchTerms)

# calculating upto 2 decimal
positive=format(positive,'.2f')
neutral=format(neutral,'.2f')
negative=format(negative,'.2f')



print("How People Are Reacting on "+searchTerm+" by analyzing " + str(noOfSearchTerms)+" Tweets.")

# printing the reaction that have the highest percentage
if(positive>neutral):
	if(negative>positive):
		print("Negative")
	else:
		print("Positive")
else:
	if(neutral>negative):
		print("Neutral")
	else:
		print("Negative")

#printing first 5 positive tweets 
print("\n\nPositive tweets:") 
for tweet in ptweets[:15]: 
    print(tweet.text) 
  
# printing first 5 negative tweets 
print("\n\nNegative tweets:") 
for tweet in ntweets[:15]: 
    print(tweet.text) 

# printing first 5 neutral tweets 
print("\n\nNeutral tweets:") 
for tweet in nutweets[:15]: 
    print(tweet.text) 

# ploting the graph and labeling of the sentiments
labels=['Positive ['+str(positive)+"%]",'Negative ['+str(negative)+"%]","Neutral ["+str(neutral)+"%]"]
sizes=[positive,negative,neutral]
colors=['blue','red','green']
patches,texts = plt.pie(sizes,colors=colors,startangle=90)
plt.legend(patches,labels,loc = "best")
plt.title("How people are reacting on "+searchTerm+" by analyzing " +str(noOfSearchTerms)+" Tweets.")
plt.axis("equal")
plt.tight_layout()
plt.show()
