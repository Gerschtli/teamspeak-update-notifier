with import <nixpkgs> { };

python36.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "HEAD";

  src = ./.;

  propagatedBuildInputs = with python36Packages; [
    beautifulsoup4
    requests
  ];

  checkInputs = with python36Packages; [
    pytest
  ];
}
