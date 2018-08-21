class Message:
    delimeter_param = " "
    delimeter_kv = "="
    encode_matrix = [
        ["\\", "\\\\"],
        ["/", "\/"],
        [" ", "\s"],
        ["|", "\p"],
    ]

    def __init__(self, command, params={}):
        self.command = command
        self._params = params

    def build_from_string(message):
        if message == "":
            return None

        message_parts = message.split(Message.delimeter_param)
        command = message_parts.pop(0)

        params = {}
        for part in message_parts:
            splitted = part.split(Message.delimeter_kv, 1)

            key = splitted[0]
            value = None if len(splitted) == 1 else Message.decode(splitted[1])

            params[key] = value

        return Message(command, params)

    def decode(string):
        for (original, encoded) in Message.encode_matrix:
            string = string.replace(encoded, original)

        return string

    def encode(string):
        for (original, encoded) in Message.encode_matrix:
            string = string.replace(original, encoded)

        return string

    def param(self, key):
        return self._params[key]

    def __repr__(self):
        encoded_params = [
            "{}{}{}".format(key, Message.delimeter_kv, Message.encode(value))
            for key, value in self._params.items()
        ]
        return Message.delimeter_param.join([self.command] + encoded_params)
