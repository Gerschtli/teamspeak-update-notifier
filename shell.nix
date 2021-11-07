{ pkgs ? import <nixpkgs> { } }:

pkgs.mkShell {
  buildInputs = with pkgs.python39Packages; [
    beautifulsoup4
    requests

    pytest
    pytestrunner

    coverage
    isort
    mypy
    pycodestyle
    pyflakes
    #pylint is currently not compiling
    typing-extensions

    pkgs.nixpkgs-fmt
  ];

  PYTHONDONTWRITEBYTECODE = 1;
}
