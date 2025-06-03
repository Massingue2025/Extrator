{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.ffmpeg
    pkgs.git
  ];

  env = {
    PYTHON_LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
  };

  postInstall = ''
    pip install flask pillow torch torchvision realesrgan
  '';
}
