# Online Callsign Lookup
#
# Author:  Ben Johnson, AB3NJ
# Purpose: Uses hamqth and its api to lookup callsigns.
#          It is not intended to be standalone, but as an interface to hamqth.


import os.path, urllib, urllib.request
import xml.etree.ElementTree as ET


### exeptions ###

class NoLoginError(IOError):
    def __init__(self, arg): self.args = arg
class BadFormatError(IOError):
    def __init__(self, arg): self.args = arg
class BadLoginError(IOError):
    def __init__(self, arg): self.args = arg
class NoResultError(ValueError):
    def __init__(self, arg): self.args = arg
class NotActiveError(ValueError):
    def __init__(self, arg): self.args = arg

### return class ###

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

### lookup class ###

class OnlineLookup:
    def __init__(self):
        self.active = False
        self.prefix = "{https://www.hamqth.com}"

    # connect
    # tries to connect automatically
    # raises exceptions upon fail
    def connect(self):
        # look for appropriate files
        if not os.path.exists('.onlinelookup-login.txt'):
            raise NoLoginError('connect')
        with open('.onlinelookup-login.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) != 2:
                raise BadFormatError('connect')
            else:
                self.username = lines[0].strip()
                self.password = lines[1].strip()
        if os.path.exists('.onlinelookup-key.txt'):
            with open('.onlinelookup-key.txt', 'r') as f:
                lines = f.readlines()
                f.close()
                if len(lines) != 1:
                    self.getKey()

                else:
                    self.key = lines[0].strip()
                    self.active = True
        else:
            self.getKey()

    def createLogin(self, username, password):
        with open('.onlinelookup-login.txt', 'w') as f:
            f.write(username + '\n' + password)
            f.close()

    # gets a key using username and password
    # called when starting and when key expires
    # raises exceptions on failure
    def getKey(self):
        # grab xml data
        req = "https://www.hamqth.com/xml.php?u=" + self.username + "&p=" + self.password
        data = ET.parse(urllib.request.urlopen(req))
        root = data.getroot()

        # pass
        if root[0][0].tag == self.prefix + "session_id":
            self.active = True
            self.key = root[0][0].text

            # write to a file
            with open('.onlinelookup-key.txt', 'w') as f:
                f.write(self.key)
                f.close()

        # fail
        elif root[0][0].tag == self.prefix + "error":
            raise BadLoginError('getKey')

        # catastrophic failure
        else:
            raise BadLoginError('getKey: catastrophic')

    # looks up callsigns on hamqth
    # IF PASS: returns a filled CallsignResult class
    # IF FAIL: raises NoResultError
    def lookup(self, call):
        # error check
        if not self.active: raise NotActiveError('lookup')
        # setup
        lr = LookupResult()
        retdict = {}
        req = "https://www.hamqth.com/xml.php?id=" + self.key + "&callsign=" + call + "&prg=YARL"

        # get the goods
        data = ET.parse(urllib.request.urlopen(req))
        root = data.getroot()

        # error check
        if root[0].tag == self.prefix + "session":
            errmess = root[0][0].text
            if errmess == 'Session does not exist or expired':
                # try again
                # NOTE: this may infinite loop on a bad day maybe
                self.getKey()
                return self.lookup(call)
            elif errmess == 'Callsign not found':
                raise NoResultError('lookup')

        # callsign found
        elif root[0].tag == self.prefix + "search":
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

            # set raw data and return
            lr.raw = retdict
            return lr

# USED FOR TESTING
def newlogin():
    un = input('username: ')
    pw = input('password: ')
    ol.createLogin(un, pw)

if __name__ == "__main__":
    ol = OnlineLookup()
    cont = True
    while True:
        try:
            ol.connect()
            break
        except NoLoginError as e:
            newlogin()
        except BadLoginError as e:
            print('Bad login')
            newlogin()
        except BadFormatError as e:
            print('Bad formatting')
            cont = False
            break

    if cont:
        # test run
        while True:
            print('') # new line for readability
            call = input('Lookup? (type q to exit): ')

            if call == 'q': break
            else:
                try:
                    result = ol.lookup(call)
                    print('')
                    print('random results testing: ' + result.callsign + " " + result.qth + " " + result.grid)
                except NotActiveError:
                    print('not active, exiting')
                    break
                except BadLoginError:
                    print('login bad, exiting')
                    break
                except NoResultError:
                    print('No result')
