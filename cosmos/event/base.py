import json

import requests

from cosmos.event import errors
from cosmos.settings import AUTHORIZATION_HEADER, PRETIX_DOMAIN


class PretixService:
    """
    Base class for all the Pretix REST API
    """

    __errors = {
        400: errors.InvalidDataError,
        401: errors.AuthenticationError,
        403: errors.AuthorizationError,
        404: None,
        409: errors.ConflictError,
    }

    @classmethod
    def _get_request_url(cls, **kwargs):
        """
        Override to define URL of HTTP request

        :param kwargs: Dictionary of arguments
        :return: HTTP request URL
        """
        raise NotImplementedError

    @classmethod
    def get_all(cls, **kwargs):
        """
        Performs a GET request for all of a certain object.

        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        url = cls._get_request_url(**kwargs)
        return cls.__pretix_request("GET", url)

    @classmethod
    def get(cls, organizer, **kwargs):
        """
        Performs a GET request for information of one object.

        :param organizer: Name of organizer
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        url = cls._get_request_url(organizer=organizer, **kwargs)
        return cls.__pretix_request("GET", url)

    @classmethod
    def create(cls, organizer, **kwargs):
        """
        Performs a POST request to create a new object

        :param organizer: Name of organizer
        :param kwargs:  Properties of new object. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        url = cls._get_request_url(organizer=organizer, **kwargs)

        headers = {"Content-Type": "application/json"}

        return cls.__pretix_request("POST", url, headers=headers, data=kwargs)

    @classmethod
    def update(cls, organizer, **kwargs):
        """
        Performs a PATCH request to modify an object

        :param organizer: Name of organizer
        :param kwargs:  Properties of new object. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        url = cls._get_request_url(organizer=organizer, **kwargs)

        headers = {"Content-Type": "application/json"}

        return cls.__pretix_request("PATCH", url, headers=headers, data=kwargs)

    @classmethod
    def delete(cls, organizer):
        """
        Performs a DELETE request to create a new object

        :param organizer: Name of organizer
        :param kwargs:  Properties of new object. Refer to Pretix documentation.
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        url = cls._get_request_url(organizer=organizer)

        headers = {"Content-Type": "application/json"}

        return cls.__pretix_request("DELETE", url, headers=headers)

    @classmethod
    def __clean_kwargs(cls, kwargs):
        """
        Remove parameters not required in a body

        :param kwargs:
        :return: payload_dict
        """
        kwargs.pop("organizers", None)
        kwargs.pop("name", None)
        kwargs.pop("event", None)
        kwargs.pop("id", None)
        return kwargs

    @classmethod
    def __pretix_request(cls, method, url, **kwargs):
        """
        Generates a HTTP request for Pretix

        :param method: HTTP request method (GET, POST, PATCH, DELETE)
        :param url: URL of HTTP request
        :param kwargs: Body of the requst
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        # Attempts to get headers. If none is given, initialize a dict
        # In all cases, add AUTHORIZATION_HEADER
        kwargs["headers"] = {**kwargs.get("headers", {}), **AUTHORIZATION_HEADER}
        kwargs["data"] = json.dumps(cls.__clean_kwargs(kwargs.get("data", {})))
        # Adds PREFIX_DOMAIN
        if url.startswith("/"):
            new_url = f"{PRETIX_DOMAIN}{url}"
        else:
            new_url = f"{PRETIX_DOMAIN}/{url}"
        # Sends the request
        response = requests.request(method, new_url, **kwargs)
        error = cls.__errors.get(response.status_code, None)
        if error is not None:
            raise error
        return response.json()


if __name__ == "__main__":
    PretixService.get_all()
