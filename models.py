#!/usr/bin/env python
import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb


"""models.py
Udacity conference server-side Python App Engine data & ProtoRPC models
$Id: models.py,v 1.1 2014/05/24 22:01:10 wesc Exp $
created/forked from conferences.py by wesc on 2014 may 24
updated for Udacity Nanodegree Project 4 by helmuthb on 2015 May 15
"""

__author__ = 'wesc+api@google.com (Wesley Chun)'


class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT


class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)
    sessionKeysOnWishlist = ndb.StringProperty(repeated=True)


class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)


class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)
    conferenceKeysToAttend = messages.StringField(4, repeated=True)
    sessionKeysOnWishlist = messages.StringField(5, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)


class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)


class Conference(ndb.Model):
    """Conference -- Conference object"""
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    organizerUserId = ndb.StringProperty()
    topics = ndb.StringProperty(repeated=True)
    city = ndb.StringProperty()
    startDate = ndb.DateProperty()
    month = ndb.IntegerProperty()  # TODO: do we need for indexing like Java?
    endDate = ndb.DateProperty()
    maxAttendees = ndb.IntegerProperty()
    seatsAvailable = ndb.IntegerProperty()


class ConferenceForm(messages.Message):
    """ConferenceForm -- Conference outbound form message"""
    name = messages.StringField(1)
    description = messages.StringField(2)
    organizerUserId = messages.StringField(3)
    topics = messages.StringField(4, repeated=True)
    city = messages.StringField(5)
    startDate = messages.StringField(6)  # DateTimeField()
    month = messages.IntegerField(7)
    maxAttendees = messages.IntegerField(8)
    seatsAvailable = messages.IntegerField(9)
    endDate = messages.StringField(10)  # DateTimeField()
    websafeKey = messages.StringField(11)
    organizerDisplayName = messages.StringField(12)


class ConferenceForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    items = messages.MessageField(ConferenceForm, 1, repeated=True)


class Speaker(ndb.Model):
    """
    Speaker -- Speaker object as stored in Data Store.
    Every speaker has a name and can have a twitter handle.
    """
    name = ndb.StringProperty(required=True)
    twitter = ndb.StringProperty()


class SpeakerFormIn(messages.Message):
    """SpeakerFormIn -- inbound speaker form message"""
    name = messages.StringField(1)
    twitter = messages.StringField(2)


class SpeakerFormOut(messages.Message):
    """SpeakerFormOut -- outbound speaker form message"""
    name = messages.StringField(1)
    twitter = messages.StringField(2)
    websafeKey = messages.StringField(3)


class SpeakerForms(messages.Message):
    """SpeakerForms -- multiple Speaker outbound form message"""
    items = messages.MessageField(SpeakerFormOut, 1, repeated=True)


class Session(ndb.Model):
    """
    Session -- Session objectas stored in Data Store.
    In a small deviation from the previous practice I am using
    a repeated KeyProperty to hold the speakers of a session.
    """
    name = ndb.StringProperty(required=True)
    highlight = ndb.StringProperty(repeated=True)
    speaker = ndb.KeyProperty(repeated=True)
    date = ndb.DateProperty()
    startTime = ndb.TimeProperty()
    durationInMins = ndb.IntegerProperty()
    typeOfSession = ndb.StringProperty(default='NOT_SPECIFIED')
    location = ndb.StringProperty()


class SessionType(messages.Enum):
    """SessionType -- session type enumeration value"""
    NOT_SPECIFIED = 1
    WORKSHOP = 2
    LECTURE = 3
    KEYNOTE = 4
    CODELAB = 5


class SessionFormIn(messages.Message):
    """SessionFormIn -- Session inbound form message"""
    name = messages.StringField(1, required=True)
    highlight = messages.StringField(2, repeated=True)
    speaker_key = messages.StringField(3, repeated=True)
    date = messages.StringField(4)
    startTime = messages.StringField(5)
    durationInMins = messages.IntegerField(6)
    typeOfSession = messages.EnumField(SessionType, 7)
    location = messages.StringField(8)


class SessionFormOut(messages.Message):
    """SessionFormOut -- Session outbound form message"""
    name = messages.StringField(1, required=True)
    highlight = messages.StringField(2, repeated=True)
    speaker = messages.MessageField(SpeakerFormOut, 3, repeated=True)
    date = messages.StringField(4)
    startTime = messages.StringField(5)
    durationInMins = messages.IntegerField(6)
    typeOfSession = messages.StringField(7)
    location = messages.StringField(8)
    websafeConferenceKey = messages.StringField(9)
    sessionId = messages.StringField(10)


class SessionForms(messages.Message):
    """SessionForms -- multiple Session outbound form message"""
    items = messages.MessageField(SessionFormOut, 1, repeated=True)


class TeeShirtSize(messages.Enum):
    """TeeShirtSize -- t-shirt size enumeration value"""
    NOT_SPECIFIED = 1
    XS_M = 2
    XS_W = 3
    S_M = 4
    S_W = 5
    M_M = 6
    M_W = 7
    L_M = 8
    L_W = 9
    XL_M = 10
    XL_W = 11
    XXL_M = 12
    XXL_W = 13
    XXXL_M = 14
    XXXL_W = 15


class QueryForm(messages.Message):
    """QueryForm -- query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)


class QueryForms(messages.Message):
    """
    QueryForms -- multiple QueryForm inbound form message
    """
    filters = messages.MessageField(QueryForm, 1, repeated=True)
