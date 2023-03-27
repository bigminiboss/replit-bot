# from .post_ql import post, headers
from typing import Dict, Any, List, Tuple, Callable as Function
from .utils.JSDict import JSDict
from replit import Database
from datetime import datetime

# from datauri import parse
from requests import post as _raw_post, get
from .utils.switch import Switch
from os import environ
from .links import links

# from .utils.EventEmitter import EventEmitter
from pyee import AsyncIOEventEmitter
from time import sleep
from threading import Thread as _Thread
from .exceptions import InvalidSid
import requests
import json
import asyncio

# import aiolimiter
import base64
import random
import logging
from .queries import q
from .colors import green, end, purple, red, bold_green, bold_blue, blue
from aiohttp import ClientSession
from queue import Queue

logger: logging.Logger = logging.getLogger(__name__)


class module:
    pass


class Track(AsyncIOEventEmitter):
    def __init__(self, func: Function[..., Any], ms: int) -> None:
        super()
        super().__init__()
        self.f = func
        self.ms = ms
        self.running = False
        self.t = None

    async def start(self) -> None:
        if self.running:
            return

        async def call_func():
            last = None
            self.running = True
            while self.running:
                n = await self.f()
                if n != last:
                    self.emit("update", n)
                self.last = n
                await asyncio.sleep(self.ms)

        await call_func()

    async def stop(self) -> None:
        if self.running:
            self.running = False


