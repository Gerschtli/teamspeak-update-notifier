from notifier import commands


def test_login() -> None:
    message = commands.Login("username", "password")

    assert isinstance(message, commands.Command)
    assert not message.has_response
    assert message.command == "login"
    assert message.param("client_login_name") == "username"
    assert message.param("client_login_password") == "password"
    assert str(message) == "login client_login_name=username client_login_password=password"


def test_notify_register() -> None:
    message = commands.NotifyRegister()

    assert isinstance(message, commands.Command)
    assert not message.has_response
    assert message.command == "servernotifyregister"
    assert message.param("event") == "server"
    assert str(message) == "servernotifyregister event=server"


def test_quit() -> None:
    message = commands.Quit()

    assert isinstance(message, commands.Command)
    assert not message.has_response
    assert message.command == "quit"
    assert str(message) == "quit"


def test_send_message() -> None:
    message = commands.SendMessage("123", "text")

    assert isinstance(message, commands.Command)
    assert message.has_response
    assert message.command == "sendtextmessage"
    assert message.param("targetmode") == "1"
    assert message.param("target") == "123"
    assert message.param("msg") == "text"
    assert str(message) == "sendtextmessage targetmode=1 target=123 msg=text"


def test_use() -> None:
    message = commands.Use("654")

    assert isinstance(message, commands.Command)
    assert not message.has_response
    assert message.command == "use"
    assert message.param("sid") == "654"
    assert str(message) == "use sid=654"


def test_whoami() -> None:
    message = commands.Whoami()

    assert isinstance(message, commands.Command)
    assert message.has_response
    assert message.command == "whoami"
    assert str(message) == "whoami"
