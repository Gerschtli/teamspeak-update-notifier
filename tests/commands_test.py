from notifier import commands


def test_login() -> None:
    command = commands.Login("username", "password")

    assert isinstance(command, commands.Command)
    assert command.message.command == "login"
    assert command.message.param("client_login_name") == "username"
    assert command.message.param("client_login_password") == "password"
    assert str(command.message) == "login client_login_name=username client_login_password=password"


def test_notify_register() -> None:
    command = commands.NotifyRegister()

    assert isinstance(command, commands.Command)
    assert command.message.command == "servernotifyregister"
    assert command.message.param("event") == "server"
    assert str(command.message) == "servernotifyregister event=server"


def test_keep_alive() -> None:
    command = commands.KeepAlive()

    assert isinstance(command, commands.ConsumerCommand)
    assert command.message.command == "version"
    assert str(command.message) == "version"


def test_quit() -> None:
    command = commands.Quit()

    assert isinstance(command, commands.Command)
    assert command.message.command == "quit"
    assert str(command.message) == "quit"


def test_send_command() -> None:
    command = commands.SendMessage("123", "text")

    assert isinstance(command, commands.ConsumerCommand)
    assert command.message.command == "sendtextmessage"
    assert command.message.param("targetmode") == "1"
    assert command.message.param("target") == "123"
    assert command.message.param("msg") == "text"
    assert str(command.message) == "sendtextmessage targetmode=1 target=123 msg=text"


def test_use() -> None:
    command = commands.Use("654")

    assert isinstance(command, commands.Command)
    assert command.message.command == "use"
    assert command.message.param("sid") == "654"
    assert str(command.message) == "use sid=654"


def test_version() -> None:
    command = commands.Version()

    assert isinstance(command, commands.QueryCommand)
    assert command.message.command == "version"
    assert str(command.message) == "version"


def test_whoami() -> None:
    command = commands.Whoami()

    assert isinstance(command, commands.QueryCommand)
    assert command.message.command == "whoami"
    assert str(command.message) == "whoami"
