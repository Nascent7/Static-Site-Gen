import os
import shutil 

def copy_static(src_dir, dest_dir):
    if os.path.exists(dest_dir) == False:
        os.mkdir(dest_dir)
    for entry in os.listdir(src_dir):
        full_src = os.path.join(src_dir, entry)
        full_dest = os.path.join(dest_dir, entry)
        if os.path.isdir(full_src):
            if not os.path.exists(full_dest):
                os.mkdir(full_dest)
            copy_static(full_src,full_dest)
        else:
            shutil.copy(full_src, full_dest)