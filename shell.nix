with import <nixpkgs> { };

let
  jedi = python36Packages.jedi.overrideAttrs (old: rec {
    pname = "jedi";
    version = "0.12.0";
    name = "${pname}-${version}";

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "1bcr7csx4xil1iwmk03d79jis0bkmgi9k0kir3xa4rmwqsagcwhr";
    };

    propagatedBuildInputs = [ parso ];
  });

  parso = python36Packages.parso.overrideAttrs (old: rec {
    pname = "parso";
    version = "0.2.1";
    name = "${pname}-${version}";

    src = python36Packages.fetchPypi {
      inherit pname version;
      sha256 = "0zvh4rdhv2wkglkgh0h9kn9ndpsw5p639wcwv47jn1kfp504lq7h";
    };
  });

  python-language-server = python36Packages.buildPythonPackage rec {
    pname = "python-language-server";
    version = "0.19.0";

    src = fetchFromGitHub {
      owner = "palantir";
      repo = "python-language-server";
      rev = version;
      sha256 = "0glnhnjmsnnh1vs73n9dglknfkhcgp03nkjbpz0phh1jlqrkrwm6";
    };

    doCheck = false;

    propagatedBuildInputs = with python36Packages; [
      jedi pluggy future autopep8 mccabe pycodestyle pydocstyle pyflakes rope yapf
    ];
  };
in

(import ./.).overrideDerivation (old: {
  name = old.pname;

  buildInputs = old.buildInputs ++ [
    python36Packages.pylint
    python-language-server
  ];

  PYTHONDONTWRITEBYTECODE = 1;
})
