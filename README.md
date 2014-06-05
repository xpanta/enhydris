iwidget_ntua
============

This is our first try in creating a modular iWidget installation.
The project is based on Enhydris platform (https://github.com/openmeteo/enhydris/).

Our purpose is to add each widget with its proper name (e.g. uc011, ec031, etc). There should be a README file in each widget app describing what the widget does.

IMPORTANT: There is an extra requirement. "Dickinson" which is not included in the requirements.txt. This is how to install it.

1. Downloaded Dickinson from https://github.com/openmeteo/dickinson
2. Unpacked it in your ~/tmp directory
3. run ./configure and make inside the new directory
4. sudo make install﻿ for system wide installation

(optional) You might need to add "export LD_LIBRARY_PATH=/usr/local/lib" in your .bashrc file for pthelma to find Dickinson
