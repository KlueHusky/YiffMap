# YiffMap flake
# KlueHusky
# 02.01.2023

{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-22.11";
    flake-utils.url = "github:numtide/flake-utils";

    mach-nix.url = "github:davhau/mach-nix";
  };

  outputs = inputs: inputs.flake-utils.lib.eachDefaultSystem (system:
    let
      pythonVersion = "python38";

      pkgs = import inputs.nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };

      #  pythonEnv = inputs.mach.mkPython {
      #     python = pythonVersion;
      #     requirements = builtins.readFile ./requirements.txt;
      #   };

    in
    {
      inherit pkgs;

      devShells.default = pkgs.mkShell.override
        {
          stdenv = pkgs.stdenvNoCC;
        }
        {
          nativeBuildInputs = with pkgs; [
            (python38.withPackages
              (pkgs: with pkgs; [
                colorama
                pyyaml
                numpy
                scipy
                pip
                matplotlib
                # forceatlas2
                networkx
                #fa2
              ]))
          ];
          #export PYTHONPATH="${pythonEnv}/bin/python"
          #shellHook = ''
          #  export PYTHONPATH=.
          #  pip install -r requirements.txt
          #'';
        };

        # This is to expose the venv in PYTHONPATH so that pylint can see venv packages
        # PYTHONPATH=\$PWD/\${venvDir}/\${pythonPackages.python.sitePackages}/:\$PYTHONPATH
    });
}
