from typing import Dict, List, Optional, Tuple

from .errors import EmptyMessageError


class Message:
    _delimeter_param: str = " "
    _delimeter_kv: str = "="
    _encode_matrix: List[Tuple[str, str]] = [
        ("\\", "\\\\"),
        ("/", r"\/"),
        (" ", r"\s"),
        ("|", r"\p"),
    ]

    def __init__(self,
                 command: str,
                 value_params: Optional[Dict[str, str]] = None,
                 key_params: Optional[List[str]] = None) -> None:
        self._command = command
        self._value_params = {} if value_params is None else value_params
        self._key_params = [] if key_params is None else key_params

    @staticmethod
    def build_from_string(message: str) -> 'Message':
        if message == "":
            raise EmptyMessageError("empty message received")

        message_parts = message.split(Message._delimeter_param)
        command = message_parts.pop(0)

        value_params = {}
        key_params = []
        for part in message_parts:
            splitted = part.split(Message._delimeter_kv, 1)

            key = splitted[0]
            if len(splitted) == 1:
                key_params.append(key)
            else:
                value_params[key] = Message._decode(splitted[1])

        return Message(command, value_params, key_params)

    def command(self) -> str:
        return self._command

    def param(self, key: str) -> Optional[str]:
        return self._value_params.get(key)

    @staticmethod
    def _decode(string: str) -> str:
        for (original, encoded) in Message._encode_matrix:
            string = string.replace(encoded, original)

        return string

    @staticmethod
    def _encode(string: str) -> str:
        for (original, encoded) in Message._encode_matrix:
            string = string.replace(original, encoded)

        return string

    def __repr__(self) -> str:
        encoded_params = [
            "".join([key, Message._delimeter_kv,
                     Message._encode(value)])
            for key, value in self._value_params.items()
        ]

        params = [self._command] + self._key_params + encoded_params

        return Message._delimeter_param.join(params)