class Client(AsyncIOEventEmitter):
    def __init__(self, sid: str, ratelimit: int = 5) -> None:
        super()
        super().__init__()

        self.backup: str = "https://graphql-playground.pikachub2005.repl.co/"
        self.endpoint: str = "https://replit.com/graphql"
        self.headers: Dict[str, str] = {
            "X-Requested-With": "replit",
            "Origin": "https://replit.com",
            "Accept": "application/json",
            "Referrer": "https://replit.com",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Host": "replit.com",
            "x-requested-with": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0",
        }
        self.number_convert: List[str] = ["1st", "2nd", "3rd"]
        self.__reset_status_codes: List[int] = [429, 403, 520, 503, 502, 500]
        self.posting_cache = Queue()
        self.ratelimit = ratelimit
        self.max_groups = 10
        # self.limiter = aiolimiter.AsyncLimiter(self.ratelimit, 1)
        self.sid = sid

        __temp_headers = self.headers
        __temp_headers["Cookie"] = f"connect.sid={self.sid}"

        self.session = ClientSession(headers=__temp_headers)

        async def __temp_post_wrapper_cu():
            data = await self.gql("currentUser")
            if "currentUser" not in data or not data["currentUser"]:
                raise InvalidSid("SID invalid")
            return data

        async def __temp_post_wrapper_update_cu(data):
            return await self.user.update(data)

        async def __temp_post_wrapper_repl():
            return await self.gql("repl", vars={"id": environ["REPL_ID"]})

        async def __temp_post_wrapper_update_repl(data):
            return await self.repl.update(data)

        async def __temp_emit_wrapper():
            await self.emit("ready", self)

        self.users = UserManager(self)
        self.repls = ReplManager(self)
        self.posts = PostManager(self, self)
        self.comments = CommentManager(self, self)
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(__temp_post_wrapper_cu())

        vars = data["currentUser"]
        # vars.update({"countryCode": data["country"]})
        self.user = CurrentUser(self)
        loop.run_until_complete(__temp_post_wrapper_update_cu(vars))
        self.users.cache[self.user.username] = self.user
        data = loop.run_until_complete(__temp_post_wrapper_repl())
        if data is not None and "repl" in data:
            self.repl = Repl(self)
            self.repl = loop.run_until_complete(
                __temp_post_wrapper_update_repl(data["repl"])
            )
            self.repls.cache[self.repl.id] = self.repl

        # loop.run_until_complete(__temp_emit_wrapper())
        self.emit("ready", self)

    async def search(self, query: str, options: Dict[str, Any] = {}):
        global post
        current = {
            "cache": True,
            "query": query,
            "categories": ["Tags"],
            "onlyCalculatedHits": False,
        }
        current.update(options)
        _ = current
        options = JSDict(current)
        res = await self.gql("search", vars={"options": _})
        search = res["search"]
        results = {"repls": {}, "templates": {}, "users": {}, "posts": {}, "tags": []}
        for r in search["replResults"]["results"]["items"]:
            repl = Repl(self)
            await repl.update(r)
            if options.cache:
                self.repls.cache[repl.id] = repl
            results["repls"][repl.id] = repl
        for t in search["templateResults"]["results"]["items"]:
            template = Template(self)
            await template.update(t)
            results["templates"][template.id] = template
        for u in search["userResults"]["results"]["items"]:
            user = User(self)
            await user.update(u)
            if options.cache:
                self.users.cache[user.username] = user
            results["users"][user.username] = user
        for p in search["postResults"]["results"]["items"]:
            _post = Post(self)
            await _post.update(u)
            if options.cache:
                self.users.cache[_post.id] = _post
            results["posts"][_post.id] = _post
        for t in search["tagResults"]["results"]["items"]:
            current = t["tag"]
            current["lastUsed"] = t["timeLastUsed"]
            current["replsCount"] = t["replsCount"]
            results["tag"].append(current)
        return results

    async def login(self, username: str, password: str) -> str:
        return await self.gql("login", {"username": username, "password": password})

    async def graphql(
        self, sid: str, query: str, vars: Dict[str, Any] = {}
    ) -> Dict[str, Any]:
        """specify sid for post"""
        return await self.post(query, vars, connection=sid)

    async def post(
        self,
        query: str,
        vars: Dict[str, Any] = {},
        raw: bool = False,
        retry_for_internal_errors: bool = True,
        __different_endpoint: str = None,
        connection: str = None,
    ):
        """post query with vars to replit graph query language"""

        __temp_headers = {}

        if connection is not None:
            __temp_headers["Cookie"] = f"connect.sid={connection}"

        class InitialRequest:
            def __init__(self):
                self.status_code = 429
                self.text = ""

        req = InitialRequest()
        number_of_attempts = 0
        max_attempts = 7
        if __different_endpoint is None:
            __different_endpoint = self.endpoint
        while (
            req.status_code in self.__reset_status_codes
            or str(req.status_code).startswith("5")
        ) and number_of_attempts < max_attempts:  # only try 7 times
            current_endpoint = f"{__different_endpoint}?e={int(random.random() * 100)}"
            async with self.session.post(
                current_endpoint,
                json={"query": (query if raw else q[query]), "variables": vars},
                headers=__temp_headers,
            ) as r:
                json_body = await r.json()
                text_body = await r.text()
                status = r.status
            if status in self.__reset_status_codes or str(status).startswith("5"):
                N_TH = (
                    self.number_convert[number_of_attempts]
                    if number_of_attempts < 3
                    else str(number_of_attempts + 1) + "th"
                )
                logger.warning(
                    f"{green}[FILE] POST_QL.py{end}\n{red}[WARNING]{end}\n{red}[STATUS CODE] {status}\n\t{red}[INFO]{end} You have been ratelimited\n\t{bold_blue}[SUMMARY]{end} Retrying query for the {N_TH} time (max retries is 5)"
                )
                number_of_attempts += 1
                sleep(
                    5 * (number_of_attempts)
                )  # as not to overload the server, the sleep time increases per num attempts
                continue

            vars_max = 200
            query_max = 100
            text_max = 200
            _query = query
            _vars = (
                f" {vars}"
                if (len(json.dumps(vars, indent=8)) + 3 >= vars_max or len(vars) <= 1)
                else f"\n\t\t\t{json.dumps(vars, indent=16)[:-1]}\t\t\t" + "}"
            )
            _text = text_body.strip()

            if len(_vars) >= vars_max:
                _vars = _vars[: vars_max - 3] + "..."
            if len(_query) >= query_max:
                _query = _query[: query_max - 3] + "..."
            if len(_text) >= text_max:
                _text = _text[: text_max - 3] + "..."
            if status == 200:
                logger.info(
                    f"{green}[FILE] POST_QL.py{end}\n{green}[INFO]{end} {bold_green}Successful graphql!{end}\n\t{blue}[SUMMARY]{end} queried replit's graphql with these query and vars.\n\t{purple}[EXTRA]{end}\n\t\t{bold_blue}[QUERY]{end} {query}\n\t\t{bold_blue}[VARS]{end}{_vars}\n\t\t{bold_blue}[RESPONSE]{end} {_text}\n\t\t{bold_blue}[IS RAW QUERY]{end} {raw}\n\t\t{bold_blue}[URL END POINT]{end} {current_endpoint}"
                )
            else:
                return logger.error(
                    f"{red}[FILE] POST_QL.py{end}\n{red}[STATUS CODE] {status}\n\t{purple}[EXTRA]{end} {_text}\n\t\t{bold_blue}[QUERY]{end} {query}\n\t\t{bold_blue}[VARS]{end}{_vars}\n\t\t{bold_blue}[IS RAW QUERY]{end} {raw}\n\t\t{bold_blue}[URL END POINT]{end} {current_endpoint}\n\t\t{bold_blue}[RETRY]{end} {retry_for_internal_errors}"
                )
            res = json_body
            if res is None or res["data"] is None:
                return None

            try:
                _ = list(map(lambda x: x["data"], list(res["data"])))
                return _
            except:
                if "data" in res["data"]:
                    return res["data"]["data"]
                else:
                    if "data" in res:
                        return res["data"]
                    else:
                        return res

    async def resolve_cached_post(self) -> None:
        """resolves top x cached posts"""
        amt = 0
        input_json_list = []
        while amt < self.max_groups and not self.posting_cache.empty():
            input_json_list.append(self.posting_cache.get())
            amt += 1

        if amt == 0:
            return

        prepared_json = list(map(lambda x: x["input"], input_json_list))
        for i in prepared_json:
            if i["query"] in q:
                i["query"] = q[i["query"]]

        retries = 0
        status = 500
        while retries < 7 and str(status).startswith("5"):
            current_endpoint = f"{self.endpoint}?e={int(random.random() * 100)}"
            async with self.session.post(current_endpoint, json=prepared_json) as r:
                json_body = await r.json()
                text_body = await r.text()
                status = r.status
                if str(status).startswith("5"):
                    retries += 1
                    await asyncio.sleep(5 * (retries))
                    continue

                for x, y in zip(json_body, input_json_list):
                    if "data" in x and x["data"] and "data" in x["data"]:
                        x = x["data"]["data"]
                    else:
                        if "data" in x:
                            x = x["data"]
                        else:
                            x = x
                    y["resp"].set_result(x)

        if str(status).startswith("5"):
            for i in input_json_list:
                if not i["resp"].done():
                    i["resp"].set_result(None)

    async def cached_post_wrapper(self) -> None:
        if not self.posting_cache.empty():  # deadlock equiv
            # await self.limiter.acquire()  # wait until not past rl
            await self.resolve_cached_post()

    async def gql(self, query: str, vars: Dict[str, Any] = {}) -> Dict[str, Any]:
        """always sends to server with client sid"""
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self.posting_cache.put_nowait(
            {"resp": future, "input": {"query": query, "variables": vars}}
        )

        loop.create_task(self.cached_post_wrapper())
        return await future
        # return await self.post(query, vars)

    def requests(self) -> module:
        return requests

    async def uploadImage(self, datauri: str) -> str:
        async with self.session.post(
            "https://replit.com/data/images/upload",
            {"context": "profile-image", "image": datauri},
        ) as r:
            json_body = await r.json()
            return json_body["data"]["url"]


