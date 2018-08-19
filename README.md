# teamspeak update notifier

Do you ever came across the day when you could not connect to your own teamspeak server because of a version
incompatibility between server and client? If you did, this tool might help you to never feel this pain.

## What does it do?

Whenever a server admin connects to your server, the most recent released teampspeak server version will be fetched and
compared to the current installed version of teamspeak. If there is any discrepancy, the admin will get a nice little
private message like:
```
￼<17:56:47> "serveradmin from <ip>:<port>": Please update your server to version 3.0.0!
```

Pretty neat!

## What do I have to do?

You need `python3` with `beautifulsoup4` and `requests` packages installed.

Setup a config file like `config.ini.dist`. The options are described in comments in the sample config.

If the config is set up, simply run the following:
```sh
$ ./notifier.py "path/to/config.ini"
```

Or install the application [setuptools](https://pypi.org/project/setuptools/) (see `setup.py`).

### Nix support

For users of the [nix package manager](https://nixos.org/nix/) the `default.nix` can be used to build the package with
`nix-build`. The development environment can be configured with `nix-shell`.
