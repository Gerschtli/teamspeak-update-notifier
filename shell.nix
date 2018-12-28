with import <nixpkgs> { };

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      mypy
      pycodestyle
      pyflakes
      pylint
      python-language-server
    ]);

  PYTHONDONTWRITEBYTECODE = 1;
})