class UserManager:
    def __init__(self, client) -> None:
        self.c = client
        self.cache = {}

    async def fetch(self, userResolvable, options: Dict[str, Any] = {}):
        current = {"force": False, "cache": True}
        current.update(options)
        options = JSDict(current)
        query, variables = None, None
        user_type = type(userResolvable)
        if user_type == str:
            query, variables = ("userByUsername", {"username": userResolvable})
        elif user_type == int:
            query, variables = ("user", {"id": userResolvable})
        elif user_type == User:
            if getattr(userResolvable, "username", None):
                query, variables = (
                    "userByUsername",
                    {"username": userResolvable.username},
                )
            elif getattr(userResolvable, "id", None):
                query, variables = ("user", {"id": userResolvable.id})
        else:
            return None
        if not options.force:
            property = list(variables.keys())[0]
            var = variables[property]
            if var in self.cache:
                match = self.cache[var]
                return match

        res = await self.c.gql(query, variables)
        if not res[query]:
            return None
        user = User(self.c)
        await user.update(res[query])
        if options.cache:
            self.cache[user.username] = user
        return user

    async def search(self, query: str, options: Dict[str, Any] = {}):
        current = {"cache": True, "limit": 10}
        current.update(options)
        options = JSDict(current)
        res = await self.c.gql(
            "userSearch", vars={"query": query, "limit": options.limit}
        )
        users = res["usernameSearch"]
        c = {}
        for u in users:
            user = User(self.c)
            await user.update(u)
            if options.cache:
                self.c.users.cache[user.username] = user
            c[user.username] = user
        return c


class UserEventManager:
    def __init__(self, client) -> None:
        self.c = client
        self.cache = {}

    async def fetch(self, options: Dict[str, Any] = {}) -> Dict[str, Any]:
        current = {"cache": True, "limit": 10}
        current.update(options)
        options = JSDict(current)
        res = await self.c.gql(
            "getUserEventsFeed", vars={"count": options.limit, "after": ""}
        )
        events = res["getUserEventsFeed"]["items"]
        c = {}
        for e in events:
            event = UserEvent(self.c)
            await event.update(e)
            if options.cache:
                self.cache[event.id] = event
            c[event.id] = event
        return c


class ReplManager:
    def __init__(self, client, user=None) -> None:
        self.c = client
        self.cache = {}
        self.user = user

    async def fetch(self, replResolvable=None, **kwargs):
        if getattr(self, "user", False) and self.user:
            if self.user == self.c.user:
                options = {"cache": True, "limit": 10, "paths": [""]}
                options.update(kwargs)
                options = JSDict(options)
                c = {}
                for path in options.paths:
                    res = await self.c.gql(
                        "dashboardRepls", vars={"path": path, "count": options.limit}
                    )
                    repls = res["currentUser"]["replFolderByPath"]["repls"]["items"]
                    for r in repls:
                        repl = Repl(self.c)
                        await repl.update(r)
                        if options.cache:
                            self.cache[repl.id] = repl
                        c[repl.id] = repl
                return c
            else:
                options = {"cache": True, "limit": 10, "search": None}
                options.update(kwargs)
                options = JSDict(options)
                res = await self.c.gql(
                    "profileRepls",
                    vars={"username": self.user.username, "count": options.limit},
                )
                repls = res["user"]["profileRepls"]["items"]
                c = {}
                for r in repls:
                    repl = Repl(self.c)
                    await repl.update(r)
                    if options.cache:
                        self.cache[repl.id] = repl
                        self.c.repls.cache[repl.id] = repl
                    c[repl.id] = repl
                return c
        else:
            options = {"force": True, "cache": True, "url": False}
            options.update(kwargs)
            options = JSDict(options)
            vars = {}
            typeof = Switch(type(replResolvable))
            if typeof.case(str):
                vars = (
                    {"url": replResolvable} if (options.url) else {"id": replResolvable}
                )
            elif typeof.case(Repl):
                if getattr(replResolvable, "id", False) and replResolvable.id:
                    vars = {"id": replResolvable.id}
            else:
                return None
            if not options.force and "id" in vars and vars["id"] in self.cache:
                return self.cache[vars["id"]]
            res = await self.c.gql("repl", vars=vars)
            repl = Repl(self.c)
            await repl.update(res["repl"])
            if options.cache:
                self.cache[repl.id] = repl
            return repl

    async def generateTitle(self) -> str:
        res = await self.c.gql("replTitle")
        return res["replTitle"]

    async def create(self, options: Dict[str, Any] = {}):
        current = {"cache": True, "title": self.generateTitle(), "language": "nix"}
        current.update(options)
        options = current
        cache = options["cache"]
        del options["cache"]
        res = await self.c.gql("createRepl", vars={"input": options})
        r = res["createRepl"]
        if "id" not in r or not r["id"]:
            return None
        repl = Repl(self.c)
        await repl.update(r)
        return repl

    async def delete(self, replResolvable):
        repl = self.fetch(replResolvable)
        if repl:
            await repl.delete()


