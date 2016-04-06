TGM - A Game Engine for Community Projects
==========================================

## Setup

This is a Python 3.4 application that requires Pyglet 1.2.4 to run.
The application is known run on Windows but theoretically should be
able to run on Linux / Mac given the correct setup (this has not been tested).

[Python 3.4](https://www.python.org/downloads/release/python-344/)   
[Pyglet 1.2.4](https://bitbucket.org/pyglet/pyglet/wiki/Download)

## Running

To run the test game simply run `main.py` with Python. A window should open with
a playground of objects demonstrating some of the engine's features.

To run unit tests go to the directory containing main.py and run the command
`python -m unittest` (or for whatever alias you gave Python). This runs
Python's unittest module which then searches for tests and finds the project's
tests. Do not run this from the `test` directory however as this will prevent the
unit tests from finding the rest of the project.

## Code Layout

* GameObject as well as the tags system can be found at `tgm/system/base.py`
* The OpenGL code can be found at `tgm/drivers/pyglet.py`
* The `tgm/engine` folder may be emptier than expected since in this project an
  engine is just a common bundle of other components and nothing fundamental.

Other than that the rest of the project's structure should be fairly obvious.
