# Copyright (c) ACSONE SA/NV 2018
# Distributed under the MIT License (http://opensource.org/licenses/MIT).

import ast
import logging
import os
from functools import wraps

from .pypi import MultiDistPublisher, RsyncDistPublisher, TwineDistPublisher

_logger = logging.getLogger("oca_gihub_bot.tasks")


def switchable(switch_name=None):
    def wrap(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            sname = switch_name
            if switch_name is None:
                sname = func.__name__

            if (
                BOT_TASKS != ["all"] and sname not in BOT_TASKS
            ) or sname in BOT_TASKS_DISABLED:
                _logger.debug("Method %s skipped (Disabled by config)", sname)
                return
            return func(*args, **kwargs)

        return func_wrapper

    return wrap


HTTP_HOST = os.environ.get("HTTP_HOST")
HTTP_PORT = int(os.environ.get("HTTP_PORT") or "8080")

GITHUB_SECRET = os.environ.get("GITHUB_SECRET")
GITHUB_LOGIN = os.environ.get("GITHUB_LOGIN")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_ORG = (
    os.environ.get("GITHUB_ORG") and os.environ.get("GITHUB_ORG").split(",") or []
)
GIT_NAME = os.environ.get("GIT_NAME")
GIT_EMAIL = os.environ.get("GIT_EMAIL")

ODOO_URL = os.environ.get("ODOO_URL")
ODOO_DB = os.environ.get("ODOO_DB")
ODOO_LOGIN = os.environ.get("ODOO_LOGIN")
ODOO_PASSWORD = os.environ.get("ODOO_PASSWORD")

BROKER_URI = os.environ.get("BROKER_URI", os.environ.get("REDIS_URI", "redis://queue"))

SENTRY_DSN = os.environ.get("SENTRY_DSN")

DRY_RUN = os.environ.get("DRY_RUN", "").lower() in ("1", "true", "yes")

# Coma separated list of task to run
# By default all configured tasks are run.
# Available tasks:
#  delete_branch,tag_approved,tag_ready_to_merge,gen_addons_table,
#  gen_addons_readme,gen_addons_icon,setuptools_odoo,merge_bot,tag_needs_review,
#  migration_issue_bot,whool_init,gen_metapackage
BOT_TASKS = os.environ.get("BOT_TASKS", "all").split(",")

BOT_TASKS_DISABLED = os.environ.get("BOT_TASKS_DISABLED", "").split(",")

GEN_ADDONS_TABLE_EXTRA_ARGS = (
    os.environ.get("GEN_ADDONS_TABLE_EXTRA_ARGS", "")
    and os.environ.get("GEN_ADDONS_TABLE_EXTRA_ARGS").split(" ")
    or []
)

GEN_ADDON_README_EXTRA_ARGS = (
    os.environ.get("GEN_ADDON_README_EXTRA_ARGS", "")
    and os.environ.get("GEN_ADDON_README_EXTRA_ARGS").split(" ")
    or []
)

GEN_ADDON_ICON_EXTRA_ARGS = (
    os.environ.get("GEN_ADDON_ICON_EXTRA_ARGS", "")
    and os.environ.get("GEN_ADDON_ICON_EXTRA_ARGS").split(" ")
    or []
)

GITHUB_STATUS_IGNORED = os.environ.get(
    "GITHUB_STATUS_IGNORED",
    "ci/runbot,codecov/project,codecov/patch,coverage/coveralls",
).split(",")

GITHUB_CHECK_SUITES_IGNORED = os.environ.get(
    "GITHUB_CHECK_SUITES_IGNORED", "Codecov,Dependabot"
).split(",")

MERGE_BOT_INTRO_MESSAGES = [
    "On my way to merge this fuckin PR, bitch!",
    "Let's merge this awesome bunch of brand new bugs!",
    "Ok, let's make yet another prod instance explode. Merging now.",
    "What a great day to merge new bugs. Let's do it!",
    "It was time you started writing some barely decent code, for Christ' sake. Merging it.",
    "Considering how you review code, not sure I can merge it. Let's try.",
    "Do you call this shit 'code'? Bah, let's merge and forget about it",
    "Better out than in, I always say! Merging now.",
    "What a disgusting pile of shit. Merging just because they force me to.",
    "Can't you merge it on your own? That's the 'abc'!",
    "Don't take it out on me when this crap goes prod. Merging now.",
    "What, seriously? Do you really want me to touch this shit? Bah, let's see what I can do",
    "Let's merge this stinking pile of crappy code",
    "Even my wife, Princess Fiona, could code better than you did. Bah, let's merge it anyway",
    "You talkin' to me? You talkin' to me? Then who the hell else are you talkin' to?",
    "SSSSSSSSSSSSSSSSMOKIN'!",
    "Well, let's not start sucking each other's dicks quite yet. Let's merge this stuff and call it a day, ok?",
    "Winter is coming. And a lot of bugs too. Merging now",
    "Merging now. That's thirty minutes away. I'll be there in ten.",
    "Wanna merge? Frankly, my dear, I don't give a damn.",
    "Asking Github to merge it. I'm going to make him an offer he can't refuse.",
    "May the Source be with you!",
    "I love the smell of bugs in the morning",
    "My name is Bot. Orco Bot. Merging your stuff.",
    "Talk is cheap, show me the code!",
    "You know how to merge, don't you Steve? You just put your branches together and blow.",
    "I'll be back.",
    "Code is like a box a chocolate. You never know what bug you're gonna get.",
    "Houston, we have a problem. This code sucks.",
    "HERE'S JOHNNY!",
    "A merge please. Shaken, not stirred.",
    "I'll do it. Sicchè!",
    "Is this a PR? Freechete!!!",
]

APPROVALS_REQUIRED = int(os.environ.get("APPROVALS_REQUIRED", "2"))
MIN_PR_AGE = int(os.environ.get("MIN_PR_AGE", "5"))

dist_publisher = MultiDistPublisher()
SIMPLE_INDEX_ROOT = os.environ.get("SIMPLE_INDEX_ROOT")
if SIMPLE_INDEX_ROOT:
    dist_publisher.add(RsyncDistPublisher(SIMPLE_INDEX_ROOT))
if os.environ.get("OCABOT_TWINE_REPOSITORIES"):
    for index_url, repository_url, username, password in ast.literal_eval(
        os.environ["OCABOT_TWINE_REPOSITORIES"]
    ):
        dist_publisher.add(
            TwineDistPublisher(index_url, repository_url, username, password)
        )

OCABOT_USAGE = os.environ.get(
    "OCABOT_USAGE",
    "**Ocabot commands**\n"
    "* ``ocabot merge major|minor|patch|nobump``\n"
    "* ``ocabot rebase``\n"
    "* ``ocabot migration {MODULE_NAME}``",
)

OCABOT_EXTRA_DOCUMENTATION = os.environ.get(
    "OCABOT_EXTRA_DOCUMENTATION",
    "**More information**\n"
    " * [ocabot documentation](https://github.com/OCA/oca-github-bot/#commands)\n"
    " * [OCA guidelines](https://github.com/OCA/odoo-community.org/blob/master/"
    "website/Contribution/CONTRIBUTING.rst), "
    'specially the "Version Numbers" section.',
)

ADOPT_AN_ADDON_MENTION = os.environ.get("ADOPT_AN_ADDON_MENTION")

MAINTAINER_CHECK_ODOO_RELEASES = (
    os.environ.get("MAINTAINER_CHECK_ODOO_RELEASES")
    and os.environ.get("MAINTAINER_CHECK_ODOO_RELEASES").split(",")
    or []
)

WHEEL_BUILD_TOOLS = os.environ.get(
    "WHEEL_BUILD_TOOLS",
    "build,pip,setuptools<70,wheel,setuptools-odoo,whool",
).split(",")

# minimum Odoo series supported by the bot
MAIN_BRANCH_BOT_MIN_VERSION = os.environ.get("MAIN_BRANCH_BOT_MIN_VERSION", "11.0")

# First Odoo Series for which the whool_init and gen_metapackage tasks are run on main
# branches. For previous versions, the setuptools_odoo task is run and generates
# setup.py instead of pyproject.toml.
GEN_PYPROJECT_MIN_VERSION = os.environ.get("GEN_PYPROJECT_MIN_VERSION", "17.0")
