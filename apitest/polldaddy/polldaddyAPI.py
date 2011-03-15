import urllib2, json
import pdRequests as pdReq
import logging
# documentation for polldaddy's api is located at:
# http://support.polldaddy.com/api/
# according to api docs: 
#### content-type of text/xml for xml requests and application/json for json requests
#### xml payload must conform to http://api.polldaddy.com/pdapi.xsd

logger = logging.getLogger('polldaddyAPI')
logger.setLevel(logging.DEBUG) # This level of message is sent to handler

fh = logging.FileHandler('/home/delane/UW/Python/UWPython/Python2/apitest/polldaddy/polldaddyAPI.log')
fh.setLevel(logging.DEBUG) # This level of message is sent to the file

formatter = logging.Formatter('%(asctime)s--%(funcName)s::%(levelname)s::%(message)s')

fh.setFormatter(formatter)
logger.addHandler(fh)

class PollDaddyAPI(object):
    """
    Implements the methods found in PollDaddys API docs:
        http://support.polldaddy.com/api/
    """
    UID = ''
    PUID = ''
    XSD_URL = pdReq.PD_API_XSD_URL
    userCode = ''
    
    def __init__(self, userID):
        """
        Creates an instance of PollDaddyAPI class.
        userID = the apiUserID created when registering for the API at http://polldaddy.com/register/
        email = email used when registering
        psw = password used to register
        """
        self.UID = userID
        logger.debug('Initialized object with uid - %s' % self.UID)

    def setUserCode(self, userCode):
        """ Sets the usercode for this object """
        self.userCode = userCode
        logger.debug('user code set to: %s' % self.userCode)

    def setParentID(self, pid='0'):
        """ Sets the parentID - used to categorize polls on Polldaddys site """
        self.PUID = pid
        logger.debug('parentID set to: %s' % self.PID)

    #################### JSON METHODS ####################
    def getUserCodeJSON(self, puid="0"):
        """
            Returns the usercode in it's json response format
            uid = UserID
            puid = PartnerUserID
            """
        jsonPayload = pdReq.USER_CODE_REQUEST_JSON % (self.UID,puid)
        ucJSON = self.fetchInfo(jsonPayload)
        logger.debug('returning %s' % ucJSON)
        return ucJSON

    def createPollJSON(self, q, mc='yes', ra='no', oa='no', rt='percent', brv='cookie', be='7200000', cmt='allow', mp='yes', cp='no', cd='0', cpn='0', sid='0', pid='0', fid='0', lid='0', shr='no', met='0', mec='0', pntID='0', ans=''):
        """
        Creates a poll - requires the following parameters:
            uid = userID - api id (class initiated with this already)
            uc = userCode - retrieved by calling getUserCode[JSON|XML] and then setting if with the setUserCode method.
            Poll Parameters:
            q = the question to ask
            mc = Multiple Choice.  This should be a yes or no string. I default to yes
            ra = randomiseAnswers.  This should be a yes or no string. I default to no
            oa = otherAnswer; - yes or no string.  I default to no
                content = yes|no string
            rt = resultsType - show|percent|hide string.  I default to percent
            brv = blockRepeatVoters -  Ensures that votes are unique.  Should be a string of off|cookie|cookieIP.  I default to cookie
            be = blockExpiration - may be used to say how long to block repeat voters.
                May be time in milliseconds or seconds. This is mentioned in the api docs but not in the xsd
                I default to 7200000
            cmt = comments; - This sets how to treat comments.  Choices are a string value of allow|moderate|off. I default to allow
                content = allow|moderate|off string
            mp = makePublic - Determines whether this is a public poll or not.  Choices are yes|no string.  I default to yes
            cp = closePoll - Determines whether this poll is closed or not.  Choices are yes|no string.  I default to no
            cd = closeDate - Determines when to close the poll.  Used with closePoll. This is a datetime string value. A value of 0 says to never close
            cpn = closePollNow - Closes the poll immediately.  Choices are yes|no string.  I default to 0.  If left at 0 this is not included in the transmission
            sid = styleID - determines the style on the poll.  This is an int value in the API which defaults to 0.  If included, it's passed as a string
            pid = packID - API specifies this as an unsignedInt with a default of 0.  If included it's passed as a string
            fid = folderID - API specifies this as an unsignedInt with a default of 0.  If included, it's passed as a string
            lid = languageID - API specifies this as an unsignedInt with a default of 0.  If included, it's passed as a string
            shr = sharing - Not mentioned in the xsd but is in the API doc.  This will add a sharing link for others to share.  It's a yes|no string value.  I default to no
            met = mediaType - XSD defines this as an int but not shown in API doc.  A value of 0 says to not include this param in the transmission
            mec = mediaCode - XSD defines this as a string but not shown in API doc.  A value of 0 says to not include this param in the transmission
            pntID = parentID - XSD defines this as an unsignedLong but not shown in API doc.  A value of 0 says to not include this param in the transmission
            ans = answers;
                answer = text (string)|mediaCode (string)|mediaType (unsignedInt)
                    answer should be a string in the form of the following:
                    [{
                        "text": "yes"
                    }, {
                        "text": "no"
                    }]
        Raises AttributeError if uc, q, or ans are not populated properly
        returns the json object returned by polldaddys api
        """
        returnStr = ''
        if self.userCode and q and ans:
            uid = self.UID
            uc = self.userCode
            temp = pdReq.CREATE_POLL_JSON_REQ % (uid, uc, q, mc, ra, oa, rt, brv, be, cmt, mp, cp, cd, sid, pid, fid, lid, shr)
            if cpn != '0':
                temp = temp + pdReq.CREATE_POLL_JSON_CLOSE_POLL_NOW % cpn
            if met != '0':
                temp = temp + pdReq.CLOSE_POLL_JSON_MEDIA_TYPE % met
            if mec != '0':
                temp = temp + pdReq.CLOSE_POLL_JSON_MEDIA_CODE % mec
            if pntID != '0':
                temp = temp + pdReq.CLOSE_POLL_JSON_PARENT_ID % pntID
            #maybe attempt a regular expression match to see if ans is in the correct format
            returnStr = temp + pdReq.CREATE_POLL_JSON_END % ans
        else:
            logger.debug('RAISING ATTRIBUTE ERROR - uc=%s, q=%s, ans=%s' % (self.userCode, q, ans))
            raise AttributeError('uc=%s, q=%s, ans=%s' % (self.userCode, q, ans))

        logger.info('calling fetchInfo with %s' % returnStr)
        return self.fetchInfo(returnStr)

    def getPollJSON(self, pollID):
        """ Retrieves a poll specified by the poll id. UserCode should be set already """
        jsonPayload = pdReq.GET_POLL_JSON % (self.UID, self.userCode, pollID)
        logger.info('calling fetchInfo with %s' % jsonPayload)
        return self.fetchInfo(jsonPayload)

    def getPollsJSON(self, parentID='0', start='0', end='0'):
        """
        Retrieves a list of polls
        parentID - the id of the Parent if polls are categorized
        start - used if results are to be paged
        end - used if results are to be paged
        if start and end are 0, no paging
        The userCode should be set already
        """
        jsonPayload = pdReq.GET_POLLS_JSON % (self.UID, self.userCode, start, end, parentID)
        logger.info('calling fetchInfo with %s' % jsonPayload)
        return self.fetchInfo(jsonPayload)

    def deletePollJSON(self, pid):
        '''
        Deletes the poll for pid.
        uid - the user id.  Set upon instantiation
        pid - the poll id to delete
        usercode - set by the setUserCode method
        '''
        if self.UID and self.userCode and pid:
            logger.info('Deleting poll with id of: %s' % pid)
            jsonPayload = pdReq.DELETE_POLL_JSON % (self.UID, self.userCode, pid)
        else:
            raise Attributeerror('userCode=%s, userID=%s, pollID=%s' % (self.userCode, self.UID, pid))

        logger.info('Calling fetchInfo with %s' % jsonPayload)
        return self.fetchInfo(jsonPayload)

    #################### XML METHODS ####################
    def initialRequestXML(self, email, password):
        """ implements the pdInitiate request which returns the userCode in XML format """
        xmlPayload = pdReq.INITIAL_REQUEST_XML % (self.UID, '1', self.XSD_URL, email, password)
        logger.info('calling fetchInfo with %s' % xmlPayload)
        return self.fetchInfo(xmlPayload)

    def getUserCodeXML(self):
        """ retrieves the XML returned by the Polldaddy API. """
        xmlPayload = pdReq.USER_CODE_REQUEST_XML % (self.UID, self.PUID, self.XSD_URL)
        logger.info('calling fetchInfo with %s' % xmlPayload)
        return self.fetchInfo(xmlPayload)

    def createAccountXML(self):
        xmlPayload = pdReq.CREATE_ACCOUNT_REQUEST_XML % (self.UID, self.XSD_URL, self.EMAIL)
        logger.info('calling fetchInfo with %s' % xmlPayload)
        return self.fetchInfo(xmlPayload)

    #################### HELPER METHODS ####################
    def fetchInfo(self,payload):
        # reach out to the apiUrl site and send the xmlRequest data to the site
        url = pdReq.PD_API_URL
        user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.237 Safari/534.10'
        headers = {'Accept':'text/*', 'Content-Type':'text/xml', 'User-Agent': user_agent}

        # the dirty work
        logger.info('sending request to %s' % url)
        logger.info('user-agent: %s' % user_agent)
        logger.info('headers: %s' % headers)
        req = urllib2.Request(url, payload, headers)
        response = urllib2.urlopen(req)

        logger.debug("\n---------- REQUEST PAYLOAD ----------\n%s" % payload)	
        resp = response.read()
        logger.debug("\n---------- RETURNING RESPONSE ----------\n%s" % resp)

        return resp

    def parseUserCode(self, payload, type="JSON"):
        """ Parses the user code.
        val = the JSON payload to parse from
        type = JSON or XML 
        """
        logger.info('Parsing UserCode...')
        returnVal = ''
	val = payload
        if type == "JSON":
            if '\\' in payload:
                val = payload.replace('\\', '\\\\')
            obj = json.loads(val)
            # obj should be a dictionary that contains a dictionary with a userCode key
            returnVal = obj['pdResponse']['userCode']
            logger.debug('return value set to: %s' % returnVal)
        else:
            logger.error('WRONG TYPE SPECIFIED')
            raise AttributeError("Wrong type specified")

        logger.debug('Returning %s' % returnVal)
        return returnVal

    def getPollIDs(self, jsonResponsePayload):
        '''
        Returns a dictionary containing an ID as a key and the question as the value.
        If there's no polls then an empty list is returned
        jsonResponsePayload - The response returned by getPollsJSON() method
        '''
        logger.info('parsing:\n%s' % jsonResponsePayload)
        obj = json.loads(jsonResponsePayload)

        #check to make sure there was something to get
        if obj['pdResponse']['demands']['demand'][0]['polls']['total'] != 0:
            respList = obj['pdResponse']['demands']['demand'][0]['polls']['poll']
            #respList should now be a list with x amount of elements.  Each element is a dictionary containing the data I want
            logger.debug('Retrieved:\n%s' % respList)
            pollList = {}
            for poll in respList:
                pollList[poll['id']] = poll['content']

            logger.info('Returning:\n%s' % str(pollList))
        else:
            logger.warning('Returning an empty list')
            pollList = {}

        return pollList

    def getPollListRaw(self, jsonResponsePayload):
        """
        Returns the list of polls as it was returned by the API.
        The list contains more information about the poll.
        Each element in the list is a dictionary representing a poll and it's metadata
        """
        logger.info('parsing:\n%s' % jsonResponsePayload)
        obj = json.loads(jsonResponsePayload)
        respList = obj['pdResponse']['demands']['demand'][0]['polls']['poll']
        logger.info('Returning:\n%s' % str(respList))
        return respList

