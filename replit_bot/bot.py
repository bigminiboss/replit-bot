"""file that stores the main bot runner code"""

import urllib.parse
import logging
import os
from .client import Client
from .links import links
from .html_default_templates import ORIGINAL_HTML, PARAM_BIO, HTML_LIST, BLOCKQUOTE
from typing import Callable as Function, Any, Dict, Tuple, get_type_hints, List
from flask import Flask, render_template, request
from waitress import serve
from threading import Thread
from time import sleep
from .param import Param
from .exceptions import NamesMustBeAlphanumeric, MustBeRunOnReplitForButtons
from .utils._uuid import random_characters
from .post_ql import post
from .colors import green, blue, purple, red, end, bold_green, bold_blue

app = Flask(__name__)
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


@app.route("/<command>/<user>/<choice>/<rand_chars>")
def _parse_button_commands(command, user, choice, rand_chars):
    global _started_buttons
    if request.headers["X-Replit-User-Name"] == "":
        return render_template(
            "index.html",
            html='<center><div><script authed="location.reload()" src="https://auth.util.repl.co/script.js"></script></div></center>',
        )
    if (
        command in _started_buttons
        and user in _started_buttons[command]
        and rand_chars in _started_buttons[command][user]
        and user == request.headers["X-Replit-User-Name"]
    ):
        _started_buttons[command][user][rand_chars] = choice
        return render_template(
            "index.html",
            html="<center><h1>your request has been processed, you can close this tab</h1></center>",
        )
    else:
        return render_template(
            "index.html", html="<center><h1>you cannot do this right now</h1></center>"
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

    def get_choice(self):
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
        allow_api: bool = False,
        create_docs: bool = True,
        api_path: str = "/api",
    ) -> None:
        if token is not None:
            super()
            super().__init__(token)
            self.init_ = True
        else:
            self.init_ = False

        def help_function(ctx, command):
            if command == "None":
                if links.docs is not None:
                    ctx.reply(f"See the docs there {links.docs}")
                else:
                    ctx.reply(
                        "This bot has not docs. You can check specific commands however"
                    )
            else:
                ctx.reply(f"description of command: {self.commands[command]['desc']}")

        def __current_default(ctx, *args, **kwargs):
            __current = "That is not a valid command."
            __current += (
                f" You can see the bot docs here {links.docs}"
                if links.docs is not None
                else ""
            )
            ctx.reply(__current)

        def __not_included_params(ctx, *args, **kwargs):
            __current = "please include all required params."
            __current += (
                f" You can check the bot docs here {links.docs}"
                if links.docs is not None
                else ""
            )
            ctx.reply(__current)

        self.commands = {
            "help": {
                "call": help_function,
                "desc": "See commands",
                "name": "help",
                "thread": False,
                "params": {"command": Param(required=False, default="None")},
            }
        }
        self._default = __current_default
        self._not_all_required_params_specified = __not_included_params
        self.token = token
        self.bio = bio
        self.prefix = prefix
        self.alias = {}
        self.listeners = {}
        self.threads_ = []
        self._call_when_followed = lambda ctx, person_who_followed: logger.info(
            f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} @{person_who_followed.username} followed bot"
        )
        self._allow_api = allow_api
        self._create_docs = create_docs
        if self._allow_api:

            @app.route(api_path, methods=["POST"])
            def _raw_api():
                kwargs = {"vars": {}, "raw": True}
                kwargs.update(request.json)
                return post(self.sid, kwargs["query"], kwargs["vars"], kwargs["raw"])

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

    def parse_command(self, command: str):
        """parses command

        `@Example-Bot /say message:hi!`
        ->
        ```
        {
            "options": {
                "message": "hi!"
            },
            "ping statement": "@Example-Bot",
            "command": "hello"
        }
        ```

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

    def valid_command(self, resp: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """validates command. Returns true if is valid `(True, parsed_json)` or false if not `(False, {'None': None})`"""
        if resp == {} or resp["comment"] == None:
            return (False, {"None": None})
        parsed = self.parse_command(resp["comment"]["body"])
        if (
            parsed == {}
            or parsed["ping statement"].strip("@") != self.user.username.lower()
        ):
            return (False, {"None": None})
        return (True, parsed)

    def get_kwargs(
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

    def create_docs(self) -> None:
        """automatically creates the documentation for the bot"""
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

        @app.route("/")
        def _() -> None:
            return render_template("index.html", html=html)

    def _delete_threads(self) -> None:
        """thread to always destroy threads"""
        while True:
            for i in self.threads_:
                i.join()
            sleep(5)

    def run(self, auto_create_docs: bool = True, token: str = None) -> None:
        """mainest runner code"""
        if token is not None and not self.init_:
            super()
            super().__init__(token)
            self.init_ = True

        def on_ready(client):
            logger.info(
                f'{green}[FILE] BOT.py{end}\n{bold_green}[STARTING BOT]{end} Botting "{bold_blue}{client.user.username}{end}"'
            )

        self.once("ready", on_ready)
        if auto_create_docs:
            self.create_docs()

        def _run(notif_id, notif) -> None:
            """main runner code"""
            # MentionedInPost, MentionedInComment, RepliedToComment, RepliedToPost, AnswerAccepted, MultiplayerJoinedEmail, MultiplayerJoinedLink, MultiplayerInvited, MultiplayerOverlimit, Warning, TeamInvite, TeamOrganizationInvite, Basic, TeamTemplateSubmitted, TeamTemplateReviewedStatus, Annotation, EditRequestCreated, EditRequestAccepted, ReplCommentCreated, ReplCommentReplyCreated, ReplCommentMention, Thread, NewFollower
            post(self.sid, "markOneAsRead", {"id": notif_id})
            __typename = getattr(notif, "__typename")
            if __typename == "WarningNotification":
                logger.critical(
                    f"{red}[FILE] BOT.py{end}\n{red}[INFO]{end} bot has been warned"
                )
            elif __typename == "NewFollowerNotification":
                self._call_when_followed(self, notif.creator)
            elif getattr(notif, "comment", False):
                notif.comment.author = notif.comment.user
                notif.comment.author.mention = "@" + notif.comment.author.username
                notif.comment.Image = lambda url, caption="": f"![{caption}]({url})"
                notif.comment.Link = lambda text, url: f"[{text}]({url})"
                for i in dir(self):
                    if not i.startswith("__") and not i.endswith("__"):
                        setattr(notif.comment, i, getattr(self, i))
                parsed_json = self.parse_command(notif.comment.body)
                if "command" in parsed_json and (
                    parsed_json["command"] in self.commands
                    or parsed_json["command"] in self.alias
                ):
                    c = parsed_json["command"]
                    if parsed_json["command"] in self.alias:
                        c = self.alias[c]
                    valid, kwargs = self.get_kwargs(
                        self.commands[c], parsed_json["options"]
                    )
                    if valid:
                        notif.comment.button = Button(notif.comment.author.username, c)

                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        if self.commands[c]["thread"]:
                            t = Thread(
                                target=self.commands[c]["call"],
                                args=(notif.comment,),
                                kwargs=kwargs,
                            )
                            t.start()
                            self.threads_.append(t)
                        else:
                            self.commands[c]["call"](notif.comment, **kwargs)
                    else:
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsucessful: {red}Not all required params specified{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        __current = "please include all required params."
                        __current += (
                            f" You can check the bot docs here {links.docs}"
                            if links.docs is not None
                            else ""
                        )
                        notif.comment.reply(__current)
                elif "command" in parsed_json and (
                    parsed_json["command"] in self.listeners
                ):
                    c = parsed_json["command"]
                    valid, kwargs = self.get_kwargs(
                        self.listeners[c], parsed_json["options"]
                    )
                    if valid:
                        notif.comment.button = Button(notif.comment.user.username, c)
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO] logging command{end}.\n\t{blue}[SUMMARY]{end} {green}command successful{end}\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        for command in self.listeners[c]:
                            if command[c]["thread"]:
                                t = Thread(
                                    target=command[c]["call"],
                                    args=(notif.comment,),
                                    kwargs=kwargs,
                                )
                                t.start()
                                self.threads_.append(t)
                            else:
                                command[c]["call"](notif.comment, **kwargs)
                    else:
                        logger.info(
                            f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsucessful: {red}Not all required params specified{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                        )
                        self._not_all_required_params_specified(notif.comment)
                elif "command" in parsed_json:
                    logger.info(
                        f"{green}[FILE] BOT.py{end}\n{green}[INFO]{end} logging command\n\t{blue}[SUMMARY]{end} unsuccessful: {red}Invalid command{end}.\n\t{purple}[EXTRA]{end} Requested command: {parsed_json['command']}"
                    )
                    self._default(notif.comment)

        self.on("notification", _run)
        self.user.notifications.startEvents()
        if auto_create_docs:
            serve(app, host="0.0.0.0", port=8080)
        else:
            while True:
                pass
