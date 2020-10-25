# Sector
A simple puzzle game made in pygame. Don't roast me for terrible code, this is my first time making a thing like this.

Trello: https://trello.com/b/ZUbwRU2V/sector


Some stuff if you wanna contribute:

## Tiles:



+  `00` is floor
  
+  `01` is block (wall)
  
+  `02` is pushblock (pushable block)
  
+  `03` is player
  
+  `04` is hole
  
+  `05` is exit

+  `06` is horizontal rails
  
  
  
## Files extensions:

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



# Level editor:

At the moment, level editor loads the file specified in code (so you can't load any other level without editing the code), and saves the file as "customLevel" + number of levels existing + 1 + the file extension (`.srlv`) so it won't overwrite an existing level file. To save the level press `s`, to change selected tile use mouse scroll wheel. Hopefully i will make it more user-friendly soon.
