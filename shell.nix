{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs.python311Packages; [
    beautifulsoup4
    requests

    pytest
    pytestrunner

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
