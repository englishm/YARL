#!/usr/bin/env python3

from utils.onlinelookup import hamqth, olerror


def new_login():
    un = input('username: ')
    pw = input('password: ')
    ol.create_login(un, pw)


if __name__ == "__main__":
    ol = hamqth.HamQTHLookup()

    while True:
        try:
            ol.connect()
            break
        except olerror.LookupVerificationError as e:
            print(f'api: {e.api}: bad login')
            new_login()

    # test run
    while True:
        print('')
        call = input('Lookup? (type q to exit): ')

        if call == 'q':
            break
        else:
            try:
                result = ol.lookup(call)
                print('')
                print('random results testing:')
                print('Callsign: ' + result.callsign)
                print('QTH: ' + result.qth)
                print('Grid Square: ' + result.grid)
            except olerror.LookupResultError as e:
                print('Callsign not found')
                continue
            except olerror.NotActiveError:
                print('not active, exiting')
                break
            except olerror.BadLoginError as e:
                print(e.args)
                print('login bad, exiting')
                break
            except olerror.NoResultError:
                print('No result')
