"""
In Minecraft, you are allowed to interact with some text, e.g.,
a hyperlink to some URL, invoke a command, etc. To describe such
a string, Minecraft uses a json text. This module provides a class
for that purpose.
"""
import json
from nbtlib.tag import String


class TextBase:
    """
    The base class with some common methods
    """
    def dump(self):
        """dump to the json object used in minecraft"""
        return {"text": ""}

    def as_list(self) -> list:
        """
        Minecraft accepts a list of json objects. If you want to
        concatenate two text with different formats or hyperlinks,
        you have to use a list of json texts. Thus, we'd better
        provide some mechanism to turn a text into a list. Then,
        we can easily add multiple json text.
        """
        return []

    def json(self, indent=None, ensure_ascii=False) -> str:
        """to json string"""
        return json.dumps(self.dump(), ensure_ascii=ensure_ascii, indent=indent)

    def to_nbt_string(self):
        """to nbt string"""
        return String(self.json())

    def __str__(self):
        return self.json()

    def __add__(self, other):
        if isinstance(other, str):
            other = Text(other)
        l1 = self.as_list()
        l2 = other.as_list()
        return ListText(*l1, *l2)

    def __radd__(self, other):
        if isinstance(other, str):
            other = Text(other)
        return other + self


class Text(TextBase):
    """
    This class models the raw json text directly used by the class
    """
    def __init__(self, text):
        self.data = {
            "text": text
        }

    def dump(self):
        return self.data

    def as_list(self) -> list:
        return [self]

    def color(self, color):
        """set color"""
        self.data["color"] = color
        return self

    def bold(self, bold=True):
        """set bold"""
        self.data["bold"] = bold
        return self

    def italic(self, italic=True):
        """set italic"""
        self.data["italic"] = italic
        return self

    def insertion(self, text):
        """insertion"""
        self.data["insertion"] = text
        return self

    def click_event(self, action, value):
        """click_event"""
        self.data["clickEvent"] = {
            "action": action,
            "value": str(value),
        }
        return self

    def run_command(self, cmd):
        """run_command"""
        cmd = str(cmd)
        if not cmd.startswith('/'):
            cmd = '/' + cmd
        return self.click_event("run_command", cmd)

    def suggest_command(self, cmd):
        """suggest_command"""
        return self.click_event("suggest_command", cmd)

    def change_page(self, page):
        """change_page"""
        return self.click_event("change_page", page)

    def hover_event(self, action, context):
        """hover_event"""
        self.data["hoverEvent"] = {
            "action": action,
            "context": context
        }
        return self

    def hover_text(self, text):
        """hover_text"""
        return self.hover_event("show_text", text)


class ListText(TextBase):
    """
    A list of json text for different formats or hyperlinks.
    """
    def __init__(self, *texts: Text | str):
        self.texts = []
        for t in texts:
            if isinstance(t, str):
                t = Text(t)
            self.texts.append(t)

    def as_list(self) -> list:
        return self.texts

    def dump(self):
        return [x.dump() for x in self.texts]
