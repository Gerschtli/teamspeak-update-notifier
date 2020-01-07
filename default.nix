with import <nixpkgs> { };

python37.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "HEAD";

  src = builtins.filterSource
    (path: type: type != "directory" || baseNameOf path != "teamspeak_update_notifier.egg-info")
    ./.;

  propagatedBuildInputs = with python37Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with python37Packages; [
    pytest
    pytestrunner
  ];
}
