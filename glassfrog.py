import requests
import json

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def echo(mystring):
    global file
    file.write(byteify(mystring)+ '\n')

def echoPersonFromRole(role):
    circle = getCircle(role['links']['circle'])
    if (len(role['links']['people']) > 0):
        person = getPerson(role['links']['people'][0])
        echo(circle['name'] + '|' + role['name'] + '|' + person['name'] + '|' + person['email'])
    else:
        echo(circle['name'] + '|' + role['name'] + '|N/A')

def getCircles():
    fac = requests.get(BASE_URL + 'circles/' + '?api_key=' + API_KEY)
    f = json.loads(fac.text)
    print('Got all circles')
    return f['circles']

def getPeople():
    fac = requests.get(BASE_URL + 'people/' + '?api_key=' + API_KEY)
    f = json.loads(fac.text)
    print('Got all people.')
    return f['people']

def getRoles():
    fac = requests.get(BASE_URL + 'roles/' + '?api_key=' + API_KEY)
    f = json.loads(fac.text)
    print('Got all roles.')
    return f['roles']

def getPerson(pid):
    for person in allPeople:
        if (person['id'] == pid):
            return person
    return None

def getCircle(cid):
    for circle in allCircles:
        if (circle['id'] == cid):
            return circle
    return None

if __name__ == '__main__':
    BASE_URL = 'https://api.glassfrog.com/api/v3/'
    API_KEY = '####### REPLACE WITH YOUR API KEY ######'

    file = open('testfile.txt','w')

    allCircles = getCircles()
    allPeople = getPeople()
    allRoles = getRoles()

    for role in allRoles:
        if (role['name'] == 'Facilitator' or role['name'] == 'Secretary'):
            echoPersonFromRole(role)
    file.close()
