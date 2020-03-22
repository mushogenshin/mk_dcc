import os
import maya.cmds as cmds

# USERPROFILE = "USERPROFILE"
USERNAME = "USERNAME"
DOCUMENTS = "Documents"
MAYA = "maya"
MODULES = "modules"
PREFS = "prefs"
PRESETS = "presets"

FILE_EXT = {"mayaAscii": "ma",
            "OBJexport": "obj",
            "ASS Export": "ass"}

FBX_PLUGIN_NAME = "fbxmaya"
OBJ_EXPORT_PLUGIN_NAME = "objExport"
MATRIX_NODES_PLUGIN_NAME = "matrixNodes"
MASH_PLUGIN_NAME = "MASH"

DDCONVEXHULL_PLUGIN_NAME = "DDConvexHull"
MATERIALPICKER_PLUGIN_NAME = "materialPicker"
SEAMSEASY_PLUGIN_NAME = "seamsEasy"
BOOL_PLUGIN_NAME = "bool"
ARNOLD_PLUGIN_NAME = "mtoa"

INITIALSHADINGGROUP = "initialShadingGroup"

MAYA_VERSIONS = ["2016", "2016.5", "2017", "2018", "2019"]

MAYA_DEFAULT_CONTENT_PATH = ['C:/Program Files/Autodesk/Maya2018/Examples',
                             'C:/Program Files/Autodesk/Bifrost/Maya2018/examples/Bifrost_Fluids',
                             'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/MASH Examples',
                             'C:/Program Files/Autodesk/Maya2018/plug-ins/MASH/Smart Presets']

unique_prefix = 'mnT2'

# SERVER FOLDERS VARIABLES SETUP

repo_lib_path = "//vietsap002/projects/ILM/lib"
dev_path = "D:/Hoan/LIBRARY/CG/maya/miniTools2_local/source"

script_folder_name = "scripts"
mnT2_folder_name = "miniTools2"
mnT2_icon_folder_name = "icons"
mnT2_source_folder_name = "source"
mel_folder_name = "mel_scripts"

znT_folder_name = "ziniTools"
znT_batch_file_name = "ziniTools_run.bat"

vsTools1_folder_name = "vsTools1"
vsTools1_ui_file = "vsTools1UI.ui"

mel_glob_string = "\\*.mel"
tool_meshes_folder_name = "tool_meshes"
instructions_folder_name = "_instructions"

repo_tools_folder_name = "TOOLS"
repo_softwares_folder_name = "SOFTWARES"
repo_maya_tools_folder_name = "maya"
repo_exchange_folder_name = "exchange"
current_username = os.environ[USERNAME]

vmtb_folder_name = "virtuos"
cgm_tools_folder_name = "cgm"
croquet_tools_folder_name = "florian.croquet"
chaumette_tools_folder_name = "adnan.chaumette"
chaumette_qpipe_file_name = "LaunchQuickPipe.mel"
korol_tools_folder_name = "henry.korol"
korol_local_tools_file_name = "mnT2_HKLocalTools.mel"
ingo_tools_folder_name = "ingo.clemens"
jirka_tools_folder_name = "stepan.jirka"
perform_file_drop_folder_name = "randall.hess"
perform_file_drop_script_name = "performFileDropAction.mel"
zen_tools_folder_name = "zen"
escribano_tools_folder_name = "brian.escribano"
wu_tools_folder_name = "joe.wu"
comet_tools_folder_name = "comet"


ninjadojo_tools_path = "//vietsap002/projects/ILM/lib/TOOLS/ninjadojo/"
ninjadojo_script_path = "//vietsap002/projects/ILM/lib/TOOLS/ninjadojo/Ninja_Dojo.mel"

# CONTENT BROWSER PATHS

repo_kitbash_path = "//vietsap002/projects/ILM/lib/MODEL/KITBASH"
repo_kitbash_folder_name = repo_kitbash_path.rpartition("/")[-1]
repo_env_path = "//vietsap002/projects/ILM/lib/MODEL/ENVIRONMENT"
repo_env_folder_name = repo_env_path.rpartition("/")[-1]
repo_costume_path = "//vietsap002/projects/ILM/lib/MODEL/COSTUME"
repo_costume_folder_name = repo_costume_path.rpartition("/")[-1]
repo_char_path = "//vietsap002/projects/ILM/lib/MODEL/CHARACTERS"
repo_char_folder_name = repo_char_path.rpartition("/")[-1]
repo_creature_path = "//vietsap002/projects/ILM/lib/MODEL/ANIMALS_CREATURES"
repo_creature_folder_name = repo_creature_path.rpartition("/")[-1]
repo_hda_path = "//vietsap002/projects/ILM/lib/HDA"
repo_hda_folder_name = repo_hda_path.rpartition("/")[-1]

VSTOOLS2_MAYA_SCRIPT_PATH = "C:/vsTools2/develop/maya/script"

