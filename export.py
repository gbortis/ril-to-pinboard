# these are the libs we need for http, json, and writing files
import urllib, json, os

APIKEY = ""
USERNAME = ""
PASSWORD = ""

query = {}
query["apikey"] = APIKEY
query["username"] = USERNAME
query["password"] = PASSWORD
query["state"] = "unread" # only import unread bookmarks
query["count"] = ""

# load calls the read method on the resulting GET
try:
    httpresponse = urllib.urlopen("https://readitlaterlist.com/v2/get?%s" % urllib.urlencode(query))
    
    # check the status code
    if httpresponse.getcode() == 200:
        # remember, load takes in the stream!
        jsonresponse = json.load(httpresponse)
    
        # this gets the data from the json object
        bookmarks = jsonresponse["list"]
                 
        # this opens a new file in write mode and will close it when this block is finished
        with open("ril-export.json", "w") as f:
            f.write(json.dumps(bookmarks.values()))
            print "Wrote " + format(len(bookmarks)) + " bookmarks to file: " + os.path.abspath(f.name)
    else:
        print "Error: HTTP status code: " + httpresponse.getcode()

except IOError:
    print "Error: Could not connect to server!"