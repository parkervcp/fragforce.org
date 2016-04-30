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

