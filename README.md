iwidget_ntua
============

This is our first try in creating a modular iWidget installation.
The project is based on Enhydris platform (https://github.com/openmeteo/enhydris/).

Our purpose is to add each widget with its proper name (e.g. uc011, uc031, etc). There should be a README file in each widget app describing what the widget does.

## IMPORTANT: ##

There is an extra requirement. The library "Dickinson" which is not included in the requirements.txt. This is how to install it.

1. Download Dickinson from https://github.com/openmeteo/dickinson
2. Unpack it in your ~/tmp directory
3. run ./configure and make inside the new directory
4. sudo make install﻿ for system wide installation

(optional) You might need to add "export LD_LIBRARY_PATH=/usr/local/lib" in your .bashrc file for pthelma to find Dickinson

## Concerning the contents of this repository ##

 * enhydris: This is the core Enhydris app. Most of the functionality lies inside this application.
 * iwidget: This app includes some extra generic functionality regarding the iWIDGET project and it is coupled with the functionality which is necessary for **Use Case C_UC01.1: Obtain total water consumption and costs using real-time data from smart meters**. We have to uncouple this functionality and create a new app (see bellow).
 * tl: This app is necessary for iwidget to run. To be honest I don't know what it does. But it is needed. As soon as I know what it does. I will update this README.
 * uc011: This is an empty app, waiting for the extra functionality regarding **Use Case C_UC01.1** of iwidget to be put here.


