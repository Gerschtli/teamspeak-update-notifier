{
  description = "Sends update notifications to server admins for teamspeak server";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";

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
      packages.${system} = {
        default = package;
        ${name} = package;
      };

      apps.${system} = {
        default = app;
        ${name} = app;
      };

      overlays.default = final: prev: {
        ${name} = import ./. { pkgs = prev; };
      };

      devShells.${system}.default = import ./shell.nix { inherit pkgs; };
    };
}
