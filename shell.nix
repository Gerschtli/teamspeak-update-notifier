let
  pkgs = let
    hostPkgs = import <nixpkgs> {};
    pinnedPkgs = hostPkgs.fetchFromGitHub {
      owner = "NixOS";
      repo = "nixpkgs";
      rev = "8f0bafcaff7744d3d489a4eed563eda76fc604f8";
      sha256 = "163bs9pfal6w0h94fr6jsd9cb1p1axc13rbzrqh6wiajkrhjir5c";
    };
    in import pinnedPkgs { };

  inherit (pkgs) python36Packages;
in

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs
    ++ (with python36Packages; [
      pycodestyle pyflakes pylint python-language-server
    ]);

  PYTHONDONTWRITEBYTECODE = 1;
})
