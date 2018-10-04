""" Teams """
from .log import root_logger
from .base import DonorDriveBase
from collections import namedtuple
from urllib.parse import urljoin

Team = namedtuple('Team',
                  [
                      'teamID',
                      'name',
                      'avatarImageURL',
                      'createdDateUTC',
                      'eventID',
                      'eventName',
                      'fundraisingGoal',
                      'numDonations',
                      'sumDonations',
                  ],
                  rename=True,
                  )
mod_logger = root_logger.getChild('teams')


class Teams(DonorDriveBase):
    URL_TEAMS = 'teams'
    URL_EVENTS = 'events'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def _team_to_team(cls, data):
        return Team(**data)

    def teams(self):
        """ Return a generator of all teams as Team named tuples """
        fresp = self.fetch(sub_url=self.URL_TEAMS)
        for t in fresp:
            yield self._team_to_team(t)

    def team(self, teamID):
        """ Get a team """
        fresp = self.fetch(sub_url=urljoin(self.URL_TEAMS, str(teamID)))
        return self._team_to_team(fresp.data)

    def event_teams(self, eventID):
        """ Return a generator of all teams as Team named tuples for the given event """
        fresp = self.fetch(sub_url=urljoin(self.URL_EVENTS, str(eventID), self.URL_TEAMS))
        for t in fresp:
            yield self._team_to_team(t)
