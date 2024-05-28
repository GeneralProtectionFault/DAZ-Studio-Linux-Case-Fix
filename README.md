# DAZ Studio - Manage upper/lower case differences in library paths
### It is recommended at present that you zip up the library you are fixing before using this tool as a backup!
The tool can do this for you right now if checking the box and selecting a path for the .zip file at the top, which works fine, but you may want to zip it manually just because it's simple, and I have yet to create a proper display that it's working,
and it will typically say it's not responding (though it will be fine if you wait for it):

![image](https://github.com/GeneralProtectionFault/DAZ-Studio-Linux-Case-Fix/assets/29645865/5ee14868-4f0d-49ec-85fa-905d7034b64e)

While what this app does is not very destructive, I have not tried throwing every convoluted directory structure at it I can think of, so this is just a safety "undo" step.


When attempting to run DAZ Studio in Linux and using any assets that need to be installed manually, it's often problematic because upper & lower case is treated as identical in Windows, but not Linux.
Therefore, if you manually add an asset, depending on what the asset creator did regarding case, it may create "duplicate" folders (i.e. Daz 3D / DAZ 3D), which can create a mess when the intent was to merge the contents.

![image](https://github.com/GeneralProtectionFault/DAZ-Studio-Linux-Case-Fix/assets/29645865/c3b3ae90-c4ce-4230-a0be-70b1ca6d2c73)

This utility is designed to use the main DAZ library (typically: "My DAZ 3D Library"):

![image](https://github.com/GeneralProtectionFault/DAZ-Studio-Linux-Case-Fix/assets/29645865/0ec5550d-c70f-462a-b793-f6d7f21f29bd)


...as a "control."  Therefore, assuming you have your own libraries:

![image](https://github.com/GeneralProtectionFault/DAZ-Studio-Linux-Case-Fix/assets/29645865/608c2651-3633-4b95-b432-a5c63ec68d83)

So, this tool is designed to take in the path to the main library, and any user-created/other library you may have.  
### It's important to make sure you pick the "root" of each library or the comparison will be quite erroneous!
### Additionally, be sure to put in the full Linux path to each, not right-click and get the path from within DAZ.
### Running this in Linux, you will be using Lutris/Wine/Etc..., and DAZ Studio will only see the c_drive within the Wine environment that was created for it.

The directory structure of these libraries is usually recognizable, with folders such as these (you may have some or all of thes, be missing some, depending on what assets you have):

* data
* Environments
* People
* Props
* Runtime

### Save Paths to File
This button will take whatever you have selected in the path fields and save them to a .pkl (pickle) file in the working directory.  If this file exists, it will load them when the application is started.

### Fix Directories
Once you've got your main & user library paths confirmed, clicking this button will iterate over all the folders & subfolders of your user library.
#### A check is done here to make sure that the DAZ main library does not have any "duplicate" (case-only) folders.  Something is definitely off if this is the case and should be fixed manually.  More to the point, it removes the "control" for what the case should be.

Before comparing the name/case to the main library, it first looks for self-consistency, and that is actually more where there are typically issues, as it depends on what the asset creators do.
If, for example, the user library has these folders (at any level in the tree within the library):
* Daz 3D
* DAZ 3D

...If the same folder (in the same place in the tree hierarchy) exists in the main DAZ library, it will use that naming, and consolidate all the files into that folder.
If there is no corresponding folder in the main DAZ library, the files will be consolidated into the foler that has more objects in it (files or folders--treated the same in this calculation).

At the end, if the user library is self-consistent, a check is done against the main DAZ library notwithstanding, and that naming taken in case (ha!) of a difference.
