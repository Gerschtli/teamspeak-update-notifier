with import <nixpkgs> { };

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      coverage
      mypy
      pylama
      python-language-server
    ]);

  PYTHONDONTWRITEBYTECODE = 1;
})
