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

## Run from Source

in order to run from source you may need to create an executable using pyinstaller, this is because the images
used in the application depend on the temporary paths pyinstaller creates. To do this please run these commands in the project directory:

`pip install pyinstaller`

`pyinstaller --name=podman-gui --add-data active.png:. --add-data inactive.png:. --add-data podman.png:. --add-data down.png:. --add-data stylesheet.qss:. --onefile main.py`

then you can run either

`./dist/podman-gui`

or just execute the python file itself since the tmp directories have been created.
