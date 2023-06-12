{ pkgs ? import <nixpkgs> { } }:

pkgs.python311.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "1.7.2";

  src = builtins.filterSource
    (path: type: type != "directory" || baseNameOf path != "teamspeak_update_notifier.egg-info")
    ./.;

  propagatedBuildInputs = with pkgs.python311Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with pkgs.python311Packages; [
    pytest
    pytest-runner
  ];
}
