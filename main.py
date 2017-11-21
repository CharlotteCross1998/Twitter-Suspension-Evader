import sys
try:
    import oauth, tweepy
except:
    try:
        import pip
        pip.main(['install', 'tweepy'])
        pip.main(['install', 'oauth'])
        import oauth, tweepy
    except:
        sys.exit("Error: Could not import pip or pip could not install the required modules. Please manually install the following:\noauth\ntweepy")

c_key = ''
c_secret = ''
a_key = ''
a_secret = ''

#TODO
help_text = "How to get keys:\nVisit http://www.apps.twitter.com, and click \"create new app\".\mEnter a name and a description. For website just put http://127.0.0.1. Click create your twitter application.\nGo to Keys and Access Tokens, and where it says consumer key\ncopy and paste that into c_key. Do the same with consumer secret and c_secret.\nGo down to \"your access token\" and click create my access token.\nSame as before, access token goes in a_key and access secret goes in a_secret.\nIf nothing works, DM me a screenshot of the 4 lines above."
#TODO
"""

Logging to file for errors
Quit whenever?
Read in optional/mandatory filters from a file

"""

if not c_key or not c_secret or not a_key or not a_secret:
    sys.exit("Error: Keys are not defined.\n"+help_text)

try:
    auth = tweepy.OAuthHandler(c_key,c_secret)
    auth.set_access_token(a_key,a_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
    username = api.me().name
except:
    sys.exit("Error authenticating...")

reviewMode = False
popularMode = False

tweets = [[]]
delete_normal = ["nigger", "kys", "kill yourself", "kill yourselves", "fuck you", "you should die"]
delete_paranoia = ["you should", "you are", "die", "kill", "rape", "cum", "murder"]

#because I'm lazy
for i in range(0, len(delete_normal)-1):
    delete_paranoia += [delete_normal[i]]

def downloadTweets():
    global tweets
    print("Downloading tweets... hold on...")
    #tweet_mode='extended' gets 280 but .text doesn't work
    for page in tweepy.Cursor(api.user_timeline,id=username, count=200, include_entities=True).pages(16):
        for status in page:
            if status.text.find("retweeted_status") == -1:
                tweets += [[status.text.lower(), status.id]]
                
def delete(normal):
    global tweets
    global reviewMode
    global popularMode
    count = 0
    #first is a blank array so 1 to skip it
    for i in range(1,len(tweets)-1):
        if normal:
            for j in delete_normal:
                tweet = tweets[i][0]
                if j in tweet:
                    canDelete = True
                    if popularMode:
                        if api.get_status(tweets[i][1]).retweet_count < 20:
                            if reviewMode:
                                print("Status: " + tweet)
                                while True:
                                    choice = input("Delete? (y/n): ")
                                    if choice.lower() == "y":
                                        canDelete = True
                                        break
                                    elif choice.lower() == "n":
                                        canDelete = False
                                        break
                            else:
                                canDelete = True                                
                        else:
                            canDelete = False
                    else:
                        if reviewMode:
                            print("Status: " + tweet)
                            while True:
                                choice = input("Delete? (y/n): ")
                                if choice.lower() == "y":
                                    canDelete = True
                                    break
                                elif choice.lower() == "n":
                                    canDelete = False
                                    break
                    if canDelete:
                        try:
                            api.destroy_status(tweets[i][1])
                            count += 1
                        except Exception as e:
                            print("Error: " + str(e))
        else:
             for j in delete_normal:
                tweet = tweets[i][0]
                if j in tweet:
                    canDelete = True
                    if popularMode:
                        if api.get_status(tweets[i][1]).retweet_count < 20:
                            if reviewMode:
                                print("Status: " + tweet)
                                while True:
                                    choice = input("Delete? (y/n): ")
                                    if choice.lower() == "y":
                                        canDelete = True
                                        break
                                    elif choice.lower() == "n":
                                        canDelete = False
                                        break
                            else:
                                canDelete = True                                
                        else:
                            canDelete = False
                    else:
                        if reviewMode:
                            print("Status: " + tweet)
                            while True:
                                choice = input("Delete? (y/n): ")
                                if choice.lower() == "y":
                                    canDelete = True
                                    break
                                elif choice.lower() == "n":
                                    canDelete = False
                                    break
                    if canDelete:
                        try:
                            api.destroy_status(tweets[i][1])
                            count += 1
                        except Exception as e:
                            print("Error: " + str(e))
    print(str(count)+ " tweets deleted.")
    
def main():
    global reviewMode
    global popularMode
    print("=========")
    print("Main Menu")
    print("=========")
    print("1 - Normal Mode")
    print("This mode deletes ALL tweets with the most commonly reported words")
    print("-----------------------------------------------------------------------------")
    print("2 - Paranoia Mode")
    print("This mode deletes ALL tweets with anything that could be reported")
    print("This includes words that are rediculous to report but they've worked before")
    print("It is HIGHLY recommended you use review mode with this option")
    print("-----------------------------------------------------------------------------")
    print("3 - Toggle popular mode")
    print("Popular mode means your tweets with 20+ rt's won't be flagged up by the bot")
    print("-----------------------------------------------------------------------------")
    print("4 - Toggle review mode")
    print("Review mode means you will be asked to confirm before every tweet")
    print("-----------------------------------------------------------------------------")
    print("5 - Exit")
    choice = 0
    canProgress = False
    while not canProgress:
        try:
            choice = int(input("Input: "))
            if choice > 5 or choice < 1:
                print("...")
            elif choice == 3:
                if popularMode:
                    popularMode = False
                    print("Popular Mode disabled")
                else:
                    popularMode = True
                    print("Popular Mode enabled")
            elif choice == 4:
                if reviewMode:
                    reviewMode = False
                    print("Review mode disabled")
                else:
                    reviewMode = True
                    print("Review mode enabled")
            elif choice == 5:
                sys.exit("")
            else:
                canProgress = True
        except:
            print("...")
    if choice == 1:
        delete(True)
    elif choice == 2:
        delete(False)

downloadTweets()
main()
sys.exit("Exiting...")
