"""file that stores the main bot runner code"""

import urllib.parse
import logging
import os
import re
import math
import asyncio
from .AsyncClient import Client
from .links import links
from .html_default_templates import (
    ORIGINAL_HTML,
    PARAM_BIO,
    HTML_LIST,
    BLOCKQUOTE,
    TEMPLATE,
)
from typing import Callable as Function, Any, Dict, Tuple, get_type_hints, List
from flask import Flask, render_template_string, request
from waitress import serve
from threading import Thread
from time import sleep
from .param import Param
from .exceptions import NamesMustBeAlphanumeric, MustBeRunOnReplitForButtons
from .utils._uuid import random_characters
from .post_ql import post
from .colors import green, blue, purple, red, end, bold_green, bold_blue
import uuid

_started_buttons = {}
# line_sep = "-" * os.get_terminal_size().columns
line_sep = "-" * 80
time_header = f"{green}[TIME]{end}"
logger: logging.Logger = logging.getLogger(__name__)
# https://realpython.com/python-logging/
# format edited, datefmt same. Added level
logging.basicConfig(
    format=time_header + " %(asctime)s\n%(message)s\n" + line_sep,
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


class Button:
    def __init__(self, user: str, command: str):
        self.choice = None
        self.user = user
        self.command = command

    def __getattr__(self, key: str):
        global _started_buttons
        if links.docs is None:
            raise MustBeRunOnReplitForButtons(
                "You must run this bot on replit if you want buttons to work"
            )
        if self.command not in _started_buttons:
            _started_buttons[self.command] = {}
        if self.user not in _started_buttons[self.command]:
            _started_buttons[self.command][self.user] = {}
        rand_chars = random_characters(15)
        _started_buttons[self.command][self.user][rand_chars] = None
        parsed = f"{self.command}/{self.user}/{urllib.parse.quote(key)}/{rand_chars}"

        return f"[{key}]({links.docs}/{parsed})"

    async def get_choice(self):
        current = None
        while current is None:
            _ = list(_started_buttons[self.command][self.user].values())
            for i in _:
                if i != None:
                    current = i
                    break
        _started_buttons[self.command][self.user] = {}
        return current


class Bot(Client):
    """main bot object"""

    def __init__(
        self,
        token: str = None,
        prefix: str = "/",
        bio: str = "",
    ) -> None:
        if token is not None:
            super(Client, self).__init__()
            super().__init__(token)
            self.init_ = True
        else:
            self.init_ = False

        async def help_function(ctx, command):
            if command == "None":
                if links.docs is not None:
                    await ctx.reply(f"See the docs there {links.docs}")
                else:
                    await ctx.reply(self.generate_doc_html())
            else:
                await ctx.reply(
                    f"description of command: {self.commands[command]['desc']}"
                )

        async def __current_default(ctx, *args, **kwargs):
            __current = "That is not a valid command."
            __current += (
                f" You can see the bot docs here {links.docs}"
                if links.docs is not None
                else self.generate_doc_html()
            )
            await ctx.reply(__current)

        async def __not_included_params(ctx, *args, **kwargs):
            __current = "please include all required params."
            __current += (
                f" You can check the bot docs here {links.docs}"
                if links.docs is not None
                else self.generate_doc_html()
            )
            await ctx.reply(__current)

        async def __default_call_when_followed(ctx, person) -> None:
            logger.info(
                f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} @{person.username} followed bot"
            )

        self.commands = {
            "help": {
                "call": help_function,
                "desc": "See commands",
                "name": "help",
                "thread": False,
                "params": {"command": Param(required=False, default="None")},
            }
        }
        self.doc_html = None  # deadlock for if html generated || stores html
        self._call_when_followed = __default_call_when_followed
        self._default = __current_default
        self._not_all_required_params_specified = __not_included_params
        self.token = token
        self.bio = bio
        self.prefix = prefix
        self.alias = {}
        self.listeners = {}
        self.threads_ = []

    def command(
        self, name: str, thread: bool = False, desc: str = None, alias: List[str] = []
    ):
        """takes in args"""
        name = name.lower()
        if not name.replace("-", "").isalnum():
            raise NamesMustBeAlphanumeric("Name must be alphanumeric")

        def wrapper(func: Function[..., Any]) -> Function[..., Any]:
            """adds to command list"""
            self.commands[name] = {
                "call": func,
                "desc": desc,
                "name": name,
                "params": get_type_hints(func),
                "thread": thread,
            }
            for i in alias:
                self.alias[i] = name

        return wrapper

    def listener(self, name: str, thread: bool = False, desc: str = None):
        name = name.lower()
        if not name.replace("-", "").isalnum():
            raise NamesMustBeAlphanumeric("Name must be alphanumeric")

        def wrapper(func: Function[..., Any]) -> Function[..., Any]:
            if name not in self.listeners:
                self.listeners[name] = []
            self.listeners[name].append(
                {
                    "call": func,
                    "desc": desc,
                    "name": name,
                    "params": get_type_hints(func),
                    "thread": thread,
                }
            )

        return wrapper

    def follower(self, func):
        self._call_when_followed = func

    def default(self, func):
        self._default = func

    def fallback_param_not_included_case(self, func):
        self._not_all_required_params_specified = func

    async def parse_command(self, command: str):
        """parses command

        @Example-Bot /say message:hi!
        ->
        {
            "options": {
                "message": "hi!"
            },
            "ping statement": "@Example-Bot",
            "command": "hello"
        }
        """
        splited = command.split(" ")
        if len(splited) < 2 or not splited[1].startswith(self.prefix):
            return {}

        output = {
            "options": {},
            "ping statement": splited[0].strip().lower(),
            "command": splited[1].lstrip(self.prefix).strip().lower(),
        }
        _current_command = None
        current = ""
        for i in splited[2:]:
            if ":" in i and _current_command is not None:
                output["options"][_current_command] = current.rstrip()
                _current_command, current = i.split(":")
                current += " "
            elif ":" in i and _current_command is None:
                _current_command, current = i.split(":")
                current += " "
            else:
                current += i + " "
        if _current_command is not None:
            output["options"][_current_command] = current.rstrip()
        return output

    async def valid_command(self, resp: str) -> Tuple[bool, Dict[str, Any]]:
        """validates command. Returns true if is valid `(True, parsed_json)` or false if not `(False, {'None': None})`"""
        if resp is None:
            return (False, {"None": None})
        parsed = await self.parse_command(resp)
        if (
            parsed == {}
            or parsed["ping statement"].strip("@") != self.user.username.lower()
        ):
            return (False, {"None": None})
        return (True, parsed)

    async def get_kwargs(
        self, resp: Dict[str, Any], given_params: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], bool]:
        """get arguements based on type hints of function"""
        params = resp["params"]
        output = {}
        for i in params:
            if i in given_params:
                output[i] = given_params[i]
            elif not params[i].required:
                output[i] = params[i].default
            else:
                return (False, {"None": None})
            if params[i].type_cast is not None:
                output[i] = params[i].type_cast(output[i])
        return (True, output)

    def generate_doc_html(self) -> None:
        """automatically creates the documentation for the bot"""
        if self.doc_html is not None:
            return self.doc_html

        html = ORIGINAL_HTML.format(
            self.user.username,
            self.prefix,
            BLOCKQUOTE.format(self.bio) if self.bio else "",
        )
        for i in self.commands:
            data = self.commands[i]
            if not len(data["params"]) and not data["desc"]:
                bio_ = "this command has no parameters"
            else:
                if data["desc"]:
                    bio_ = BLOCKQUOTE.format(data["desc"])
                else:
                    bio_ = ""

            html += PARAM_BIO.format(self.prefix, data["name"], bio_)
            current_json = {}
            for j in data["params"]:
                _param = data["params"][j]
                current_json[j] = _param.default if not _param.required else None
                html += HTML_LIST.format(
                    j,
                    _param.desc,
                    _param.required,
                    _param.default,
                    _param.type_cast.__name__,
                )

        for i in self.listeners:
            if len(self.listeners[i]) == 0:
                continue
            data = self.listeners[i][0]
            if not len(data["params"]) and not data["desc"]:
                bio_ = "this command has no parameters"
            else:
                if data["desc"]:
                    bio_ = BLOCKQUOTE.format(data["desc"])
                else:
                    bio_ = ""
            html += PARAM_BIO.format(self.prefix, data["name"], bio_)
            current_json = {}
            for j in data["params"]:
                _param = data["params"][j]
                current_json[j] = _param.default if not _param.required else None
                html += HTML_LIST.format(
                    j,
                    _param.desc,
                    _param.required,
                    _param.default,
                    _param.type_cast.__name__,
                )

        return html

    def run(
        self,
        token: str = None,
        auto_create_docs: bool = False,
        flask_app: Flask = None,
        daemon: bool = True,
    ) -> None:
        """main runner code, input a flask app and auto_create_docs if you want auto created docs"""
        if token is not None and not self.init_:
            super()
            super().__init__(token)
            self.init_ = True

        @self.once("ready")
        async def on_ready(client):
            logger.info(
                f'{green}[FILE] BOT.py{end}\n{bold_green}[STARTING BOT]{end} Botting "{bold_blue}{client.user.username}{end}"'
            )

        self.emit("ready", self)
        self.doc_html = self.generate_doc_html()

        if auto_create_docs and flask_app is None:
            flask_app = Flask("replit_bot")

        if flask_app is not None:

            if auto_create_docs:

                @flask_app.route("/")
                def _():
                    return render_template_string(TEMPLATE, html=self.doc_html)

            else:
                links.docs = None

            @flask_app.route("/<command>/<user>/<choice>/<rand_chars>")
            def _parse_button_commands(command, user, choice, rand_chars):
                global _started_buttons
                if request.headers["X-Replit-User-Name"] == "":
                    return render_template_string(
                        TEMPLATE,
                        html='<center><div><script authed="location.reload()" src="https://auth.util.repl.co/script.js"></script></div></center>',
                    )
                if (
                    command in _started_buttons
                    and user in _started_buttons[command]
                    and rand_chars in _started_buttons[command][user]
                    and _started_buttons[command][user][rand_chars] is None
                    and user == request.headers["X-Replit-User-Name"]
                ):
                    _started_buttons[command][user][rand_chars] = choice
                    return render_template_string(
                        TEMPLATE,
                        html="<center><h1>your request has been processed, you can close this tab</h1></center>",
                    )
                else:
                    return render_template_string(
                        TEMPLATE,
                        html="<center><h1>you cannot do this right now</h1></center>",
                    )

        else:
            links.docs = None

        @self.on("notification")
        async def _run(notif_id, notif) -> None:
            """main runner code"""
            # MentionedInPost, MentionedInComment, RepliedToComment, RepliedToPost, AnswerAccepted, MultiplayerJoinedEmail, MultiplayerJoinedLink, MultiplayerInvited, MultiplayerOverlimit, Warning, TeamInvite, TeamOrganizationInvite, Basic, TeamTemplateSubmitted, TeamTemplateReviewedStatus, Annotation, EditRequestCreated, EditRequestAccepted, ReplCommentCreated, ReplCommentReplyCreated, ReplCommentMention, Thread, NewFollower
            await self.gql("markOneAsRead", {"id": notif_id})

            __typename = getattr(notif, "__typename")
            if __typename == "WarningNotification":
                logger.critical(
                    f"{red}[FILE] BOT.py{end}\n{red}[INFO]{end} bot has been warned"
                )
            elif __typename == "NewFollowerNotification":
                await self._call_when_followed(self, notif.creator)
            elif getattr(notif, "comment", False):
                notif.comment.author = notif.comment.user
                notif.comment.author.mention = "@" + notif.comment.author.username
                notif.comment.Image = lambda url, caption="": f"![{caption}]({url})"
                notif.comment.Link = lambda text, url: f"[{text}]({url})"
                for i in dir(self):
                    if not i.startswith("__") and not i.endswith("__"):
                        setattr(notif.comment, i, getattr(self, i))
                valid_first, parsed_json = await self.valid_command(notif.comment.body)
                if not valid_first:
                    return

                if (
                    "command" in parsed_json
                    and (
                        parsed_json["command"] in self.commands
                        or parsed_json["command"] in self.alias
                    )
                    and valid_first
                ):
                    c = parsed_json["command"]
                    if parsed_json["command"] in self.alias:
                        c = self.alias[c]
                    valid, kwargs = await self.get_kwargs(
                        self.commands[c], parsed_json["options"]
                    )
                    if valid and valid_first:
                        notif.comment.button = Button(notif.comment.author.username, c)

                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        if self.commands[c]["thread"]:
                            # t = Thread(
                            #     target=self.commands[c]["call"],
                            #     args=(notif.comment,),
                            #     kwargs=kwargs,
                            # )
                            # t.start()
                            # self.threads_.append(t)
                            await self.commands[c]["call"](notif.comment, **kwargs)
                        else:
                            await self.commands[c]["call"](notif.comment, **kwargs)
                    elif valid_first:
                        await self._not_all_required_params_specified(notif.comment)
                elif (
                    "command" in parsed_json
                    and (parsed_json["command"] in self.listeners)
                    and valid_first
                ):
                    c = parsed_json["command"]
                    valid, kwargs = await self.get_kwargs(
                        self.listeners[c], parsed_json["options"]
                    )
                    if valid and valid_first:
                        notif.comment.button = Button(notif.comment.user.username, c)
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        for command in self.listeners[c]:
                            if command[c]["thread"]:
                                # t = Thread(
                                #     target=command[c]["call"],
                                #     args=(notif.comment,),
                                #     kwargs=kwargs,
                                # )
                                # t.start()
                                # self.threads_.append(t)
                                await command[c]["call"](notif.comment, **kwargs)
                            else:
                                await command[c]["call"](notif.comment, **kwargs)
                    elif valid_first:
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsucessful: {red}Not all required params specified{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        await self._not_all_required_params_specified(notif.comment)
                elif "command" in parsed_json and valid_first:
                    logger.info(
                        f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsuccessful: {red}Invalid command{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                    )
                    await self._default(notif.comment)
            elif __typename == "AnnotationNotification":
                super_self = self

                class CurrentThread:
                    def __init__(self, data) -> None:
                        self.id = data["id"]
                        self.anchor_id = data["anchor"]["id"]
                        self.seen = data["seen"]
                        self.user = None

                        async def __temp_wrapper():
                            self.user = await super_self.users.fetch(
                                data["user"]["username"]
                            )

                        loop = asyncio.get_event_loop()
                        loop.create_task(__temp_wrapper())
                        self.body = data["content"]["text"]

                res = await self.gql(
                    "getReplAnnotations",
                    {"url": notif.url},
                )
                repl_annotations = res["repl"]
                if repl_annotations is None:
                    return
                anchor = list(
                    filter(
                        lambda x: x["isGeneral"], repl_annotations["annotationAnchors"]
                    )
                )[0]
                if not anchor:
                    return
                messages = list(map(lambda x: CurrentThread(x), anchor["messages"]))
                message = list(
                    filter(
                        lambda x: x.body.startswith("@" + self.user.username)
                        and not x.seen,
                        messages,
                    )
                )
                message = message[0]
                await self.gql(
                    "markMessageAsSeen",
                    {"replId": repl_annotations["id"], "anchorId": anchor["id"]},
                )

                class CurrentCtx:
                    def __init__(self):
                        self.repl_id = repl_annotations["id"]
                        self.anchor_id = anchor["id"]

                    async def reply(self, body) -> None:
                        return await self.gql(
                            "createChatMessage",
                            vars={
                                "replId": self.repl_id,
                                "anchorId": self.anchor_id,
                                "annotationMessage": {
                                    "id": str(uuid.uuid4()),
                                    "text": body,
                                },
                            },
                        )

                ctx = CurrentCtx()
                for i in dir(self):
                    if not i.startswith("__") and not i.endswith("__"):
                        setattr(ctx, i, getattr(self, i))
                for i in dir(message):
                    if not i.startswith("__") and not i.endswith("__"):
                        setattr(ctx, i, getattr(message, i))

                ctx.author = ctx.user
                ctx.author.mention = "@" + ctx.user.username
                valid_first, parsed_json = await self.valid_command(ctx.body)
                if not valid_first:
                    return

                if (
                    "command" in parsed_json
                    and (
                        parsed_json["command"] in self.commands
                        or parsed_json["command"] in self.alias
                    )
                    and valid_first
                ):
                    c = parsed_json["command"]
                    if parsed_json["command"] in self.alias:
                        c = self.alias[c]
                    valid, kwargs = await self.get_kwargs(
                        self.commands[c], parsed_json["options"]
                    )
                    if valid and valid_first:
                        ctx.button = Button(ctx.author.username, c)

                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        if self.commands[c]["thread"]:
                            # t = Thread(
                            #     target=self.commands[c]["call"],
                            #     args=(notif.comment,),
                            #     kwargs=kwargs,
                            # )
                            # t.start()
                            # self.threads_.append(t)
                            await self.commands[c]["call"](ctx, **kwargs)
                        else:
                            await self.commands[c]["call"](ctx, **kwargs)
                    elif valid_first:
                        await self._not_all_required_params_specified(ctx)
                elif (
                    "command" in parsed_json
                    and (parsed_json["command"] in self.listeners)
                    and valid_first
                ):
                    c = parsed_json["command"]
                    valid, kwargs = await self.get_kwargs(
                        self.listeners[c], parsed_json["options"]
                    )
                    if valid and valid_first:
                        ctx.button = Button(ctx.user.username, c)
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        for command in self.listeners[c]:
                            if command[c]["thread"]:
                                # t = Thread(
                                #     target=command[c]["call"],
                                #     args=(notif.comment,),
                                #     kwargs=kwargs,
                                # )
                                # t.start()
                                # self.threads_.append(t)
                                await command[c]["call"](ctx, **kwargs)
                            else:
                                await command[c]["call"](ctx, **kwargs)
                    elif valid_first:
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsucessful: {red}Not all required params specified{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        await self._not_all_required_params_specified(ctx)
                elif "command" in parsed_json and valid_first:
                    logger.info(
                        f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsuccessful: {red}Invalid command{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                    )
                    await self._default(ctx)

        if flask_app is not None:
            Thread(
                target=serve,
                kwargs={"app": flask_app, "host": "0.0.0.0", "port": 8080},
                daemon=daemon,
            ).start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.user.notifications.startEvents())
