with import <nixpkgs> { };

python36.pkgs.buildPythonPackage rec {
  pname = "teamspeak-update-notifier";
  version = "HEAD";

  src = ./.;

  propagatedBuildInputs = with python36Packages; [
    beautifulsoup4
    dependency-injector
    requests
  ];
}