class PostManager:
    def __init__(self, client, parent) -> None:
        self.c = client
        self.parent = parent
        self.cache = {}

    async def fetch(self, **kwargs: Dict[str, Any]) -> None:
        res = None
        name = Switch(type(self.parent).__name__)
        if name.case("Client") or name.case("Bot"):
            id = kwargs["id"]
            options = {"cache": True}
            options.update(kwargs)
            options = JSDict(options)
            res = await self.c.gql("post", vars={"id": id})
            if "post" not in res or not res["post"]:
                return None
            _post = Post(self.c)
            await _post.update(res["post"])
            if options.cache:
                self.cache[_post.id] = _post
            return _post
        elif name.case("User") or name.case("CurrentUser"):
            options = {"cache": True, "limit": 10, "order": "new"}
            options.update(kwargs)
            options = JSDict(options)
            res = await self.c.gql(
                "userPosts",
                vars={"username": self.parent.username, "count": options.limit},
            )
            posts = res["userByUsername"]["posts"]["items"]
            c = {}
            for p in posts:
                _post = Post(self.c)
                await _post.update(p)
                if options.cache:
                    self.cache[_post.id] = _post
                c[_post.id] = _post
            return c

    async def trending(self, options: Dict[str, Any] = {}) -> Dict[str, Any]:
        if (
            type(self.parent).__name__ == "Client"
            or type(self.parent).__name__ == "Bot"
        ):
            return None
        options = {"cache": True, "limit": 10, "tags": []}
        res = await self.c.gql(
            "trending",
            vars={
                "options": {
                    "searchQuery": options.search,
                    "count": options.limit,
                    "order": options.order,
                    "tags": options.tags,
                }
            },
        )
        posts = res["replPosts"]["items"]
        c = {}
        for p in posts:
            _post = Post(self.c)
            await _post.update(p)
            if options.cache:
                self.cache[_post.id] = _post
            c[_post.id] = _post
        return c


class NotificationManager:
    def __init__(self, client: Client, seconds: int = 30) -> None:
        self.c = client
        self.cache = {}

        async def __wrapper():
            return await self.c.user.notifications.fetch_all()

        self.track = Track(__wrapper, seconds)

        @self.track.on("update")
        async def resolve_notifications(notifs) -> None:
            _ = list(notifs.keys())
            _.reverse()
            for i in _:
                self.c.emit("notification", i, notifs[i])
            # if len(notifs) > 0:
            #     await self.markAsRead()

    async def fetch(self, options: Dict[str, Any] = {}) -> None:
        current = {"cache": True, "seen": False, "limit": 10}
        current.update(options)
        options = JSDict(current)
        res = await self.c.gql(
            "notifications",
            vars={"count": options.limit, "seen": options.seen},
        )
        notifications = res["notifications"]["items"]
        c = {}
        for n in notifications:
            notification = Notification(self.c)
            await notification.update(n)
            if getattr(notification, "id", None) == None:
                continue
            if options.cache:
                self.cache[notification.id] = notification
            c[notification.id] = notification
        return c

    async def fetch_all(self, options: Dict[str, Any] = {}) -> None:
        current = {"cache": True, "seen": False, "limit": 200}
        current.update(options)
        options = JSDict(current)
        res = {"notifications": {"items": [None for i in range(options.limit)]}}
        while len(res["notifications"]["items"]) >= options.limit:
            res = await self.c.gql(
                "notifications",
                vars={"count": options.limit, "seen": options.seen},
            )

            notifications = res["notifications"]["items"]
            options.limit *= 10
        c = {}
        for n in notifications:
            notification = Notification(self.c)
            await notification.update(n)
            if options.cache:
                self.cache[notification.id] = notification
            c[notification.id] = notification
        return c

    async def markAsRead(self) -> None:
        await self.c.gql("markAsRead")
        self.c.user.notificationCount = 0

    async def startEvents(self) -> None:
        await self.track.start()

    async def stopEvents(self) -> None:
        await self.track.stop()


