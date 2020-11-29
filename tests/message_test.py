from notifier.message import Message


def test_build_from_string() -> None:
    message = Message.build_from_string("login hello user=hans password=georg")

    assert message is not None
    assert message.command == "login"
    assert message.param("user") == "hans"
    assert message.param("password") == "georg"
    assert str(message) == "login hello user=hans password=georg"


def test_build_from_string_with_special_chars() -> None:
    message = Message.build_from_string(r"command payload=test\sx\\o\/x\p")

    assert message is not None
    assert message.command == "command"
    assert message.param("payload") == r"test x\o/x|"
    assert str(message) == r"command payload=test\sx\\o\/x\p"


def test_build_from_string_with_empty_message() -> None:
    message = Message.build_from_string("")

    assert message is None


def test_init() -> None:
    message = Message("login", {"user": "hans", "password": "georg"}, ["hello"])

    assert message is not None
    assert message.command == "login"
    assert message.param("user") == "hans"
    assert message.param("password") == "georg"
    assert str(message) == "login hello user=hans password=georg"


def test_init_with_special_chars() -> None:
    message = Message("command", {"payload": r"test x\o/x|"})

    assert message is not None
    assert message.command == "command"
    assert message.param("payload") == r"test x\o/x|"
    assert str(message) == r"command payload=test\sx\\o\/x\p"
