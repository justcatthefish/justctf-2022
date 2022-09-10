{ config, lib, pkgs, ... }:
let
  script = ''
echo 1 > /.CTF_START
echo "start" > start.log;
cd /home/task/
exec ./run.sh
  '';
in {
  security.apparmor.enable = true;
  security.apparmor.policies."foreigner".profile = builtins.readFile ./private/foreigner/foreigner-armor;
  security.apparmor.policies."foreigner".enforce = true;

  environment.systemPackages = with pkgs; [
      nerdctl
      buildkit
      apparmor-bin-utils
      apparmor-parser
      iptables
      tmux
  ];
  virtualisation.containerd.enable = true;

  systemd.services.buildkitd =  {
      enable = true;
      description = "buildkitd";
      wantedBy = [ "multi-user.target" ];
      after = [ "network.target" ] ;
      serviceConfig = {
          Type = "simple";
          ExecStart = "${pkgs.buildkit}/bin/buildkitd --oci-worker=false --containerd-worker=true";
          Restart = "on-failure";
      };
  };

  systemd.services.ctf-start = {
    inherit script;
    path = [ pkgs.nerdctl pkgs.buildkit pkgs.apparmor-bin-utils pkgs.apparmor-parser pkgs.iptables pkgs.procps pkgs.jq pkgs.gnused pkgs.curl pkgs.gnugrep pkgs.git pkgs.openssh pkgs.docker pkgs.docker-compose pkgs.coreutils pkgs.bash ];
    description = "Start ctf tasks on startup";
    wantedBy = [ "network-online.target" ];
    unitConfig = {
#      ConditionPathExists = "!/.CTF_START";
      After = [ "network-online.target" ];
      X-StopOnRemoval = false;
    };
    restartIfChanged = false;
    serviceConfig = {
      Type = "oneshot";
      RemainAfterExit = true;
    };
  };
}