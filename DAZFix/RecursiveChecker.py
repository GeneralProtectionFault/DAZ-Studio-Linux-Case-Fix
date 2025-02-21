from DAZFix.LibraryFix import log_to_ui
import os
import shutil


def fix_recursive(library_path):
    dupe_folders = []
    for (root, dirs, files) in os.walk(library_path, topdown=True):
        for dir in dirs:
            full_directory = os.path.join(root,dir)
            # if current_depth > previous_depth and os.path.basename(os.path.normpath(full_directory)) == previous_root_end_folder:
            if os.path.basename(os.path.normpath(root)) == os.path.basename(os.path.normpath(full_directory)):
                log_to_ui("WARNING: Folder appears to have been placed inside itself:")
                log_to_ui(f"Current full path: {full_directory}")

                # FIX #
                # Note the top-level folder
                # top_folder = root
                dupe_folder_name = os.path.basename(os.path.normpath(root))
                
                # Walk from this folder to find out how many matryoshka folders we have
                for (root2, dirs2, files2) in os.walk(root, topdown=True):
                    # Iterate over the directories for this level/root
                    for d in dirs2:
                        full_dir_path = os.path.join(root2,d)
                        # Mark dupe folders with the same name as the current ("parent") folder
                        if os.path.basename(os.path.normpath(d)) == dupe_folder_name:
                            # dupe_folders.append(full_dir_path)

                            if os.path.exists(full_dir_path):
                                # Check before the copy if there's a dupe within a dupe
                                dupe_folder_children = os.listdir(full_dir_path)
                                nest_within_nest = dupe_folder_name in dupe_folder_children

                                log_to_ui(f"Moving {full_dir_path} => {root}")
                                try:
                                    shutil.copytree(full_dir_path, root, dirs_exist_ok=True)
                                except Exception as e:
                                    log_to_ui(f"ERROR MOVING: {e}")
                                
                                # Only remove the directory if it's...a directory & empty
                                if os.path.isdir(full_dir_path):
                                    while nest_within_nest:
                                        full_dir_path = os.path.join(full_dir_path, dupe_folder_name)
                                        shutil.copytree(full_dir_path, root, dirs_exist_ok=True)
                                        dupe_folder_children = os.listdir(full_dir_path)
                                        nest_within_nest = dupe_folder_name in dupe_folder_children
                                    
                                    log_to_ui(f"Deleting copied folder: {full_dir_path}")
                                    shutil.rmtree(full_dir_path)  
                                else: 
                                    log_to_ui(f"Not a folder: {full_dir_path}, skipping........")
                                    return False
                                        
                            else:
                                log_to_ui(f"Can't move to {root}")
                                log_to_ui(f"Folder doesn't exist (already moved/deleted): {full_dir_path}")
                            
                            return False
        # Move CONTENTS of the dupes to the top folder, since we don't want to keep the folder itself.
        # If dupes were found, break the loop at this level of the directory tree, and start over.abs
        # if len(dupe_folders) > 0:
        #     # Check for case match
        #     # Merge
        #     for f in dupe_folders:
        #         if os.path.exists(f):
        #             log_to_ui(f"Moving {f} => {root}")
        #             try:
        #                 shutil.copytree(f, root, dirs_exist_ok=True)
        #                 # copy_tree(f, root)
        #             except Exception as e:
        #                 log_to_ui(f"ERROR MOVING: {e}")
        #             # Only remove the directory if it's...a directory & empty
        #             if os.path.isdir(f):
        #                 log_to_ui(f"Deleting empty folder: {f}")
        #                 shutil.rmtree(f)
        #         else:
        #             log_to_ui(f"Can't move to {root}")
        #             log_to_ui(f"Folder doesn't exist (already moved/deleted): {f}")
        #     return False
    return True


def check(library_path):
    complete = False
    counter = 1
    while not complete:
        log_to_ui(f"Checking {library_path} for recursive folders, iteration {counter}-------------------------------------------------------")
        complete = fix_recursive(library_path)
        counter += 1

    log_to_ui("Done fixing recursive folders!")
    