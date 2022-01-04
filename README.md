# Podman-GUI

This is a GUI for the container engine podman fully written in python. This project utilizes the podman-py bindings and PyQt, a graphics framework based on Qt, which is used to generate GUI's in C/C++.

# Files
This gui is built from a single script **main.py** and uses assets like **active.png** **stylesheet.qss** and so on to form the images and styling of the application. the .qss extension is particular to Qt, and is virtually identical to CSS. This allows you to customize your python Qt widgets as if it was HTML.

This mix of CSS styling with Python scripting makes PyQt a powerful GUI tool and allows for a small yet effective and quick application like podman-gui.

This application depends on the podman socket being active so before running please verify both the podman service and socket are running. If you find they are not running you can start them:

`systemctl --user start podman.service`
`systemctl --user start podman.socket`

## Download

you can download the rpm [here](podman-gui-1-1.x86_64.rpm) and run via the command line using `podman-gui`

if you receive an error relating to wayland and Qt being incompatible please `export QT_QPA_PLATFORM=xcb`