class MultiplayerManager:
    def __init__(self, client, repl) -> None:
        self.c = client
        self.cache = {}
        self.repl = repl

    async def invite(self, userResolvable) -> None:
        user = await self.c.users.fetch(userResolvable)
        if not user:
            return None
        await self.c.gql(
            "addMultiplayer",
            vars={"username": user.username, "replId": self.repl.id, "type": "rw"},
        )

    async def remove(self, userResolvable) -> None:
        user = await self.c.users.fetch(userResolvable)
        if not user:
            return None
        await self.c.gql(
            "removeMultiplayer",
            vars={
                "username": user.username,
                "replId": self.repl.id,
            },
        )


class FollowingManager:
    def __init__(self, client, user) -> None:
        self.c = client
        self.user = user
        self.cache = {}
        self.events = UserEventManager(self.c)

    async def fetch(self, options: Dict[str, Any] = {}) -> Dict[str, Any]:
        current = {"cache": True, "limit": 10}
        current.update(options)
        options = current
        res = await self.c.gql(
            "follows",
            vars={"username": self.user.username, "count": options["limit"]},
        )
        users = res["userByUsername"]["follows"]["items"]
        c = {}
        for u in users:
            user = User(self.c)
            await user.update(u)
            if options["cache"]:
                self.cache[user.username] = user
                self.c.users.cache[user.username] = user
            c[user.username] = user
        return c

    async def setFollowing(
        self,
        userResolvable,
        should_follow: bool = True,
        options: Dict[str, Any] = {"cache": True},
    ) -> bool:
        user = await self.c.users.fetch(userResolvable)
        if not user:
            return False
        res = await self.c.gql(
            "follow",
            vars={"input": {"targetUserId": user.id, "shouldFollow": should_follow}},
        )
        if not res["setFollowing"]:
            return False
        await user.update(res["setFollowing"]["targetUser"])
        return user.isFollowingCurrentUser


class FollowersManager:
    def __init__(self, client, user) -> None:
        self.c = client
        self.cache = {}
        self.user = user

    async def fetch(self, options: Dict[str, Any] = {}) -> Dict[str, Any]:
        current = {"cache": True, "limit": 10}
        current.update(options)
        options = JSDict(current)
        res = await self.c.gql(
            "followers",
            vars={"username": self.user.username, "count": options.limit},
        )
        users = res["userByUsername"]["followers"]["items"]
        c = {}
        for u in users:
            user = User(self.c)
            await user.update(u)
            if options.cache:
                self.cache[user.username] = user
                self.c.users.cache[user.username] = user
            c[user.username] = user
        return c


class CommentManager:
    def __init__(self, client, parent_class) -> None:
        self.c = client
        self.cache = {}
        self.parent = parent_class

    async def fetch(self, commentResolvable=None, **arguements: Dict[str, Any]):
        name = Switch(type(self.parent).__name__)
        if name.case("Client") or name.case("Bot"):
            options = {"cache": True, "force": False}
            options.update(arguements)
            options = JSDict(options)
            id = None
            _ = Switch(type(commentResolvable))
            if _.case(int):
                id = commentResolvable
            elif _.case(Comment):
                id = commentResolvable.id
            else:
                return None
            if not options.force:
                if id in self.cache:
                    _comment = self.cache[id]
                    return _comment
            res = await self.c.gql("replComment", vars={"id": id})
            c = res["replComment"]
            if "message" in c:
                return None
            comment = Comment(self.c)
            await comment.update(c)
            if options.cache:
                self.cache[comment.id] = comment
                if getattr(comment, "comments", None) and comment.comments:
                    for reply in comment.comments:
                        self.cache[reply.id] = reply
                if getattr(comment, "parentComment", None) and comment.parentComment:
                    self.cache[comment.parentComment.id] = comment.parentComment
            return comment
        elif name.case("Repl"):
            options = {"cache": True, "limit": 10}
            options.update(arguements)
            options = JSDict(options)
            res = await self.c.gql(
                "replComments",
                vars={"id": self.parent.id, "count": options.limit},
            )
            comments = res["repl"]["comments"]["items"]
            cn = {}
            for c in comments:
                comment = Comment(self.c, self.parent)
                await comment.update(c)
                if options.cache:
                    self.cache[comment.id] = comment
                    self.c.comments.cache[comment.id] = comment
                cn[comment.id] = comment
            return cn
        elif name.case("Post"):
            return None
        elif name.case("CurrentUser") or name.case("User"):
            options = {"cache": True, "limit": 10}
            options.update(arguements)
            options = JSDict(options)
            res = await self.c.gql(
                "userComments",
                vars={"username": self.parent.username, "count": options.limit},
            )
            return res
        else:
            return {}


