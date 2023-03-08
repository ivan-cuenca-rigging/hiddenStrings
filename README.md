# hiddenStrings #

<img alt="icon of the hiddenStrings project" height="128" src="/icons/hiddenStrings.png" width="128"/>

Here is where I'm going to store my rigging stuff

[go to GitHub to read the file more comfortably](https://github.com/ivan-cuenca-rigging/hiddenStrings)

If you want to support me with my open source development, you can leave a tip here. 

Thank you!

[![Support via PayPal](https://img.shields.io/badge/Donate-PayPal.Me-orange)](https://www.paypal.me/IvanCuencaRigging/)

--------------------------------------------

## DISCLAIMER ##

The tool is under development.

I have a full time job and this is a side project, I will attempt to address all issues outside work hours.

--------------------------------------------

## LICENSE ##

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

[![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

hiddenStrings © 2023 by Iván Cuenca Ruiz is licensed under Attribution-NonCommercial-ShareAlike 4.0 International. 

[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[LICENSE](https://github.com/ivan-cuenca-rigging/hiddenStrings/blob/main/LICENSE.md)

--------------------------------------------

## REQUIREMENTS ##

Maya 2023 

Python 3

--------------------------------------------

## INSTALLATION ##

1. Download the most current release or clone the repository. 

2. Rename main folder to `hiddenStrings`

3. Save the main folder in your maya folder:
   "C:\Users\userName\Documents\maya\2023\scripts"

4. Run this code in maya as python:

       import hiddenStrings

   This import will check if there is a userSetup.py in "C:\Users\userName\Documents\maya\2023\"

   If it exists it will edit the file and add the hiddenStrings imports.

   If it does not exist it will create a userSetup.py with the hiddenStrings imports .

If you don't want to auto create the userSetup.py or load the markingMenu, the hotkeys or the plugins you can set these
parameters to False in the `__init__.py`

--------------------------------------------

## Marking menu ##

Hold <kbd>Shift</kbd> + <kbd>Alt</kbd> + <kbd>Right click</kbd> to open the marking menu

<kbd>&uarr;</kbd> Shapes utils

<kbd>&#8598; </kbd> Skins utils

<kbd>&larr;</kbd> Connections utils

<kbd>&darr;</kbd> Tools

### Private features: ###

<kbd>&rarr;</kbd> Builder

--------------------------------------------

## HotKeys ##

Run this code in maya as python:

       hiddenStrings.import_hotkeys()

### Keys: ###

<kbd>Alt</kbd> + <kbd>P</kbd> &rarr; Print selection

#### Resets ####

<kbd>Alt</kbd> + <kbd>Q</kbd> &rarr; Reset all

<kbd>Alt</kbd> + <kbd>W</kbd> &rarr; Reset translate

<kbd>Alt</kbd> + <kbd>E</kbd> &rarr; Reset rotate

<kbd>Alt</kbd> + <kbd>R</kbd> &rarr; Reset scale

#### Toggles ####

<kbd>Alt</kbd> + <kbd>2</kbd> &rarr; Add to isolate

<kbd>Alt</kbd> + <kbd>3</kbd> &rarr; Toggle highlighting

<kbd>Alt</kbd> + <kbd>4</kbd> &rarr; Toggle X-Ray

<kbd>Alt</kbd> + <kbd>5</kbd> &rarr; Toggle wireframe

#### Windows ####

<kbd>N</kbd> &rarr; Node editor

<kbd>Alt</kbd> + <kbd>S</kbd> &rarr; Paint skin tool

--------------------------------------------

## SOCIAL NETWORKS ##
[GitHub](https://github.com/ivan-cuenca-rigging/)
[LinkedIn](https://www.linkedin.com/in/ivan-cuenca-ruiz/)
[Instagram](https://www.instagram.com/ivan_cuenca_rigging/)
