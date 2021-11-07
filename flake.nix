{
  description = "Sends update notifications to server admins for teamspeak server";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};

      package = import ./. { inherit pkgs; };

      name = package.pname;

      app = {
        type = "app";
        program = "${package}/bin/${name}";
      };
    in
    {
      defaultPackage.${system} = package;
      packages.${system}.${name} = package;

      defaultApp.${system} = app;
      apps.${system}.${name} = app;

      overlay.${system} = final: prev: {
        ${name} = import ./. { pkgs = prev; };
      };

      devShell.${system} = import ./shell.nix { inherit pkgs; };
    };
}
