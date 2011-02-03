from django.shortcuts import render_to_response as r2r
from django.http import HttpResponseRedirect as httpRedirect
from polldaddyAPI import PollDaddyAPI as pollAPI
from time import time

def index(request):
    results = {}
    if 'uid' in request.REQUEST and request.REQUEST['uid']:
        # Get and set the UserCode
        uid = request.REQUEST['uid']
        results['uid'] = uid
        #request.session['uid'] = uid # set the session cookie
        pd = pollAPI(uid)
        start = time()
        codeJSON = pd.getUserCodeJSON(uid)
        stop = time()
        userCodeSpeed = stop - start
        uCode = pd.parseUserCode(codeJSON)
        pd.setUserCode(uCode)
        #request.session['userCode'] = uCode # store the usercode in the session
        results['userCode'] = uCode
        
        # Get the list of IDs with Questions
        start = time()
        pollIDsJSON = pd.getPollsJSON(uCode) #returns the json response
        stop = time()
        pollIDs = pd.getPollIDs(pollIDsJSON)
        
        pollIDsSpeed = stop - start
        results['pollIDs'] = pollIDs
        
        # print the speeds
        print 'It took %.2f seconds to retrieve the userCode' % userCodeSpeed
        print 'It took %.2f seconds to retrieve the pollID list' % pollIDsSpeed
    
    return r2r('polldaddy/main.html', results)

def editpoll(request):
    results = {}

    if 'pid' in request.REQUEST:
        pid = request.POST['pid']
        uid = request.POST['uid']
        uCode = request.POST['userCode']
        results['pid'] = pid
        results['uid'] = uid
        results['userCode'] = uCode
        
        # get the poll belonging to pid
        pd = pollAPI(uid)
        pd.setUserCode(uCode)
        pollJSON = pd.getPollJSON(pid)
        results['poll'] = pollJSON
        return r2r('polldaddy/editpoll.html', results)
    else:
        return httpRedirect('/polldaddy/')