if __name__ == "__main__":
    u = '67e37610-f575-8528-4ac8-0000523e46e2'
    e = 'delane.jackson@gmail.com'
    p = 'p@ssword'
    pd = PollDaddyAPI(u)

    # Get usercode and set it
    uCode = pd.getUserCodeJSON(u)
    uCode = pd.parseUserCode(uCode)
    pd.setUserCode(uCode)

    #setup a question and answer for a poll and then create a poll with that answer
#    q1 = "Are you happy"
#    q2 = "Are having fun"
#    answer = """[{
#        "text": "yes"
#    }, {
#        "text": "no"
#    }]"""

    #print 'Creating 2 polls...............'
    #print 'POLL1 %s' % pd.createPollJSON(uCode, q1, ans=answer)
    #print 'POLL2 %s' % pd.createPollJSON(uCode, q2, ans=answer)

    #Retrieve poll ids list
    polls = pd.getPollsJSON(uCode)
    print "POLL IDs: "
    pollIDs = pd.getPollIDs(polls)
    firstPoll = pollIDs.keys()[0]
    print pd.getPollJSON(firstPoll)
    
#    print "RAW POLL INFO: "
#    print pd.getPollListRaw(polls)

    
#    print "CREATING POLL.................."
#    print createPollJSON(userCode,"Do you feel good today", ans=answer)a
   
#    print pd.initialRequestXML()
