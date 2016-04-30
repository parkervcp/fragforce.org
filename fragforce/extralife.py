import requests


class ExtraLifeTeam(object):
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

    @classmethod
    def from_url(cls, team_id):
        """Constructs an ExtraLifeTeam from the team web service.

        :param team_id: the Extra-Life assigned team ID
        """

        url = ("http://www.extra-life.org/"
               "index.cfm?fuseaction=donorDrive.team&teamID={}&format=json")

        r = requests.get(url.format(team_id))
        if r.status_code != 200:
            raise Exception("Could not retrieve Extra-Life team information.")

        data = r.json()

        name = data.get("name", "Extra-Life Team")
        raised = data.get("totalRaisedAmount", 0.0)
        goal = data.get("fundraisingGoal", 0.0)
        avatar_url = data.get("avatarImageURL", None)
        created = data.get("createdOn", None)

        return cls(team_id, name, raised, goal, avatar_url, created)

    def __repr__(self):
        return "ExtraLifeTeam<team_id={}>".format(self.team_id)


class ExtraLifeParticipant(object):
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

    @classmethod
    def from_url(cls, participant_id):
        """Constructs an ExtraLifeParticipant from the participant web service.
        
        :param participant_id: The Extra-Life provided participant ID.
        """
        url = ("http://www.extra-life.org/index.cfm?"
               "fuseaction=donorDrive.participant&"
               "participantID={}&format=json")

        r = requests.get(url.format(participant_id))

        if r.status_code != 200:
            raise Exception("Could not retrieve Extra-Life participant information.")

        data = r.json()

        team_id = data.get("teamID", None)
        is_team_captain = data.get("isTeamCaptain", False)
        first_name = data.get("firstName", "John")
        last_name = data.get("lastName", "Doe")
        raised = data.get("totalRaisedAmount", 0.0)
        goal = data.get("fundraisingGoal", 0.0)
        avatar_url = data.get("avatarImageURL", None)
        created = data.get("createdOn", None)

        return cls(participant_id, team_id, is_team_captain, first_name,
                   last_name, raised, goal, avatar_url, created)

    def __repr__(self):
        return "ExtraLifeParticipant<participant_id={}>".format(self.team_id)
