with import <nixpkgs> { };

python36.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "1.2.0";

  src = ./.;

  doCheck = false;

  propagatedBuildInputs = with python36Packages; [
    beautifulsoup4
    requests
  ];
}
