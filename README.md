ogdwien-converter - restructure OGD Vienna's bike route kml into a more organized format

GENERAL INFORMATION
===================
ogdwien-converter is a simple python script which reorganizes the bicycle route kml file
which is provided by the city of Vienna. Currently there are four different bicycle track
types:

- Radroute (Bicycle route; blue)
- Radfahren im Wald (Outdoor/Mountain bike track; green)
- Markierte Anlagen (Bicycle lane; orange)
- Getrennte Führung (Dedicated bicycle track; red)

In the original map they are not categorized and all types are drawn in the same color.
This scripts creates a folder for every type and assigns different colors for the
track types.

USAGE
=====

`ogdwien-converter.py input.kml output.kml'

REFERENCES
==========
- [Open Government Data - Radfahranlangen](http://data.wien.gv.at/katalog/radfahranlagen.html)
- [ogdwien-converter github page](https://github.com/zapster/ogdwien)

INSTALL
=======

Installation is not necessary. Just run the code as stated in the usage section.

REQUIREMENTS
============

- Python

BUGS
====

If you find a bug please open a new issue on the github page and feel free to
fork the project and fix it ;).

WARNINGS
========
The program is distributed WITHOUT ANY WARRANTY.

LICENSING INFORMATION
=====================
Copyright (C) 2012 Josef Eisl

ogdwien-converter is distributed under the GNU General Public license (see COPYING).

ogdwien-converter is written by 

- Josef Eisl

