with import <nixpkgs> { };

let
  dependency-injector = python36Packages.buildPythonPackage rec {
    pname = "dependency-injector";
    version = "3.13.1";

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "0bmcgdfjavgxdzkb904q968ig1x44arvpj2m4rpm5nc9vhhgq43q";
    };

    propagatedBuildInputs = with python36Packages; [ six ];
  };
in

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
