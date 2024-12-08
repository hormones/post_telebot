import os
import yaml
import logging
from base import util
from telegram.ext import (
    PicklePersistence,
    ApplicationBuilder,
)

__fs = open(os.path.join("config.yml"), "r", encoding="UTF-8")
__config: dict = yaml.safe_load(__fs)

BOT_TOKEN: str = util.get_config(__config, "bot_token")
APPROVE_CHANNEL: str = util.get_config(__config, "approve_channel")
DISPLAY_CHANNEL: str = util.get_config(__config, "display_channel")
DEBUG: bool = util.get_config(__config, "debug", False)
PROXY: dict = util.get_config(__config, "proxy", {})

_logging_format = "%(asctime)s %(name)s %(process)d %(filename)s:%(lineno)s %(levelname)s: %(message)s"
_logging_level = logging.DEBUG if DEBUG else logging.INFO
_logging_file = logging.FileHandler("appdata/post_telebot.log")
_logging_file.setLevel(_logging_level)
_logging_file.setFormatter(logging.Formatter(_logging_format))
logging.basicConfig(format=_logging_format, level=_logging_level)
logging.getLogger().addHandler(_logging_file)


def get_proxy():
    enabled = PROXY.get("enabled", False)
    type = PROXY.get("type", "http")
    host = PROXY.get("host", "")
    port = PROXY.get("port", "")
    username = PROXY.get("username", "")
    password = PROXY.get("password", "")
    if not enabled or host == "" or port == "":
        return None
    if username != "" and password != "":
        return f"{type}://{username}:{password}@{host}:{port}"
    return f"{type}://{host}:{port}"


_proxy_str = get_proxy()
logging.info(f"config loaded...")
logging.info(f"config --> bot_token: {BOT_TOKEN}")
logging.info(f"config --> approve_channel: {APPROVE_CHANNEL}")
logging.info(f"config --> display_channel: {DISPLAY_CHANNEL}")
logging.info(f"config --> debug: {DEBUG}")
logging.info(f"config --> proxy: {PROXY}")
logging.info(f"config --> resolved proxy: {_proxy_str}")


_pers = PicklePersistence("appdata/persistence")
# _defaults = Defaults(parse_mode="HTML", disable_notification=True)
_builder = ApplicationBuilder().token(BOT_TOKEN).persistence(_pers)
if _proxy_str is not None:
    _builder.proxy(_proxy_str)
APP = _builder.build()


async def init():
    logging.info(f"=== config initialized ===")


if __name__ == "__main__":
    logging.info("=== config main ===")
