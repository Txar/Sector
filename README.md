# Sector
A simple puzzle game made in pygame. Don't roast me for terrible code, this is my first time making a thing like this. Right now it's very broken and has almost no levels.
Trello: https://trello.com/b/ZUbwRU2V/sector
Uh... that's it.

Some stuff if you wanna contribute:

## Tiles:
  
+  `00` is floor
  
+  `01` is wall
  
+  `02` is block (pushable)
  
+  `03` is player
  
+  `04` is hole
  
+  `05` is exit
  
  
  
## Files extensions:

  `(generally, "sr" is "sector", "lv" is level, "gd" is game data)`

+  `.srlv` - sector level
  
+  `.srgd` - sector game data

## Installation guide

1. Create a virtual env

  ```
  python -m venv env
  ```

2. Activate virtual env

  ```
  source env/bin/activate
  ```

3. Install dependencies

  ```
  pip install -r requrements.txt
  ```

4. Run game or level editor

  ```
  python sector.py
  ```

  ```
  python levelEditor.py
  ```
