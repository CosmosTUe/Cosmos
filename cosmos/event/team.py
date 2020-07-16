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
        # 201 Created – no error
        # 400 Bad Request – The event could not be created due to invalid submitted data.
        # 401 Unauthorized – Authentication failure
        # 403 Forbidden – The requested organizer does not exist or you have no permission to create this resource.
        return super().create(organizer, name=name, **kwargs)

    @staticmethod
    def update(organizer, id, **kwargs):
        """
        Update a team

        :param organizer: Name of organizer
        :param id: ID of team
        :param kwargs:  Properties of new object. Refer to Pretix documentation.
        :returns: Tuple of (success: boolean, response: object) where
        response is None if success is False.
        """
        return super().update(organizer, id=id, **kwargs)

    def delete(cls, organizer, id, **kwargs):
        """
        Deletes a team

        :param organizer: Name of organizer
        :param id: ID of team
        :param kwargs:  Properties of new object. Refer to Pretix documentation.
        :returns: Tuple of (success: boolean, response: object) where
        response is None if success is False.
        """
        return super().delete(organizer=organizer, id=id, **kwargs)

    # TODO implement team members


if __name__ == "__main__":
    print(Team.get_all("cosmos"))
