from cosmos.event.base import PretixService


class Team(PretixService):
    """
    HTTP request service for Pretix Teams

    Reference: https://docs.pretix.eu/en/latest/api/resources/teams.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        organizer = kwargs.get("organizer")
        id = kwargs.get("id", "")
        if organizer is None:
            # If organizer does not exist, raise TypeError
            raise TypeError
        # Otherwise, continue with HTTP request
        return f"/api/v1/organizers/{organizer}/teams/{id}"

    @classmethod
    def get_all(cls, organizer, **kwargs):
        return super().get_all(organizer=organizer, **kwargs)

    @classmethod
    def get(cls, organizer, id, **kwargs):
        return super().get(organizer, id=id, **kwargs)

    @classmethod
    def create(cls, organizer, name, **kwargs):
        """
        Create a team

        :param organizer: Name of organizer
        :param name: Name of new team
        :param kwargs: Properties of new team. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().create(organizer, name=name, **kwargs)

    @staticmethod
    def update(organizer, id, **kwargs):
        """
        Update a team

        :param organizer: Name of organizer
        :param id: ID of team
        :param kwargs:  Properties of new team. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().update(organizer, id=id, **kwargs)

    def delete(cls, organizer, id, **kwargs):
        """
        Deletes a team

        :param organizer: Name of organizer
        :param id: ID of team
        :param kwargs:  Properties of new team. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().delete(organizer=organizer, id=id, **kwargs)

    class Token(PretixService):
        """
        HTTP request service for Pretix Team Token

        Reference: https://docs.pretix.eu/en/latest/api/resources/teams.html#team-api-token-endpoints
        """

        @classmethod
        def _get_request_url(cls, **kwargs):
            organizer = kwargs.get("organizer")
            team = kwargs.get("team")
            if organizer is None or team is None:
                raise TypeError
            id = kwargs.get("id", "")
            return f"/api/v1/organizers/{organizer}/teams/{team}/tokens/{id}/"

        @classmethod
        def get_all(cls, organizer, team):
            """
            Performs a GET request for the list of all API tokens of a team

            :param organizer: Name of organizer
            :param team: ID of Team
            :returns: Response given as dictionary
            :raises PretixException: Request exception
            """
            return super().get_all(organizer=organizer, team=team)

        @classmethod
        def get(cls, organizer, team, id):
            """
            Performs a GET request for information on one token

            :param organizer: Name of organizer
            :param team: ID of Team
            :param id: ID of Token
            :returns: Response given as dictionary
            :raises PretixException: Request exception
            """
            return super().get(organizer, team=team, id=id)

        @classmethod
        def create(cls, organizer, team, name):
            """
            Performs a POST request to create a new token

            :param organizer: Name of organizer
            :param team: ID of Team
            :param name: Name of Token
            :returns: Response given as dictionary
            :raises PretixException: Request exception
            """
            return super().create(organizer, team=team, name=name)

        @classmethod
        def update(cls, organizer, **kwargs):
            """
            Pretix Tokens do not support updating/PATCH requests
            """
            raise NotImplementedError

        @classmethod
        def delete(cls, organizer, team):
            """
            Performs a DELETE request to delete a token

            :param organizer: Name of organizer
            :param kwargs:  Properties of new token. Refer to Pretix documentation.
            :returns: Response given as dictionary
            :raises PretixException: Request exception
            """
            return super().delete(organizer, team=team)


if __name__ == "__main__":
    print(Team.get_all("cosmos"))
