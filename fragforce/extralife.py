import requests
import fragforce


class WebServiceException(Exception):
    pass


@fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
def team(team_id):
    """Convenience method to instantiate a Team

    :param team_id: The assigned team ID
    """
    try:
        t = Team.from_url(team_id)
    except WebServiceException:
        t = None

    return t


@fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
def participants(team_id):
    """Convenience method to retrieve a Team's participants

    :param team_id: The assigned team ID
    """
    try:
        p = Team.from_url(team_id).participants()
    except WebServiceException:
        p = None

    return p


@fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
def participant(participant_id):
    """Convenience method to retrieve a Participant

    :param participant_id: The assigned participant ID
    """
    try:
        p = Participant.from_url(participant_id)
    except WebServiceException:
        p = None

    return p


@fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
def participant_donations(participant_id):
    """Convenience method to retrieve a Participant's donations

    :param participant_id: The assigned participant ID
    """
    try:
        d = Participant.from_url(participant_id).donations()
    except WebServiceException:
        d = None

    return d


class Team(object):
    def __init__(self, team_id, name, raised, goal, avatar_url, created):

        # extra-life assigned team ID
        self.team_id = team_id

        # the team name provided by the organizer
        self.name = name

        # how much money the team has raised thus far
        self.raised = raised

        # the fundraising goal the team has, if any
        self.goal = goal

        # avatar image URL
        self.avatar_url = avatar_url

        # when the team was registered with Extra-Life
        self.created = created

        # participant cache - see participants()
        self._participants = None

    @classmethod
    @fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
    def from_url(cls, team_id):
        """Constructs an ExtraLifeTeam from the team web service.

        :param team_id: the Extra-Life assigned team ID
        """

        url = ("http://www.extra-life.org/"
               "index.cfm?fuseaction=donorDrive.team&teamID={}&format=json")

        r = requests.get(url.format(team_id))
        if r.status_code != 200:
            raise WebServiceException("Could not retrieve Extra-Life team "
                                      "information.")

        data = r.json()

        name = data.get("name", "Extra-Life Team")
        raised = data.get("totalRaisedAmount", 0.0)
        goal = data.get("fundraisingGoal", 0.0)
        avatar_url = data.get("avatarImageURL", None)
        created = data.get("createdOn", None)

        return cls(team_id, name, raised, goal, avatar_url, created)

    @fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
    def participants(self, force=False):
        """Returns the list of participants for the team using the
        teamParticipants web service call. This call is cached. To force a
        new service call, use force=True

        :param force: Ignore existing participants info. Default False.
        """
        if self._participants is not None and not force:
            return self._participants

        url = ("http://www.extra-life.org/index.cfm?"
               "fuseaction=donorDrive.teamParticipants&teamID={}&format=json")

        r = requests.get(url.format(self.team_id))
        if r.status_code != 200:
            raise WebServiceException("Could not retrieve Extra-Life team "
                                      "participant information.")

        data = r.json()
        self._participants = []
        for pdata in data:
            participant_id = pdata.get("participantID", None)
            created = pdata.get("createdOn", None)
            last_name = pdata.get("lastName", None)
            first_name = pdata.get("firstName", None)
            avatar_url = pdata.get("avatarImageURL", None)
            team_captain = pdata.get("isTeamCaptain", False)

            # these fields are not present in the web service
            raised = None
            goal = None

            p = Participant(participant_id, self.team_id,
                            team_captain, first_name, last_name,
                            raised, goal, avatar_url, created)
            self._participants.append(p)

        return self._participants

    def __repr__(self):
        return "ExtraLifeTeam<team_id={}>".format(self.team_id)


class Participant(object):
    def __init__(self, participant_id, team_id, is_team_captain, first_name,
                 last_name, raised, goal, avatar_url, created):

        # extra-life assigned participant ID
        self.participant_id = participant_id

        # which team they belong to
        self.team_id = team_id

        # is this person a team captain?
        self.is_team_captain = is_team_captain

        # participant-entered name data
        self.first_name = first_name
        self.last_name = last_name

        # how much money this person has raised
        self.raised = raised

        # this person's fundraising goal
        self.goal = goal

        # avatar image url
        self.avatar_url = avatar_url

        # when this person registered
        self.created = created

        # the list of donations this participant has - see donations()
        self._donations = None

    @classmethod
    @fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
    def from_url(cls, participant_id):
        """Constructs an Participant from the participant web service.
        
        :param participant_id: The Extra-Life provided participant ID.
        """
        url = ("http://www.extra-life.org/index.cfm?"
               "fuseaction=donorDrive.participant&"
               "participantID={}&format=json")

        r = requests.get(url.format(participant_id))

        if r.status_code != 200:
            raise WebServiceException("Could not retrieve Extra-Life "
                                      "participant information.")

        data = r.json()

        team_id = data.get("teamID", None)
        is_team_captain = data.get("isTeamCaptain", False)
        first_name = data.get("firstName", "John")
        last_name = data.get("lastName", "Doe")
        raised = data.get("totalRaisedAmount", 0.0)
        goal = data.get("fundraisingGoal", 0.0)
        avatar_url = data.get("avatarImageURL", None)
        created = data.get("createdOn", None)

        participant = cls(participant_id, team_id, is_team_captain, first_name,
                          last_name, raised, goal, avatar_url, created)

        return participant

    @fragforce.cache.memoize(timeout=fragforce.app.config['CACHE_DONATIONS_TIME'])
    def donations(self, force=False):
        """Returns the list of donations for the participant using the
        participantDonations web service call. This call is cached. To force a
        new service call, use force=True

        :param force: Ignore existing donations info. Default False.
        """

        if self._donations is not None and not force:
            return self._donations

        url = ("http://www.extra-life.org/index.cfm?"
               "fuseaction=donorDrive.participantDonations&"
               "participantID={}&"
               "format=json")

        r = requests.get(url.format(self.participant_id))

        if r.status_code != 200:
            raise WebServiceException("Could not retrieve Extra-Life participant "
                                      "donation information.")

        data = r.json()

        self._donations = []
        for d in data:
            donor = d.get("donorName", None)
            amount = d.get("donationAmount", None)
            message = d.get("message", None)
            avatar_url = d.get("avatarImageURL", None)
            created = d.get("created", None)

            donation = Donation(self.participant_id, donor, amount,
                                message, avatar_url, created)

            self._donations.append(donation)

        return self._donations

    def __repr__(self):
        return "Participant<participant_id={}>".format(self.participant_id)


class Donation(object):
    def __init__(self, participant_id, donor, amount, message, avatar_url,
                 created):
        # the owning participant for this donation
        self.participant_id = participant_id

        # who donated the $$$
        self.donor = donor

        # the amount of the donation
        self.amount = amount

        # personalized message from the donor to the participant
        self.message = message

        # if the donor was also an ExtraLife participant, they have an avatar
        self.avatar_url = avatar_url

        # when the donor gave the money (?)
        self.created = created

    def __repr__(self):
        return "Donation<participant_id={}>".format(self.participant_id)
