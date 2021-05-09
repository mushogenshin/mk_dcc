# Python 3

# Step 1: clone the private Git repo into `target_dir` below -- this is important to not include excessive .venv files
# Step 2: install to Maya (drag'n'drop .py file) from this folder to generate all .pyc files, as all .py files will be removed

from pathlib import Path
from distutils import dir_util

app_name = "setDressMaster"
target_dir = Path("E:/projects/mk_dcc_dist")
failed_to_remove = []


def remove_item(item_path, force_delete_dir_only=False, force_delete_file_only=False):
    if item_path.is_file():
        if not force_delete_dir_only:
            try:
                item_path.unlink()
            except Exception:
                failed_to_remove.append(item_path)
    elif item_path.is_dir():
        if not force_delete_file_only:
            try:
                # item_path.rmdir()
                dir_util.remove_tree(item_path.as_posix())
            except Exception:
                failed_to_remove.append(item_path)


if __name__ == "__main__":

    # delete init_venv_* files
    for i in target_dir.glob("*"):
        item_name = i.name
        if item_name.startswith("init_venv_") or \
            item_name.startswith(".gitignore") or \
                item_name == "setup.py" or \
                    item_name.startswith(".vscode"):
            remove_item(i)
            
    # delete the downloaded .venv3
    for i in target_dir.glob(".venv3"):
        remove_item(i)

    # delete the .egg-info
    for i in (target_dir / "src").glob("*"):
        if i.name.endswith(".egg-info"):
            remove_item(i)

    # delete install/* except maya
    for i in (target_dir / "install").glob("*"):
        if i.name != "maya":
            remove_item(i)

    # delete src/utils/blender
    for i in (target_dir / "src/utils").glob("blender"):
        remove_item(i)

    # delete src/utils/packaging
    for i in (target_dir / "src/utils").glob("packaging"):
        remove_item(i)

    # delete src/gui/stylesheets
    for i in (target_dir / "src/gui").glob("stylesheets"):
        remove_item(i)

    # delete src/gui/app/* except current app
    for i in (target_dir / "src/gui/app").glob("*"):
        if i.name != app_name:
            remove_item(i, force_delete_dir_only=True)

    # delete all the __pycache__ folders
    for i in target_dir.rglob("__pycache__"):
        remove_item(i)

    # delete docs of other apps
    for i in (target_dir / "docs").glob("*"):
        if i.name != app_name:
            remove_item(i)

    # delete docs/{app_name}/images
    for i in (target_dir / "docs/{}".format(app_name)).glob("images"):
        remove_item(i)

    # delete src/gui/app/{app_name}/rc
    for i in (target_dir / "src/gui/app/{}".format(app_name)).glob("rc"):
        remove_item(i)

    # delete all .ui files
    for i in target_dir.rglob("*.ui"):
        remove_item(i)

    # delete all batch folders
    for i in target_dir.rglob("batch"):
        remove_item(i)

    # delete all .py files except the install script
    for i in target_dir.rglob("*.py"):
        if ".venv2" in i.as_posix():
            continue
        if "install/maya/{}".format(app_name) in i.as_posix():
            continue
        if "ui_qt" in i.stem:
            continue
        if i.stem in ("control", "model"):
            continue
        remove_item(i)

    # delete all .md, .adoc, and .mod, files
    for i in target_dir.rglob("*.adoc"):
        remove_item(i)

    for i in target_dir.rglob("*.mod"):
        remove_item(i)

    for i in target_dir.rglob("*.md"):
        if i.stem == "README":
            remove_item(i)

    for i in failed_to_remove:
        print("Failed to remove: {}".format(i))
