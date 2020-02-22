# Update APT
sudo apt update
# Install lxde
sudo apt install lxde
 # Manual config 
 # Choose US keyboard template.

XCLIENT=192.168.1.1:0.0

EXPORT DISPLAY=$XCLIENT
# For remote clients, Mesa's libGL prefers to use client-side software rendering and then transfer the rendered image to the server
# OpenGL (GLX)
EXPORT LIBGL_ALWAYS_INDIRECT=0

# startlxde