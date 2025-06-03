{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.ffmpeg
    pkgs.python311Packages.flask
    pkgs.python311Packages.werkzeug
  ];
}
