import json
import logging


class MyJSONEncoder(json.JSONEncoder):
    """
    json encoder
    """

    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        return super().default(obj)


class TelethonFilter(logging.Filter):
    """
    filter out telethon debug logs
    """

    def filter(self, record):
        return not (
            record.name.startswith("telethon") and record.levelno == logging.DEBUG
        )


class Post(object):
    """
    Post object
    """

    def __init__(
        self,
        id=None,
        from_id=None,
        message_id=None,
        message_ids=None,
        media_group_id=None,
        anonymous=1,
        approval_id=None,
        approver_id=None,
        approval_result=None,
        approval_reply_id=None,
        create_time=None,
    ):
        self.id: int = id
        # who send the post
        self.from_id: int = from_id
        # the first message id of the post
        self.message_id: int = message_id
        # the message id of the post, in case of album, it's the first message id
        self.message_ids: str = message_ids
        # the media group id of the post
        self.media_group_id: int = media_group_id
        # whether the post is anonymous
        self.anonymous: int = anonymous
        # the message id of post forwoard in the approval channel
        self.approval_id: int = approval_id
        # the approver id who approved the post
        self.approver_id: int = approver_id
        # the result of the approval, 1 for passed, 0 for rejected
        self.approval_result: int = approval_result
        # the message id of post forward in the approval group, which group linked to the approval channel
        self.approval_reply_id: int = approval_reply_id
        self.create_time: str = create_time
        self._message_ids_list: list = []

    @property
    def get_param(self):
        return f"{self.id}|{self.from_id}|{self.message_ids}|{self.offset}|{self.anonymous}"

    @property
    def get_message_ids(self) -> list:
        if not self._message_ids_list:
            numbers = [int(num) for num in self.message_ids.split(",") if num]
            numbers.sort()
            self._message_ids_list = numbers
        return self._message_ids_list

    @property
    def is_batch(self):
        return len(self.get_message_ids) > 1

    def __str__(self):
        return json.dumps(self.__dict__)

    def __json__(self):
        return json.dumps(self.__dict__)


class Chat(object):
    """
    Chat object
    """

    def __init__(self, chat_id, status=None, lang_code=None, create_time=None):
        self.chat_id = chat_id
        self.status = status
        self.lang_code = lang_code
        self.create_time: str = create_time

    def __str__(self):
        return json.dumps(self.__dict__)

    def __json__(self):
        return json.dumps(self.__dict__)
