import urllib, json, os, time
from datetime import datetime
from xml.dom import minidom

USERNAME = ""
PASSWORD = ""

try:
    with open("ril-export.json", "r") as f:
        bookmarks = json.loads(f.read())
    
    for bookmark in bookmarks:
        query = {}
        query["url"] = bookmark["url"] # note that url "urchin cruft" is automatically removed when posting
        query["description"] = bookmark["title"].encode("utf8")
        query["dt"] = datetime.fromtimestamp(float(bookmark["time_added"])).strftime("%Y-%m-%dT%H:%M:%SZ")
        query["replace"] = "no"
        query["shared"] = "no"
        query["toread"] = "yes" # mark them as "to read"
        query["tags"] = "readitlater" # automatically tag imported entries

        httpresponse = urllib.urlopen("https://" + USERNAME + ":" PASSWORD + "@api.pinboard.in/v1/posts/add?%s" % urllib.urlencode(query))

        if httpresponse.getcode() == 429:
            print "Too many requests! Aborting..."
            break;
        else:
            code = minidom.parseString(httpresponse.read()).documentElement.attributes.get("code").value

            if code != "done":
                print "Error! " + code + ": " + query["url"]

            else:
                print "Added bookmark " + bookmark["item_id"]

            time.sleep(3) # sleep for 3 seconds so that we don't hit the rate limit

except IOError:
    print "Error: Could not connect to server!"