from typing import Optional, List
from datetime import datetime
from functools import lru_cache
from requests import request
from abc import ABC, abstractmethod

from wnghub.model.notification import Notification


class BaseGithubClient(ABC):

    auth_token: str = ""

    def __init__(self, auth_token: str):
        self.auth_token = auth_token

    @abstractmethod
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = None,
        page: int = 1,
    ) -> List[Notification]:
        raise NotImplementedError("Cannot be called directly from base client")


class GithubApiClient(BaseGithubClient):

    NOTIFICATIONS_URL = "https://api.github.com/notifications"

    @lru_cache(maxsize=None)
    def get_notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        per_page: int = 10,
        page: int = 1,
    ) -> List[Notification]:
        """
        Retrieves users' notifications based on current `auth_token`

        :param all: whether to retrieve all notifications, or just new ones
        :type all: bool
        :param participating: whether to show only notifications user is
                              directly participating in
        :type participating: bool
        :param since: optional datetime for start of notification range to fetch
        :type since: Optional[datetime.datetime]
        :param before: optional datetime for end of notification range to fetch
        :type before: Optional[datetime.datetime]
        :return: List[Notification]
        """
        raw_res = self._notifications(
            all=all,
            participating=participating,
            since=since,
            before=before,
            per_page=per_page,
            page=page,
        )
        return Notification.load_from_json_str(raw_res)

    @lru_cache(maxsize=None)
    def _notifications(
        self,
        all: bool = False,
        participating: bool = False,
        since: Optional[datetime] = None,
        before: Optional[datetime] = None,
        page: int = 1,
        per_page: int = 10,
    ) -> str:
        """
        API call for getting notifications

        :param all: whether to retrieve all notifications, or just new ones
        :type all: bool
        :param participating: whether to show only notifications user is
                              directly participating in
        :type participating: bool
        :param since: optional datetime for start of notification range to fetch
        :type since: Optional[datetime.datetime]
        :param before: optional datetime for end of notification range to fetch
        :type before: Optional[datetime.datetime]
        :return: str
        """
        headers = {
            "Authorization": "token {}".format(self.auth_token),
            "accept": "application/vnd.github.v3+json",
        }
        params = {
            "all": "true" if all else "false",
            "participating": "true" if participating else "false",
            "page": page,
            "per_page": per_page,
        }
        if since is not None:
            params["since"] = since.isoformat()
        if before is not None:
            params["before"] = before.isoformat()
        if per_page > 100:
            raise Exception(
                "Github API support maximum 100 notifications per page for api calls"
            )
        res = request("GET", self.NOTIFICATIONS_URL, headers=headers, params=params)
        return res.text
