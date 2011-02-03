# This module defines some strings to use for the requests to Polldaddy

#################### VARS ####################
PD_API_URL = 'https://api.polldaddy.com/'
PD_API_XSD_URL = 'http://api.polldaddy.com/pdapi.xsd'

#################### INTERPOLATED CONSTANTS - XML ####################
INITIAL_REQUEST_XML = """
    <?xml version="1.0" encoding="utf-8" ?>
    <pd:pdInitiate partnerGUID="%s" partnerUserID="%s" xmlns:pd="%s">
        <pd:Email>%s</pd:Email>
        <pd:Password>%s</pd:Password>
    </pd:pdInitiate>
    """

USER_CODE_REQUEST_XML = """
    <?xml version="1.0" encoding="utf-8" ?>
    <pd:pdAccess partnerGUID="%s" partnerUserID="%s" xmlns:pd="%s">
        <pd:demands>
            <pd:demand id="GetUserCode"/>
        </pd:demands>
    </pd:pdAccess>
    """

CREATE_ACCOUNT_REQUEST_XML = """
    <?xml version="1.0" encoding="utf-8" ?>
    <pd:pdAccess partnerGUID="%s" xmlns:pd="%s">
        <pd:demands>
            <pd:demand id="CreateAccount">
                <pd:account>
                    <pd:userName>pootytang</pd:userName>
                    <pd:email>%s</pd:email>
                    <pd:firstName>Delane</pd:firstName>
                    <pd:lastName>Jackson</pd:lastName>
                    <pd:countryCode>US</pd:countryCode>
                    <pd:gender>male</pd:gender>
                    <pd:yearOfBirth>1980</pd:yearOfBirth>
                    <pd:bio>Sa Da Tae</pd:bio>
                </pd:account>
            </pd:demand>
        </pd:demands>
    </pd:pdAccess>
    """

#################### INTERPOLATED CONSTANTS - JSON ####################
USER_CODE_REQUEST_JSON = """
    {
        "pdAccess": {
            "partnerGUID": "%s",
            "partnerUserID": "%s",
            "demands": {
                "demand": {
                    "id": "GetUserCode"
                }
            }
        }
    }
    """

CREATE_POLL_JSON_REQ = """
    {
        "pdRequest": {
            "partnerGUID": "%s",
            "userCode": "%s",
            "demands": {
                "demand": {
                    "poll": {
                        "question": "%s",
                        "multipleChoice": "%s",
                        "randomiseAnswers": "%s",
                        "otherAnswer": {
                            "content": "%s"
                        },
                        "resultsType": "%s",
                        "blockRepeatVotersType": "%s",
                        "blockExpiration": "%s",
                        "comments": {
                            "content": "%s"
                        },
                        "makePublic": "%s",
                        "closePoll": "%s",
                        "closeDate": "%s",
                        "styleID": "%s",
                        "packID": "%s",
                        "folderID": "%s",
                        "languageID": "%s",
                        "sharing": "%s","""

CREATE_POLL_JSON_CLOSE_POLL_NOW = """
                        "closePollNow": "%s,"
    """

CLOSE_POLL_JSON_MEDIA_TYPE = """
                        "mediaType": "%s,"
    """

CLOSE_POLL_JSON_MEDIA_CODE = """
                        "mediaCode": "%s,"
    """
    
CLOSE_POLL_JSON_PARENT_ID = """
                        "parentID": "%s,"
    """
    
CREATE_POLL_JSON_END = """
                        "answers": {
                            "answer": %s
                        }
                    }, "id": "CreatePoll"
                }
            }
        }
    }
    """

GET_POLL_JSON = """
    {
        "pdRequest": {
            "partnerGUID": "%s",
            "userCode": "%s",
            "demands": {
                "demand": {
                    "poll": {
                        "id": "%s"
                    }, "id": "GetPoll"
                }
            }
        }
    }
    """

GET_POLLS_JSON = """
    {
        "pdRequest": {
            "partnerGUID": "%s",
            "userCode": "%s",
            "demands": {
                "demand": {
                    "list": {
                        "start": "%s",
                        "end": "%s",
                        "id": "%s"
                    }, "id": "GetPolls"
                }
            }
        }
    }
    """

DELETE_POLL_JSON = """
    {
        "pdRequest": {
            "partnerGUID": "%s",
            "userCode": "%s",
            "demands": {
                "demand": {
                    "poll": {
                        "id": "%s"
                    }, "id": "DeletePoll"
                }
            }
        }
    }
    """

################### METHODS ####################




