with import <nixpkgs> { };

let
  dependency_injector = python36Packages.buildPythonPackage rec {
    pname = "dependency_injector";
    version = "3.13.1";

    src = fetchFromGitHub {
      owner = "ets-labs";
      repo = pname;
      rev = version;
      sha256 = "03cn4aanz6q28vy5946bpbmnpg25szzp0q3m4wk82ardw5j6x07i";
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
    dependency_injector
    requests
  ];
}