class User:
    """user object. Follow and blocking"""

    def __init__(self, client) -> None:
        self.c = client
        self.repls = ReplManager(self.c, self)
        self.followers = FollowersManager(self.c, self)
        self.following = FollowingManager(self.c, self)
        self.posts = PostManager(self.c, self)

    async def update(self, data: Dict[str, Any]):
        """update profile"""
        timeCreated, presenceStatus = (None, None)
        if "timeCreated" in data and data["timeCreated"]:
            timeCreated = data["timeCreated"]
            del data["timeCreated"]
        if "presenceStatus" in data and data["presenceStatus"]:
            presenceStatus = data["presenceStatus"]
            del data["presenceStatus"]
        for key in data:
            setattr(self, key, data[key])
        if timeCreated is not None:
            self.timeCreated = timeCreated
        if presenceStatus is not None:
            self.lastSeen = presenceStatus["lastSeen"]
            self.online = presenceStatus["isOnline"]

    async def setFollowing(self, should_follow: bool = True) -> bool:
        """follow a user and return whether they are following you"""
        res = await self.c.gql(
            "follow",
            vars={
                "input": {
                    "targetUserId": self.id,
                    "shouldFollow": should_follow and True,
                }
            },
        )
        if res["setFollowing"]:
            return False
        await self.update(res["setFollowing"]["targetUser"])
        return self.isFollowedBycurrentUser

    async def setBlock(self, should_block: bool = True) -> bool:
        """blocks a user and return whether they are blocking you"""
        res = await self.c.gql(
            "block",
            vars={
                "input": {
                    "targetUserId": self.id,
                    "shouldFollow": should_block and True,
                }
            },
        )
        if res["setBlocking"]:
            return False
        await self.update(res["setBlocking"])
        return self.isBlockedBycurrentUser


class CurrentUser(User):
    def __init__(self, client):
        super()
        super().__init__(client)
        self.c = client
        self.repls = ReplManager(self.c, self)
        self.notifications = NotificationManager(self.c)
        self.auth = {"google": None, "github": None, "facebook": None}

    async def update(self, data: Dict[str, Any] = {}):
        """update profile"""

        login = {
            "googleAuth": None,
            "cannySSOToken": None,
            "githubAuth": None,
            "facebookAuth": None,
            "clui": None,
            "usernameRepl": None,
        }
        properties = {}
        for i in data:
            if i in login:
                login[i] = data[i]
            else:
                properties[i] = data[i]
        await super().update(properties)
        self.cannySSOToken = login["cannySSOToken"]
        if login["googleAuth"]:
            self.auth["google"] = login["googleAuth"]["accessToken"]
        if login["githubAuth"]:
            self.auth["github"] = login["githubAuth"]["accessToken"]
        if login["facebookAuth"]:
            self.auth["facebook"] = login["facebookAuth"]["accessToken"]
        if login["clui"]:
            self.clui = login["clui"]
        if login["usernameRepl"]:
            del login["usernameRepl"]["url"]
            self.usernameRepl = self.c.repls.fetch(
                login["usernameRepl"]["id"], **login["usernameRepl"]
            )
        return self

    async def cannySSOToken(self):
        return self.cannySSOToken

    async def auth(self):
        return self.auth

    async def change(self, options: Dict[str, Any] = {}):
        if "image" not in options:
            options["image"] = None
        image = options["image"]
        del options["image"]
        if image:
            # from stackoverflow, ok -_-
            binary = open(image, "rb").read()
            base64_utf8_str = base64.b64encode(binary).decode("utf-8")
            ext = image.split(".")[-1]
            i = f"data:image/{ext};base64,{base64_utf8_str}"
            if i:
                async with self.c.session.post(
                    "https://replit.com/data/images/upload",
                    {"context": "profile-image", "image": i},
                    headers={"Cookie": f"connect.sid={self.c.sid}"},
                ) as r:
                    json_body = await r.json()
                    status = r.status
                if status == 200:
                    options["profileImageId"] = json_body["data"]["id"]
        res = await self.c.gql("updateUser", vars={"input": options})
        await self.update(res["updateCurrentUser"])
        return self


class UserEvent:
    def __init__(self, client) -> None:
        self.c = client

    async def update(self, data: Dict[str, Any]):
        user_events = {
            "timeUpdated": None,
            "user": None,
            "repl": None,
            "comment": None,
            "following": None,
        }
        for i in data:
            if i in user_events:
                user_events[i] = data[i]
            else:
                setattr(self, i, data[i])
        if user_events["timeUpdated"]:
            self.timeUpdated = user_events["timeUpdated"]
        if user_events["user"]:
            self.user = await self.c.users.fetch(user_events["user"])
        if user_events["repl"]:
            self.repl = await self.c.repls.fetch(user_events["repl"])
        if user_events["following"]:
            self.following = await self.c.users.fetch(user_events["following"])
        if user_events["comment"]:
            self.comment = await self.c.comments.fetch(user_events["comment"])
        return self


class ThreadMessage:
    def __init__(self, client) -> None:
        self.c = client

    async def update(self, data: Dict[str, Any]):
        thread_message_data = {"timeCreated": None, "timeUpdated": None, "user": None}
        for key in data:
            if key in thread_message_data:
                thread_message_data[key] = data[key]
            else:
                setattr(self, key, data[key])
        if thread_message_data["timeCreated"]:
            self.timeCreated = thread_message_data["timeCreated"]
        if thread_message_data["timeUpdated"]:
            self.timeUpdate = thread_message_data["timeUpdated"]
        if thread_message_data["user"]:
            self.user = await self.c.users.fetch(thread_message_data["user"])
        return self


class Thread:
    def __init__(self, client) -> None:
        self.c = client
        self.participants = {}
        self.messages = []

    async def update(self, data: Dict[str, Any]):
        thread_data = {
            "timeCreated": None,
            "timeUpdated": None,
            "messages": None,
            "participants": None,
        }
        for key in data:
            if key in thread_data:
                thread_data[key] = data[key]
            else:
                setattr(self, key, data[key])
        if thread_data["timeCreated"]:
            self.timeCreated = thread_data["timeCreated"]
        if thread_data["timeUpdated"]:
            self.timeUpdated = thread_data["timeUpdated"]
        if thread_data["messages"]:
            for m in thread_data["messages"]:
                message = ThreadMessage(self.c)
                await message.update(m)
                self.messages.append(message)
        if thread_data["participants"]:
            for u in thread_data["participants"]:
                user = await self.c.users.fetch(u)
                self.participants[user.username] = user
        return self


