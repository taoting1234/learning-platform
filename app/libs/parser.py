class Parser:
    def __init__(
        self, name, type_, required=False, range_=None, enum=None, default=None
    ):
        self.name = name
        self.type = type_
        self.required = required
        self.range = range_ if range_ is not None else ()
        self.enum = enum if enum is not None else []
        self.value = default

    def check(self, raw):
        if raw is None and self.required:
            raise Exception("{}: cannot be empty".format(self.name))
        if raw is None:
            return
        try:
            self.value = self.type(raw)
        except Exception:
            raise Exception(
                "{}: {} cannot decode to {}".format(self.name, raw, self.type.__name__)
            )
        if self.range:
            if self.value < self.range[0] or self.value > self.range[1]:
                raise Exception(
                    "{}: {} not in range ({}, {})".format(
                        self.name, raw, self.range[0], self.range[1]
                    )
                )
        if self.enum:
            if raw not in self.enum:
                raise Exception(
                    "{}: {} not in enum {}".format(self.name, raw, self.enum)
                )