QUICK_MA_TO_ZB_FILE = "C:/temp/znT_exported.ma"
QUICK_ZB_TO_MA_FILE = "C:/temp/zzz.fbx"

SOFTWARES = {"HairStrand_Designer": ("HairStrand_Designer/v1.287", "HairStrand_Designer_v1.287.exe"),
             "Materialize": ("Materialize/v1.78", "Materialize.exe")}

hsd_sample_set_folder_name = "SampleSet"

CAM_CLIP_PLANE_DIST = {"small": (0.09, 500), "medium": (0.9, 5000), "large": (9, 50000)}

############################################################################

# LOCAL FOLDERS VARIABLES SETUP

user_home_path = os.environ['HOME']  # C:/Users/%USERNAME%/Documents
user_maya_app_dir = os.environ['MAYA_APP_DIR']  # C:/Users/%USERNAME%/Documents/maya

temp_folder_name = "_temp"
gpu_cache_folder_name = "GPU_cache"
ma_separately_folder_name = "export_MA_separate"
obj_separately_folder_name = "export_OBJ_separate"
fbx_separately_folder_name = "export_FBX_separate"
# textures_folder_name = "textures"

############################################################################

znT_script_path = os.path.join(repo_lib_path, script_folder_name, znT_folder_name)
# \\vietsap002\projects\ILM\lib\scripts\ziniTools\source
znT_source_path = os.path.join(znT_script_path, mnT2_source_folder_name)
znT_batch_file_path = os.path.join(znT_source_path, znT_batch_file_name)

# //vietsap002/projects/ILM/lib/scripts/miniTools2
mnT2_script_path = os.path.join(repo_lib_path, script_folder_name, mnT2_folder_name)

# //vietsap002/projects/ILM/lib/scripts/miniTools2/modules
mnT2_source_modules_folder_path = os.path.normpath(os.path.join(mnT2_script_path, MODULES))

mnT2_source_prefs_folder_path = os.path.normpath(os.path.join(mnT2_script_path, PREFS))

mnT2_source_presets_folder_path = os.path.normpath(os.path.join(mnT2_script_path, PRESETS))

# //vietsap002/projects/ILM/lib/scripts/miniTools2/icons
mnT2_source_icon_folder_path = os.path.join(mnT2_script_path, mnT2_icon_folder_name)

############################################################################

# MEL SCRIPTS GLOB STRINGS

# //vietsap002/projects/ILM/lib/scripts/miniTools2/source/mel_scripts
mnT2_mel_essentials_server_folder_path = os.path.join(mnT2_script_path, mnT2_source_folder_name, mel_folder_name)
mnT2_mel_essentials_server_files_glob_string = mnT2_mel_essentials_server_folder_path + mel_glob_string

# D:/Hoan/LIBRARY/CG/maya/miniTools2_local/source/mel_scripts
mnT2_mel_essentials_local_files_glob_string = os.path.join(dev_path, mel_folder_name) + mel_glob_string

# OLD MEL FROM ILM VSTOOLS1

# //vietsap002/projects/ILM/lib/scripts/miniTools2/source/vsTools1/mel_scripts
vsTools1_mel_server_folder_path = os.path.join(mnT2_script_path, mnT2_source_folder_name,
                                               vsTools1_folder_name, mel_folder_name)
vsTools1_mel_server_files_glob_string = vsTools1_mel_server_folder_path + mel_glob_string


# D:/Hoan/LIBRARY/CG/maya/miniTools2_local/source/vsTools1/mel_scripts
vsTools1_mel_local_files_glob_string = os.path.join(dev_path, vsTools1_folder_name,
                                                    mel_folder_name) + mel_glob_string


# ILM VSTOOLS1 UI FILE

# //vietsap002/projects/ILM/lib/scripts/miniTools2/source/vsTools1UI.ui
vsTools1_ui_server_file_path = os.path.join(mnT2_script_path, mnT2_source_folder_name, vsTools1_ui_file)

# D:/Hoan/LIBRARY/CG/maya/miniTools2_local/source/vsTools1UI.ui
vsTools1_ui_local_file_path = os.path.join(dev_path, vsTools1_ui_file)

# //vietsap002/projects/ILM/lib/scripts/miniTools2/tool_meshes
tool_meshes_path = os.path.join(mnT2_script_path, tool_meshes_folder_name)

# //vietsap002/projects/ILM/lib/scripts/miniTools2/_instructions
mnT2_instructions_path = os.path.join(mnT2_script_path, instructions_folder_name)


repo_tools_path = os.path.join(repo_lib_path, repo_tools_folder_name, repo_maya_tools_folder_name)
repo_softwares_path = os.path.join(repo_lib_path, repo_softwares_folder_name)
repo_exchange_path = os.path.join(repo_lib_path, repo_exchange_folder_name)

