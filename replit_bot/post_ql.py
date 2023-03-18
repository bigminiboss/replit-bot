"""file that handles posting to replit graphql endpoint for queries and mutations"""

import json
from requests import Session
from typing import Dict, Any, List
from .queries import q
from .colors import green, end, purple, red, bold_green, bold_blue, blue
from time import sleep
import logging
import random
import os

logger: logging.Logger = logging.getLogger(__name__)
backup: str = "https://graphql-playground.pikachub2005.repl.co/"
endpoint: str = "https://replit.com/graphql"
headers: Dict[str, str] = {
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
number_convert: List[str] = ["1st", "2nd", "3rd"]
__reset_status_codes: List[int] = [429, 403, 520, 503, 502, 500]
s = Session()
s.headers.update(headers)


def post(
    connection: str,
    query: str,
    vars: Dict[str, Any] = {},
    raw: bool = False,
    retry_for_internal_errors: bool = True,
    __different_endpoint: str = None,
):
    """post query with vars to replit graph query language"""
    s.headers.update({"Cookie": f"connect.sid={connection}"})

    class InitialRequest:
        def __init__(self):
            self.status_code = 429
            self.text = ""

    req = InitialRequest()
    number_of_attempts = 0
    max_attempts = 7
    if __different_endpoint is None:
        __different_endpoint = endpoint
    while (
        req.status_code in __reset_status_codes or str(req.status_code).startswith("5")
    ) and number_of_attempts < max_attempts:  # only try 7 times
        current_endpoint = f"{__different_endpoint}?e={int(random.random() * 100)}"
        req = s.post(
            current_endpoint,
            json={"query": (query if raw else q[query]), "variables": vars},
        )
        if req.status_code in __reset_status_codes or str(req.status_code).startswith(
            "5"
        ):
            N_TH = (
                number_convert[number_of_attempts]
                if number_of_attempts < 3
                else str(number_of_attempts + 1) + "th"
            )
            logger.warning(
                f"{green}[FILE] POST_QL.py{end}\n{red}[WARNING]{end}\n{red}[STATUS CODE] {req.status_code}\n\t{red}[INFO]{end} You have been ratelimited\n\t{bold_blue}[SUMMARY]{end} Retrying query for the {N_TH} time (max retries is 5)"
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
        _text = req.text.strip("\n")
        if len(_vars) >= vars_max:
            _vars = _vars[: vars_max - 3] + "..."
        if len(_query) >= query_max:
            _query = _query[: query_max - 3] + "..."
        if len(_text) >= text_max:
            _text = _text[: text_max - 3] + "..."
        if req.status_code == 200:
            logger.info(
                f"{green}[FILE] POST_QL.py{end}\n{green}[INFO]{end} {bold_green}Successful graphql!{end}\n\t{blue}[SUMMARY]{end} queried replit's graphql with these query and vars.\n\t{purple}[EXTRA]{end}\n\t\t{bold_blue}[QUERY]{end} {query}\n\t\t{bold_blue}[VARS]{end}{_vars}\n\t\t{bold_blue}[RESPONSE]{end} {_text}\n\t\t{bold_blue}[IS RAW QUERY]{end} {raw}\n\t\t{bold_blue}[URL END POINT]{end} {current_endpoint}"
            )
        else:
            return logger.error(
                f"{red}[FILE] POST_QL.py{end}\n{red}[STATUS CODE] {req.status_code}\n\t{purple}[EXTRA]{end} {_text}\n\t\t{bold_blue}[QUERY]{end} {query}\n\t\t{bold_blue}[VARS]{end}{_vars}\n\t\t{bold_blue}[IS RAW QUERY]{end} {raw}\n\t\t{bold_blue}[URL END POINT]{end} {current_endpoint}\n\t\t{bold_blue}[RETRY]{end} {retry_for_internal_errors}"
            )
        res = json.loads(req.text)

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


gql = post
