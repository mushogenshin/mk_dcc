import shutil
import logging as log

def commit():
    destination_folder = r"\\vietsap002\projects\ILM\lib\scripts\miniTools2\source"
    source_folder = r"D:\Hoan\LIBRARY\CG\maya\miniTools2_local\source"

    try:
        shutil.rmtree(destination_folder)
    except:
        log.info('Cannot delete.')
        pass

    try:
        shutil.copytree(source_folder, destination_folder)
    except:
        log.info('Cannot copy.')
        pass

    log.info('DONE.')

    return True