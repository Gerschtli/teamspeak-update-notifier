with import <nixpkgs> { };

mkShell {
  buildInputs = with python37Packages; [
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
  ];

  PYTHONDONTWRITEBYTECODE = 1;
}