cgm_tools_path = os.path.join(repo_tools_path, cgm_tools_folder_name)
vmtb_tools_path = os.path.join(repo_tools_path, vmtb_folder_name)
croquet_tools_path = os.path.join(repo_tools_path, croquet_tools_folder_name)
chaumette_qpipe_file_path = os.path.join(repo_tools_path, chaumette_tools_folder_name, chaumette_qpipe_file_name)
korol_local_tools_file_path = os.path.join(repo_tools_path, korol_tools_folder_name, korol_local_tools_file_name)
perform_file_drop_script_source_path = os.path.join(repo_tools_path,
                                                    perform_file_drop_folder_name,
                                                    perform_file_drop_script_name)
zen_tools_path = os.path.join(repo_tools_path, zen_tools_folder_name)

ingo_tools_path = os.path.join(repo_tools_path, ingo_tools_folder_name)
ingo_mel_files_glob_string = ingo_tools_path + mel_glob_string

jirka_tools_path = os.path.join(repo_tools_path, jirka_tools_folder_name)

jirka_material_picker_mel_files_glob_string = os.path.join(jirka_tools_path, "materialPicker") + mel_glob_string
jirka_seams_easy_mel_files_glob_string = os.path.join(jirka_tools_path, "seamsEasy") + mel_glob_string

escribano_tools_path = os.path.join(repo_tools_path, escribano_tools_folder_name)
escribano_mel_files_glob_string = escribano_tools_path + mel_glob_string

wu_tools_path = os.path.join(repo_tools_path, wu_tools_folder_name)

comet_tools_path = os.path.join(repo_tools_path, comet_tools_folder_name)
comet_mel_files_glob_string = comet_tools_path + mel_glob_string

repo_tools_instructions_path = os.path.join(repo_tools_path, instructions_folder_name)
repo_softwares_instructions_path = os.path.join(repo_softwares_path, instructions_folder_name)

user_current_maya_version = cmds.about(q=True, v=True)
user_current_maya_script_path = os.path.join(user_maya_app_dir, 
                                             user_current_maya_version,
                                             script_folder_name)

# QICON PATH

hsd_icon_name = "HairStrand_Designer_30.png"
hsd_icon_path = os.path.join(mnT2_source_icon_folder_path, hsd_icon_name)

hsd_sample_set_path = os.path.join(repo_softwares_path,
                                   SOFTWARES["HairStrand_Designer"][0].partition("/")[0],
                                   hsd_sample_set_folder_name)

materialize_icon_name = "Materialize_30.png"
materialize_icon_path = os.path.join(mnT2_source_icon_folder_path, materialize_icon_name)

# STYLESHEET

text_align_left_ss = "text-align: left"
row_multi_btns_max_width = "max-width: 4em"
row_multi_btns_max_width_narrower = "max-width: 2.5em"
medium_btn_width = "max-width: 7em"
medium_btn_width2 = "max-width: 9em"

readme_btn_ss = "color: grey; background-color: rgb(40, 40, 40); max-width: 1em; padding: 4px"
folder_btn_ss = "max-width: 5em; padding: 3px"

red_btn_ss = "background-color: rgb(162, 59, 59)"
green_btn_ss = "color: black; background-color: rgb(119, 224, 119)"
blue_btn_ss = "color: white; background-color: rgb(79, 79, 225)"
terra_btn_ss = "color: black; background-color: rgb(255, 176, 109)"  # vmtb
dark_gold_btn_ss = "background-color: rgb(161, 120, 18)"  # (187, 146, 44)
yellow_green2_btn_ss = "color: black; background-color: rgb(167, 170, 87)"
brown_btn_ss = "background-color: rgb(55, 47, 42)"
evergreen3_btn_ss = "color: black; background-color: rgb(166, 201, 27)"
pink_btn_ss = "background-color: rgb(191, 74, 93)"
grey_pink2_btn_ss = "color: black; background-color: rgb(179, 165, 177)"
grey_blue2_btn_ss = "color: black; background-color: rgb(167, 165, 179)"
grey_green4_btn_ss = "color: black; background-color: rgb(182, 186, 180)"
deep_violet_btn_ss = "background-color: rgb(42, 0, 95)"
dark_btn_ss = "color: white; background-color: black"
sea_green5_btn_ss = "background-color: rgb(66, 143, 99)"
bordeaux_btn_ss = "background-color: rgb(138, 61, 61)"
croquet_btn_ss = "background-color: rgb(103, 138, 152)"

MODELING_UNRELATED_PLUGINS = ('hairPhysicalShader', 'lookdevKit', 'shaderFXPlugin', 'VectorRender',
                              'ik2Bsolver', 'ikSpringSolver', 'matrixNodes', 'quatNodes',
                              'invertShape', 'poseInterpolator',
                              'mayaCharacterization', 'mayaHIK', 'MayaMuscle',
                              'sceneAssembly', 'ATFPlugin',
                              'BifrostMain', 'bifmeshio', 'bifrostshellnode', 'bifrostvisplugin', 'MASH',
                              'CloudImportExport')
