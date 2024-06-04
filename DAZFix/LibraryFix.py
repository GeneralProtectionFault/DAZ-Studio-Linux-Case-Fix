# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
import sys
import shutil
import zlib

import globals


def log_to_ui(text):    
    globals.ui_object.ui.txtEditLog.insertPlainText(text + "\n")

    # Scroll to the bottom after adding the log text
    scrollBar = globals.ui_object.ui.txtEditLog.verticalScrollBar()
    globals.ui_object.ui.txtEditLog.verticalScrollBar().setValue(scrollBar.maximum())


class HaltException(Exception): pass


def move_to_new_home(dupe_dirs_folder, dest_full_path, root):
    log_to_ui(f'Moving objects into {dest_full_path}')
    for item in dupe_dirs_folder:
        dupe_folder_path = os.path.join(root, item)
        
        # Don't do anything to the folder we're keeping!
        if dest_full_path in dupe_folder_path:
            # print(f"SKIPPING: {dupe_folder_path}")
            continue
        
        # Move the files into the chosen directory
        # subfolder_alone = os.path.basename(os.path.normpath(dupe_folder_path))
        # log_to_ui(f'Getting all objects within: {dupe_folder_path}')
        objects_within_folder = os.listdir(dupe_folder_path)
        
        for obj in objects_within_folder:
            source = os.path.join(dupe_folder_path, obj)
            destination = os.path.join(dest_full_path, obj)

            # If we're moving a folder, shutil will put the folder inside the "destination" if it does not exist.
            # However, if the destination folder already has that folder, it puts it INSIDE that folder, creating something like
            # TheFolder/Characters/Characters....FML
            if os.path.isdir(destination):
                if os.path.isdir(source):
                    for obj in os.listdir(source):
                        src = os.path.join(source, obj)
                        dest = os.path.join(destination, obj)
                        
                        if os.path.isdir(src):
                            log_to_ui(f'Moving FOLDER: {src} => {dest}')
                            shutil.copytree(src, dest, dirs_exist_ok=True)
                        else:
                            log_to_ui(f'Moving FILE: {src} => {dest}')
                            shutil.copy2(src, dest)
                        
            else:
                log_to_ui(f'Moving {obj} => {destination}')
                shutil.move(source, destination)

        # Now that all the files are moved out, delete the directory
        if os.path.exists(dupe_folder_path):
            log_to_ui(f'Removing folder: {dupe_folder_path}:')
            for obj in os.listdir(dupe_folder_path):
                # Indent to indicate objects within the folder that were removed (after being copied)
                log_to_ui("     " + obj)
            shutil.rmtree(dupe_folder_path)
        

def make_archive(source, destination):
        base = os.path.basename(destination)
        name = base.split('.')[0]
        format = base.split('.')[1]
        archive_from = os.path.dirname(source)
        archive_to = os.path.basename(source.strip(os.sep))
        shutil.make_archive(name, format, archive_from, archive_to)
        shutil.move('%s.%s'%(name,format), destination)



