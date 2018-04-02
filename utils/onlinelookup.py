# Online Callsign Lookup
#
# Author:  Ben Johnson, AB3NJ
# Purpose: Uses hamqth and its api to lookup callsigns.
#          It is not intended to be standalone, but as an interface to hamqth.


import json, urllib, urllib.request
import xml.etree.ElementTree as ET
from simplecrypt import encrypt, decrypt


# return class
class LookupResult:
    def __init__(self):
        self.callsign = ''
        self.name = ''
        self.country = ''
        self.qth = ''
        self.itu = ''
        self.cq = ''
        self.grid = ''
        self.street1 = ''
        self.street2 = ''
        self.city = ''
        self.state = ''
        self.zip = ''

        self.raw = {}

class OnlineLookup:
    def __init__(self):
        self.active = False
        self.prefix = "{https://www.hamqth.com}"

    # init with existing credentials
    # TODO: implement a way to save passwords safely
    # TODO: also, pretty much this whole function
    def initWithCreds(self, username, fn, passcode):
        f = open(fn)
        pw = 'stopped here'

    # init just a key
    # purpose is mostly for testing
    def initkey(self, key):
        self.key = key

    # initializes a session with hamqth
    # gets an api key for an hour
    def init(self, username, password):
        self.username = username
        self.password = password
        self.active = True
        self.key = self.getKey()

        # check and return
        if self.key == None: return False
        else:
            print("Copy this key. It will work for an hour: " + self.key)
            return True

    # gets a key using username and password
    # called when starting and when key expires
    # IF PASS: returns api key
    # IF FAIL: returns None
    def getKey(self):
        if not self.active: return None

        # grab xml data
        req = "https://www.hamqth.com/xml.php?u=" + self.username + "&p=" + self.password
        data = ET.parse(urllib.request.urlopen(req))
        root = data.getroot()

        # pass
        if root[0][0].tag == self.prefix + "session_id":
            print("passed")
            return root[0][0].text

        # fail
        elif root[0][0].tag == self.prefix + "error":
            print('failed')
            return None

        # catastrophic failure
        else:
            print("Something happened.")
            return None

    # looks up callsigns on hamqth
    # IF PASS: returns a filled CallsignResult class
    # IF FAIL: returns None
    def lookup(self, call):
        # setup
        lr = LookupResult()
        retdict = {}
        req = "https://www.hamqth.com/xml.php?id=" + self.key + "&callsign=" + call + "&prg=YARL"

        # get the goods
        data = ET.parse(urllib.request.urlopen(req))
        root = data.getroot()

        # error check
        # TODO: deal with failure, also in real life :(
        if root[0].tag == self.prefix + "session":
            errmess = root[0][0].text
            if errmess == 'Session does not exist or expired':
                print('Key is bad or out of date')
            elif errmess == 'Callsign not found':
                print('Bad call sign')
            return None
        elif root[0].tag == self.prefix + "search":
            print("GOOD")
            for t in root[0]:
                key = t.tag[len(self.prefix):]
                value = t.text

                # info filling
                if key == 'callsign': lr.callsign = value.upper()
                elif key == 'adr_name': lr.name = value
                elif key == 'adr_street1': lr.street1 = value
                elif key == 'adr_street2': lr.street2 = value
                elif key == 'adr_city': lr.city = value
                elif key == 'us_state': lr.state = value
                elif key == 'adr_zip': lr.zip = value
                elif key == 'country': lr.country = value
                elif key == 'qth': lr.qth = value
                elif key == 'itu': lr.itu = value
                elif key == 'cq': lr.cq = value
                elif key == 'grid': lr.grid = value

                # set raw data for extra whatever
                if key != None and value != None:
                    retdict[key] = value
                    print(key + ': ' + value)

            # set raw data and return
            lr.raw = retdict
            return lr

# USED FOR TESTING
if __name__ == "__main__":
    ol = OnlineLookup()

    ch = input('Do you have a key? (leave blank if not): ')

    if ch != '':
        ol.initkey(ch)

    else:
        un = input('username: ')
        ps = input('password: ')
        ol.init(un, ps)

    # test run
    while True:
        print('') # new line for readability
        call = input('Lookup? (type q to exit): ')

        if call == 'q': break
        else:
            result = ol.lookup(call)
            print('')
            print('random results testing: ' + result.callsign + " " + result.qth + " " + result.grid)
