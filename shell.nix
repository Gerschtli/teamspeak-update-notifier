with import <nixpkgs> { };

stdenv.mkDerivation {
  name = "teamspeak-update-notifier";

  src = ./.;

  buildInputs = with python36Packages; [
    python
    beautifulsoup4
    requests
  ];
}