def fix_libraries(backup_first, backup_zip_path, daz_default_library_path, daz_user_library_path):
    log_to_ui("\nFixing libraries...")
    if globals.process_running:
        return

    globals.process_running = True

    default_path_directories = [x[0] for x in os.walk(daz_default_library_path)]
    default_lowered = [x.casefold() for x in default_path_directories]
    default_parent_dropped = [x.replace(daz_default_library_path,'') for x in default_path_directories]
    default_lowered_and_parent_dropped = [x.replace(daz_default_library_path,'').casefold() for x in default_path_directories]


    user_path_directories = [x[0] for x in os.walk(daz_user_library_path)]
    user_lowered = [x.casefold() for x in user_path_directories]
    user_parent_dropped = [x.replace(daz_user_library_path,'') for x in user_path_directories]
    user_lowered_and_parent_dropped = [x.replace(daz_user_library_path,'').casefold() for x in user_path_directories]

    user_library = os.walk(daz_user_library_path, topdown=True)

    # Backup all contents first if option enabled
    if backup_first:
        log_to_ui("Zipping up your library to backup... (May take a while)")
        make_archive(daz_user_library_path, os.path.join(backup_zip_path, "UserLibraryBackup.zip"))



    for (root, dirs, files) in user_library:
        for dir in dirs:
            full_directory = f'{root}/{dir}'
            user_dir_no_parent = full_directory.replace(daz_user_library_path,'')
            
            # If the path (without the base) of the user library matches the default library except for case...
            user_default_variance = user_dir_no_parent.casefold() in default_lowered_and_parent_dropped \
                and user_dir_no_parent not in default_parent_dropped
            
            # Get the path from the default library that corresponds to the user folder we're currently iterating over
            default_path_this_dir = root.replace(daz_user_library_path, daz_default_library_path)
            default_library_has_root_folder = os.path.isdir(default_path_this_dir)
            default_path_has_subfolder = False
            
            dupe_dirs_in_default_folder = list()
            # print(default_path_this_dir)
            # print(dir)
            if default_library_has_root_folder:
                dupe_dirs_in_default_folder = [x for x in os.listdir(default_path_this_dir) if dir.casefold() == x.casefold()]
                
                # Get the current subfolder in the case of the default library
                # Get the first item in the list - note that with the above check ^^^, we ensure there's only 1
                if dupe_dirs_in_default_folder:
                    default_subfolder_this_dir = dupe_dirs_in_default_folder[0]
                    default_fullpath_this_dir = os.path.join(default_path_this_dir, default_subfolder_this_dir)
                    default_path_has_subfolder = os.path.isdir(default_fullpath_this_dir)
                
                # if default_path_has_subfolder:
                #     print(f"DEFAULT LIBRARY SUBFOLDER: {default_fullpath_this_dir}")
        
            if len(dupe_dirs_in_default_folder) > 1:
                log_to_ui('----------------------ERROR-------------------------')
                log_to_ui('-----------The DEFAULT DAZ library has multiple folders with the same case!-----------')
                log_to_ui('This must be resolved first.  Please combine these manually into the desired case')
                log_to_ui('If the folder was created by DAZ\'s installer, it is recommended to choose the case of that folder')
                log_to_ui('The following folder is the one at issue:')
                log_to_ui(default_path_this_dir)
                raise HaltException(f"Stopping: DAZ default library has dupclicate folders!\n{default_path_this_dir}/{dir}")
            # else:
            #     log_to_ui("Main Library consistency check passed...")

            # Before addressing the mismatch to the default DAZ library, the user's library might well have another same-named, but different-cased, 
            # folder WITHIN that user library (common cause of the issue to begin with)
            # If that is the case, we should detect that and combine all the files into one folder, then remove the other (renaming as appropriate)
            dupe_dirs_in_this_folder = [x for x in os.listdir(root) if dir.casefold() == x.casefold()]
            # print(f'Dupe dirs length: {len(dupe_dirs_in_this_folder)}')
            if len(dupe_dirs_in_this_folder) >= 2:
                log_to_ui('\nMultiple folders w/ the same "Name" found in USER library:')
                log_to_ui(root)
                for dupe in dupe_dirs_in_this_folder:
                    log_to_ui(dupe)
                    
                # if dupe_dirs_in_default_folder:
                # If this comes back true, we know there's a folder w/ the same name, but different case when comparing the original DAZ vs. the user's library
                if user_default_variance and default_path_has_subfolder:
                    chosen_subdirectory = dupe_dirs_in_default_folder[0]
                    chosen_full_path = os.path.join(root, chosen_subdirectory)
                else:
                    log_to_ui(f'\nThere is no folder with this name in the default DAZ library: {os.path.join(root, dupe)}')
                    # If there are multiple folders in the user's library, but none in the DAZ default library, we need to pick, but can't use the name in the DAZ default directory
                    # First, here, create a dictionary that stores the subfolder name & the number of ojbects in it
                    dupe_subdirectories = dict()
                    log_to_ui("Fixing user-only library duplicate folder.  Consolidating into the folder with the most objects...")
                    for item in dupe_dirs_in_this_folder:
                        count = len(os.listdir(os.path.join(root, item)))
                        dupe_subdirectories[item] = count
                    
                    # Pick based on the directory with the largest # of items in it
                    chosen_sub_directory = list(dupe_subdirectories.keys())[list(dupe_subdirectories.values()).index(count)]
                    chosen_full_path = os.path.join(root, chosen_sub_directory)
                    
                move_to_new_home(dupe_dirs_in_this_folder, chosen_full_path, root)
            # else:
            #     log_to_ui("No User Library issues found...")
                    
                
            # If the USER library does not have multiple folders w/ the same name,
            # but there remains the difference between the default & user libraries
            # In this case, simply rename the directory to the case of the default library
            if len(dupe_dirs_in_this_folder) <= 1 and user_default_variance:
                log_to_ui(f"\nUser library is unique but does not match the DAZ default library...")
                log_to_ui(f'FOLDER: {root}')
                
                old_path = os.path.join(root, dir)
                new_path = os.path.join(root, dupe_dirs_in_default_folder[0])
                log_to_ui("RENAMING user library:")
                log_to_ui(f'OLD: {dir}')
                log_to_ui(f'NEW: {dupe_dirs_in_default_folder[0]}')
                
                # Here we just need to rename to the default case
                # This may have been addressed by the fix to the user's library above, so check...
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                
    globals.process_running = False
    log_to_ui("Complete!")
                
                    
                    
                    
                
                
                
                
    
