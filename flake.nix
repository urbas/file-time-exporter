{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, flake-utils, ... }: flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-linux" ] (system: with nixpkgs.legacyPackages.${system};
    let
      checkInputs = with python3.pkgs; [
        pytestCheckHook
      ];

      propagatedBuildInputs = with python3.pkgs; [
        click
        prometheus-client
        pyyaml
      ];

      devInputs = with python3.pkgs; [
        black
        flake8
        isort
        nodePackages.prettier
        nodePackages.pyright
        pip
        pkgs.parallel
        pytest
        pytest-cov
        pytest-watch
        types-pyyaml
      ];

      pkg = python3.pkgs.buildPythonApplication {
        pname = "file-time-exporter";
        version = "local";
        src = pkgs.nix-gitignore.gitignoreSource [] ./.;
        inherit checkInputs propagatedBuildInputs;
        pytestFlagsArray = ["-v" "tests"];
      };
    in {
      packages.default = pkg;
      devShells.default = pkg.overrideAttrs(oldAttrs: { nativeBuildInputs = oldAttrs.nativeBuildInputs ++ devInputs; });
    });
}
