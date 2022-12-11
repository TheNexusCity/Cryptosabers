# Generate JSON

To generate the JSON file simply just open your terminal, navigate to directory containing
_"generate.js"_ and the run the command:

> node generate.js

This will automatically generate the JSON in the /randomizer directory so that the script will be ready to run

# Run Script

To run the script you must run the "run.bat" file, this can be done by just double clicking the file.

If it doesn't work or gives you an error in the console then you probably have to set
"blender.exe" as an enviroment variable on your system (it's annoying but it's the
simplest way to run blender python scripts from the console in background).

### HOW TO SET BLENDER AS AN ENVIROMENT VARIABLE:

1. Press the windows key on your keyboard (or click on the start button)
2. Search **"Environment Variables"** and press enter (or click on "edit the
   system enviroment variables")
3. In the advanced tab click on **"Environment Variables"**
4. Under the variables look for **"Path"** and double-click it.

   You should now see a window with a list of directories

5. Click on new and add the directory where your "blender.exe" file is located
   (usually it's in _"C:\Program Files\Blender Foundation\Blender 3.0"_ but make
   sure you select the right directory)

6. You should now be able to run the "run.bat" file in the project folder

Once you run the .bat file an /out folder should be created and the renders will
be saved there. For the script to work the files must be named as they are in the
folder I sent. So you should have:

- data.json
- main.py
- scene.blend

**NOTE:** if these files are named any differently or are not in the same folder as
the .bat file the you will get errors

### TROUBLESHOOTING: 

It is paramount that everything is uniformly named throughout the generate.js, main.py, obj_map.py, and scene.blend otherwise you will get errors

**KeyError:** item not included or improperly labeled in obj_map.py

**Object not found:** item improperly labeled in generate.js

