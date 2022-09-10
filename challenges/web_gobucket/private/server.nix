{ config, lib, pkgs, ... }:
let
  script = ''
echo 1 > /.CTF_START
echo "start" > start.log;
cd /home/task/
exec ./run.sh
  '';
in {
  environment.systemPackages = with pkgs; [
      vagrant
      python3
  ];
  boot.kernelModules = [ "kvm-intel" ];
  boot.extraModprobeConfig = "options kvm_intel nested=1";
  virtualisation.libvirtd.enable = true;

  services.nginx.enable = true;
  services.nginx.appendHttpConfig = ''
    error_log stderr;
    access_log syslog:server=unix:/dev/log combined;
  '';
  services.nginx.virtualHosts."gobucket.web.jctf.pro" = {
    locations."/" = {
      extraConfig = "proxy_set_header X-Real-IP $remote_addr;";
      proxyPass = "http://127.0.0.1:8080";
    };
  };

  systemd.services.ctf-start = {
    inherit script;
    path = [ pkgs.python3 pkgs.vagrant pkgs.procps pkgs.jq pkgs.gnused pkgs.curl pkgs.gnugrep pkgs.git pkgs.openssh pkgs.docker pkgs.docker-compose pkgs.coreutils pkgs.bash ];
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