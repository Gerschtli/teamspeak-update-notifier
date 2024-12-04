{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs.python3Packages; [
    beautifulsoup4
    requests

    pytest

    coverage
    isort
    mypy
    pycodestyle
    pyflakes
    pylint
    typing-extensions
    types-requests

    pkgs.nixpkgs-fmt
  ];

  PYTHONDONTWRITEBYTECODE = 1;
}
