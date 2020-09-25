""" Participants """
from collections import namedtuple

from .base import DonorDriveBase
from .log import root_logger

mod_logger = root_logger.getChild('participants')
Participant = namedtuple('Participant',
                         [
                             'avatarImageURL',
                             'campaignDate',
                             'campaignName',
                             'createdDateUTC',
                             'displayName',
                             'eventID',
                             'eventName',
                             'fundraisingGoal',
                             'isTeamCaptain',
                             'numDonations',
                             'participantID',
                             'sumPledges',
                             'sumDonations',
                             'teamID',
                             'teamName',
                             'raw',
                         ],
                         rename=True,
                         )


class Participants(DonorDriveBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def sub_base(self):
        return 'participants'

    def sub_by_pid(self, participantID):
        return 'participants/%d' % participantID

    def sub_by_eid(self, eventID):
        return 'events/%d/participants' % eventID

    def sub_by_tid(self, teamID):
        return 'teams/%d/participants' % teamID

    @classmethod
    def _p_to_p(cls, data):
        kws = {}
        for f in Participant._fields:
            if f == 'raw':
                kws[f] = data
            else:
                kws[f] = dict(data).get(f, None)
        return Participant(**kws)

    def participants(self):
        """ Get a list of ALL EL participants
        WARNING: This takes a LOT of requests! It's a ton of data...
        """
        fresp = self.fetch(sub_url=self.sub_base())
        for t in fresp:
            yield self._p_to_p(t)

    def participant(self, participantID):
        """ Get a single EL participant
        """
        fresp = self.fetch(sub_url=self.sub_by_pid(participantID))
        return self._p_to_p(fresp)

    def participants_for_event(self, eventID):
        """ Get all participants for the given event """
        fresp = self.fetch(sub_url=self.sub_by_eid(eventID))
        for t in fresp:
            yield self._p_to_p(t)

    def participants_for_team(self, teamID):
        """ Get all participants for the given team """
        fresp = self.fetch(sub_url=self.sub_by_tid(teamID))
        for t in fresp:
            yield self._p_to_p(t)
