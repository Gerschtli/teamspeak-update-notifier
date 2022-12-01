{ pkgs ? import <nixpkgs> { } }:

pkgs.python39.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "1.7.2";

  src = builtins.filterSource
    (path: type: type != "directory" || baseNameOf path != "teamspeak_update_notifier.egg-info")
    ./.;

  propagatedBuildInputs = with pkgs.python39Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with pkgs.python39Packages; [
    pytest
    pytest-runner
  ];
}
