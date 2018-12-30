with import <nixpkgs> { };

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      coverage
      mypy
      pycodestyle
      pyflakes
      pylint
      python-language-server
    ]);

  PYTHONDONTWRITEBYTECODE = 1;
})
