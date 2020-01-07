with import <nixpkgs> { };

python37.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "HEAD";

  src = ./.;

  propagatedBuildInputs = with python37Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with python37Packages; [
    pytest
    pytestrunner
  ];
}
