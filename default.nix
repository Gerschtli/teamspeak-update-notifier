{ pkgs ? import <nixpkgs> { } }:

pkgs.python3.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "1.7.2";

  src = builtins.filterSource
    (path: type: type != "directory" || baseNameOf path != "teamspeak_update_notifier.egg-info")
    ./.;

  pyproject = true;
  build-system = with pkgs.python3Packages; [
    setuptools
  ];

  propagatedBuildInputs = with pkgs.python3Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with pkgs.python3Packages; [
    pytest
  ];
}
