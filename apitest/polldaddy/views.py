from django.shortcuts import render_to_response as r2r
from django.http import HttpResponseRedirect as httpRedirect
from polldaddyAPI import PollDaddyAPI as pollAPI
from time import time
from settings import PD_API_KEY as uid

def index(request):
    results = {}
    message = 'Problem retrieving info'
    if uid:
        results['title'] = 'Poll Manager'
        # Get and set the UserCode
#        uid = request.REQUEST['uid']
        results['uid'] = uid
        pd = pollAPI(uid)

        #Start UserCode timer
        start = time()
        codeJSON = pd.getUserCodeJSON(uid) # maybe try to move this to the top of this script or in settings
        stop = time()
        userCodeSpeed = stop - start
        uCode = pd.parseUserCode(codeJSON) # maybe move this as well
        pd.setUserCode(uCode) # and this
        results['userCode'] = uCode
        
        # Get the list of IDs with Questions
        start = time()
        pollIDsJSON = pd.getPollsJSON(uCode) #returns the json response
        stop = time()
        pollIDs = pd.getPollIDs(pollIDsJSON)
        
        pollIDsSpeed = stop - start
        results['pollIDs'] = pollIDs
        
        # show the speeds
        message1 = 'Time (in seconds) to retrieve the userCode: %.2f' % userCodeSpeed
        message2 = 'Time (in seconds) to retrieve the pollID list: %.2f' % pollIDsSpeed
        results['message'] = [message1, message2]
    
    return r2r('polldaddy/main.html', results)

def create_poll(request):
    # Only allowed via post
    if request.method == "POST" and request.POST['question'] and request.POST['answer'] and request.POST['userCode']:
        question = request.POST['question']
        answer = '''
        [{
            "text": "%s"
        }, {
            "text": "%s"
        }]'''

        # Check the answer
        if request.POST['answer'].lower() == 'yes/no':
            answer = answer %  ('yes', 'no')
        else:
            answer = answer % ('true', 'false')

        pd = pollAPI(uid)
        pd.setUserCode(request.POST['userCode'])

        # Create the poll
        newPollJSON = pd.createPollJSON(question, ans=answer)
        return r2r('polldaddy/create.html', {'poll': newPollJSON})
    else:
        return httpRedirect('/pd/')

    return r2r('polldaddy/create.html')

def edit_poll(request):
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
        return httpRedirect('/apitests/pd/')

def delete_poll(request):
    #template looking for id and poll
    message = 'There was a problem with the delete form.  Make sure at least one value is selected'
    response = r2r('polldaddy/delete_poll_error.html', {'message': message})

    if request.method == 'POST' and 'pid' in request.POST:
        results = {}
        pid = request.POST.getlist('pid')
        uid = request.POST['uid']
        uCode = request.POST['userCode']
        results['pid'] = pid
        results['uid'] = uid
        results['userCode'] = uCode

        # delete the poll belonging to pid
        pd = pollAPI(uid)
        pd.setUserCode(uCode)
        pollJSON = []
        for pollID in pid:
            pollJSON.append(pd.deletePollJSON(pollID))
        results['polls'] = pollJSON
        response = r2r('polldaddy/deletepoll.html', results)
    return response