class Template:
    def __init__(self, client) -> None:
        self.c = client

    async def update(self, data: Dict[str, Any]):
        for key in data:
            setattr(self, key, data[key])
        return self


class Team:
    def __init__(self, client) -> None:
        self.c = client

    async def update(self, data: Dict[str, Any]):
        for key in data:
            setattr(self, key, data[key])
        return self


class Env:
    def __init__(self, pyDict: Dict[str, Any] = {}) -> None:
        self._env = pyDict

    def __getitem__(self, key):
        return self._env[key]

    def __setitem__(self, key, val) -> None:
        self._env[key] = val

    def __delitem__(self, key) -> None:
        del self._env[key]


class Repl:
    def __init__(self, client) -> None:
        self.c = client
        self.threads = []
        self.multiplayers = MultiplayerManager(self.c, self)
        self.comments = CommentManager(self.c, self)
        self.env = Env()

    async def update(self, data: Dict[str, Any] = {}):
        repl_data = {
            "layoutState": None,
            "owner": None,
            "timeCreated": None,
            "timeUpdated": None,
            "currentUserPermissions": None,
            "annotationAnchors": None,
            "multiplayers": None,
            "database": None,
        }
        for key in data:
            if key in repl_data:
                repl_data[key] = data[key]
            else:
                setattr(self, key, data[key])
        if repl_data["layoutState"]:
            self._layoutState = repl_data["layoutState"]
        if repl_data["owner"]:
            u = User(self.c)
            await u.update(repl_data["owner"])
            self.owner = u
            if repl_data["database"]:
                self.db = Database(
                    f'https://kv.replit.com/v0/{repl_data["database"]["jwt"]}'
                )
        if repl_data["timeCreated"]:
            self.timeCreated = repl_data["timeCreated"]
        if repl_data["timeUpdated"]:
            self.timeUpdated = repl_data["timeUpdated"]
        if repl_data["currentUserPermissions"]:
            self.currentUserPermissions = repl_data["currentUserPermissions"]
        if repl_data["multiplayers"]:
            for u in repl_data["multiplayers"]:
                user = await self.c.users.fetch(u["username"])
                self.multiplayers.cache[user.username] = user
        if getattr(self, "url", False):
            self.usersWhoLiked = await self.likes()
        return self

    async def layoutState(self):
        return self._layoutState

    async def fetchThreads(
        self, options: Dict[str, Any] = {"cache": True}
    ) -> Dict[str, Any]:
        options = JSDict(options)
        res = await self.c.gql("replThreads", vars={"id": self.id})
        threads = res["repl"]["annotationAnchors"]
        c = {}
        for t in threads:
            thread = Thread(self.c)
            await thread.update(t)
            if options.cache:
                self.threads[thread.id] = thread
            c[thread.id] = thread
        return c

    async def fork(self, options: Dict[str, Any] = {}):
        current = {
            "cache": True,
            "title": self.title,
            "description": self.description,
            "language": (
                self.templateInfo.label
                if getattr(self.templateInfo, "label", False)
                else self.templateInfo["label"]
            ),
            "isPrivate": self.isPrivate,
            "originId": self.id,
        }
        current.update(options)
        options = current
        cache = options["cache"]
        del options["cache"]
        res = await self.c.gql("createRepl", vars={"input": options})
        r = res["createRepl"]
        if not r["id"]:
            return None
        repl = Repl(self.c)
        await repl.update()
        if cache:
            self.c.repls.cache[repl.id] = repl
        return repl

    async def delete(self) -> None:
        await self.c.gql("deleteRepl", vars={"id": self.id})

    async def change(self, options: Dict[str, Any] = {}):
        options.update({"id": self.id})
        res = await self.c.gql("updateRepl", vars={"input": options})
        await self.update(res["updateRepl"]["repl"])
        return self

    async def comment(self, body: str, options: Dict[str, Any] = {"cache": True}):
        options = JSDict(options)
        res = await self.c.gql(
            "sendReplComment",
            vars={"input": {"body": body, "replId": self.id}},
        )
        if not res:
            return None
        comment = Comment(self.comment)
        await comment.update(res["createReplComment"])
        if options.cache:
            self.c.comments.cache[comment.id] = comment
        return comment

    async def report(self, reason: str) -> str:
        return await self.c.gql("reportRepl", {"replId": self.id, "reason": reason})[
            "createBoardReport"
        ]["id"]

    async def likes(self) -> List[str]:
        async def fetch_once(after=None):
            if after is not None:
                vars = {"after": after, "url": self.url}
            else:
                vars = {"url": self.url}
            res = await self.c.gql("usersWhoLikedRepl", vars=vars)
            if "repl" not in res or not res["repl"]:
                return None
            current = list(map(lambda x: x["votes"], res["repl"]["posts"]["items"]))
            output = []
            for i in current:
                output.append(
                    {
                        "voters": list(
                            map(lambda x: x["user"]["username"], i["items"])
                        ),
                        "cursor": i["pageInfo"]["nextCursor"],
                    }
                )
            output.reverse()
            return output

        res = await fetch_once()
        if res is None:
            return None
        voters = []
        visited = {}
        for i in range(len(res)):
            r = None
            cursor = res[i]["cursor"]
            current = res[i]["voters"]
            while cursor:
                r = fetch_once(cursor)
                p = r[i]
                cursor = p["cursor"]
                current.extend(p["voters"])
            current.reverse()
            for j in current:
                if j not in visited:
                    voters.append(j)
                    visited[j] = True
        return voters


