from .errors import EmptyMessageError


class Message:
    _delimeter_param = " "
    _delimeter_kv = "="
    _encode_matrix = [
        ["\\", "\\\\"],
        ["/", r"\/"],
        [" ", r"\s"],
        ["|", r"\p"],
    ]

    def __init__(self, command, params=None):
        self._command = command
        self._params = params if params is not None else {}

    @staticmethod
    def build_from_string(message):
        if message == "":
            raise EmptyMessageError("empty message received")

        message_parts = message.split(Message._delimeter_param)
        command = message_parts.pop(0)

        params = {}
        for part in message_parts:
            splitted = part.split(Message._delimeter_kv, 1)

            key = splitted[0]
            value = None if len(splitted) == 1 else Message._decode(
                splitted[1])

            params[key] = value

        return Message(command, params)

    def command(self):
        return self._command

    def param(self, key):
        return self._params.get(key)

    @staticmethod
    def _decode(string):
        for (original, encoded) in Message._encode_matrix:
            string = string.replace(encoded, original)

        return string

    @staticmethod
    def _encode(string):
        for (original, encoded) in Message._encode_matrix:
            string = string.replace(original, encoded)

        return string

    def __repr__(self):
        encoded_params = [
            "".join([key, Message._delimeter_kv,
                     Message._encode(value)])
            for key, value in self._params.items()
        ]

        return Message._delimeter_param.join([self._command] + encoded_params)
