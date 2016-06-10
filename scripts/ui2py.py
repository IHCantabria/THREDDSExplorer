import os
import sys
import subprocess as sp

def convert(ui_fn, py_fn):
    """Convert "ui_fn" .ui file, into .py file."""

    # Avoid path problem with Linux vs Windows:
    ui = normalize_path(ui_fn)
    py = normalize_path(py_fn)

    # Build convert command, and run it:
    if sys.platform.startswith('linux'):
        fmt = "pyuic4 {ui} -o {py}"
    else:
        fmt = "C:\Python27\Lib\site-packages\PyQt4\pyuic4.bat {ui} -o {py}"
    cmd = fmt.format(ui=ui, py=py)
    s = sp.Popen(cmd, shell=True)
    s.communicate()

    # Remove some unwanted comments:
    with open(py) as f:
        content = f.read()

    with open(py, "w") as f:
        for line in content.split("\n"):
            if not "Form implementation generated" in line:
                f.write(line+"\n")

def normalize_path(mypath):
    """Take a unix-like path, normalize to current OS, and return it."""

    # Yes, the asterisk is correct:
    return os.path.join(*mypath.split("/"))


# Files to be processed:
fn_pairs = [
    [ "THREDDS_Explorer_dockwidget_base.ui", "THREDDS_Explorer_dockwidget.py" ],
    [ "libvisor/animation/Animation_add_others.ui", "libvisor/animation/Animation_add_others.py" ],
    [ "libvisor/animation/Animation_add_wcs_layer.ui", "libvisor/animation/Animation_add_wcs_layer.py" ],
    [ "libvisor/animation/Animation_add_wms_layer.ui", "libvisor/animation/Animation_add_wms_layer.py" ],
    [ "libvisor/animation/Animation_menu.ui", "libvisor/animation/Animation_menu.py" ],
    [ "libvisor/persistence/Server_Manager_Add_Server.ui", "libvisor/persistence/Server_Manager_Add_Server.py" ],
    [ "libvisor/persistence/Server_Manager.ui", "libvisor/persistence/Server_Manager_UI.py" ],
]

# Perform the processing:
for ui_fn, py_fn in fn_pairs:
    msg = "Processing UI file {ui}...".format(ui=normalize_path(ui_fn))
    print(msg)
    convert(ui_fn, py_fn)