class Post:
    def __init__(self, client) -> None:
        self.c = client

    async def update(self, data: Dict[str, Any]):
        posts = {
            "user": None,
            "repl": None,
            "replComment": None,
            "timeUpdated": None,
            "timeCreated": None,
            "board": None,
        }
        for i in data:
            if i in posts:
                posts[i] = data[i]
            else:
                setattr(self, i, data[i])
        if posts["user"]:
            self.user = await self.c.users.fetch(posts["user"])
        if posts["repl"]:
            self.repl = await self.c.repls.fetch(posts["repl"])
        if posts["replComment"]:
            comment = Comment(self.c, self.repl)
            await comment.update(posts["replComment"])
            self.comment = comment
            self.comment.post = self
        if posts["timeCreated"]:
            self.timeCreated = posts["timeCreated"]
        if posts["timeUpdated"]:
            self.timeUpdated = posts["timeUpdated"]
        return self

    async def reply(self, body: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return await self.comment.reply(body, **kwargs)


class Notification:
    def __init__(self, client) -> None:
        self.c = client
        self.id = None

    async def update(self, data: Dict[str, Any]):
        notif_data = {"timeCreated": None, "creator": None, "replComment": None}
        for key in data:
            if key in notif_data:
                notif_data[key] = data[key]
            else:
                setattr(self, key, data[key])
        if notif_data["timeCreated"]:
            self.timeCreated = notif_data["timeCreated"]
        if notif_data["creator"]:
            self.creator = await self.c.users.fetch(notif_data["creator"]["username"])
        if notif_data["replComment"]:
            self.comment = await self.c.comments.fetch(
                int(notif_data["replComment"]["id"]), **notif_data["replComment"]
            )
        return self


class Comment:
    def __init__(self, client, parent=None) -> None:
        self.c = client
        self.comments = []
        self.parentComment = parent
        self.id = None

    async def update(self, data: Dict[str, Any]):
        comment_data = {
            "timeCreated": None,
            "timeUpdated": None,
            "user": None,
            "repl": None,
            "post": None,
            "parentComment": None,
            "comments": None,
        }
        for i in data:
            if i in comment_data:
                comment_data[i] = data[i]
            else:
                setattr(self, i, data[i])
        if comment_data["timeCreated"]:
            self.timeCreated = comment_data["timeCreated"]
        if comment_data["timeUpdated"]:
            self.timeUpdated = comment_data["timeUpdated"]
        if comment_data["user"]:
            self.user = await self.c.users.fetch(comment_data["user"]["username"])
        if comment_data["repl"]:
            self.repl = await self.c.repls.fetch(comment_data["repl"])
        if comment_data["post"]:
            self.post = await self.c.posts.fetch(**comment_data["post"])
        if comment_data["parentComment"]:
            parent = comment_data["parentComment"]
            if parent["id"] in self.c.comments.cache:
                self.parentComment = self.c.comments.cache[parent["id"]]
            else:
                # recursively get the root comment
                comment = Comment(self.c)
                await comment.update(parent)
                self.parentComment = comment
        if comment_data["comments"]:
            for c in comment_data["comments"]:
                if c["id"] in self.c.comments.cache:
                    self.comments.append(self.c.comments.cache[c["id"]])
                else:
                    comment = Comment(self.c)
                    parentComment = None
                    if "parentComment" in c:
                        parentComment = c["parentComment"]
                        del c["parentComment"]
                    await comment.update(c)
                    comment.parentComment = self
                    self.comments.append(comment)
        return self

    async def delete(self) -> None:
        """delete comment"""
        if "delete" not in self.currentUserPermission:
            self.currentUserPermission["delete"] = None
        if self.currentUserPermission["delete"] or self.isAuthor or self.repl.isOwner:
            await self.c.gql("deleteComment", vars={"id": self.id})

    async def reply(self, body: str, **options: Dict[str, Any]):
        """reply comment"""
        current = {"cache": True}
        current.update(options)
        options = JSDict(current)
        send_text = (
            f"@{self.user.username} {body}"
            if (getattr(options, "mention", False) and options.mention)
            else body
        )
        if getattr(self, "parentComment", False):
            id = self.parentComment.id
        else:
            id = self.id
        res = await self.c.gql(
            "sendReplCommentReply",
            vars={"input": {"body": send_text, "replCommentId": id}},
        )
        if not res:
            return None
        comment = Comment(self.c)
        await comment.update(res["createReplCommentReply"])
        if options.cache:
            if comment.id != None:
                self.c.comments.cache[comment.id] = comment
        return comment
