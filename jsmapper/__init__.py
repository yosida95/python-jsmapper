# -*- coding: utf-8 -*-


class JSONSchema:

    def __init__(self, title=None, description=None, default=None,
                 type=None, all_of=None, any_of=None, one_of=None, not_=None,
                 format=None):  # difinitions
        # metadata
        self.title = title
        self.description = description
        self.default = default

        # general validators
        self.type = type
        self.all_of = all_of
        self.any_of = any_of
        self.one_of = one_of
        self.not_ = not_

        # semantic validation
        self.format = format
