import os
import json
import subprocess
import math
from functools import partial

import unreal

LEVEL_SEQ_NAME = 'TurntableLevelSequence'

# Required total number of output images is 60
SEQ_DISP_RATE = 3  # fps
SEQ_LENGTH = 20  # in seconds
SEQ_TOTAL_FRAMES = 60  # multiple two numbers above

TT_CHANNELS = {'Rotation.Z': (0, 360)}

IMG_FORMAT = ('.jpg', unreal.ImageSequenceProtocol_JPG)
IMG_RESOLUTION = (1920, 1080)
FN_PADDING = 4

FIX_BLURRED_FRAME_RANGE = 1

_ASSET_TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
_UTILITY_BASE = unreal.GlobalEditorUtilityBase.get_default_object()
_TT_MOVIESCENECAPTURE = unreal.AutomatedLevelSequenceCapture()

_MAIN_ACTOR = None
_CINE_CAM_ACTOR = None  # to modify focus settings later

# Get the HDRIBackdrop class, a BlueprintGeneratedClass
try:
    _HDRI_BACKDROP_CLASS = unreal.EditorAssetLibrary.load_blueprint_class('/HDRIBackdrop/Blueprints/HDRIBackdrop')
except:
    # Module unreal does not log this somehow
    _HDRI_BACKDROP_CLASS = None

if not _HDRI_BACKDROP_CLASS:
    unreal.log_warning('HDRIBackdrop plugin might have NOT been loaded. Please check again before using STWookies Tools.')


class CUSTOM_CFG:
    _HUNTER_CUR_PROJ_ASSET_JSON_FP = 'C:/Temp/HUNTER_current_proj_asset.json'
    _VERSIONING_MODULE = 'C:/vsTools2/SPD/python/asset/tools/default_external_tools/RealTT/hunter_real_tt_versioning.py'

    _TT_ROOT_KEY = 'unreal_tt_root'
    _TT_WORKSPACE_KEY = 'unreal_tt_workspace'

    
def list_selection():
    return _UTILITY_BASE.get_selection_set()


def create_new_level_sequence(level_seq_name, level_seq_path):
    """
    Create a new level sequence in engine
    :parm str level_seq_path: e.g. '/Game'
    """
    level_seq_asset_path = '/'.join([level_seq_path, level_seq_name])

    # Delete current one if it exists
    found = unreal.find_asset(level_seq_asset_path)

    if found:
        unreal.log_warning('Asset "{}" already exists. Removing it...'.format(level_seq_asset_path))
        unreal.EditorAssetLibrary.delete_asset(level_seq_asset_path)
    
    # Create a new one
    unreal.log('Creating new "{}"'.format(level_seq_asset_path))

    return _ASSET_TOOLS.create_asset(
        asset_name=level_seq_name,
        package_path=level_seq_path,
        asset_class=unreal.LevelSequence,
        factory=unreal.LevelSequenceFactoryNew()
    )


def add_actor_to_sequence(target_sequence, actor, track_type):
    """
    Add one possessable actor to the target sequence
    """
    # Add actor
    seq_bind_proxy = target_sequence.add_possessable(actor)
    # Add track
    new_track = seq_bind_proxy.add_track(track_type)
    # Add section
    new_section = new_track.add_section()

    return seq_bind_proxy, new_track, new_section
    

def config_level_sequence(target_sequence, length, fps):
    """
    Set the frame rate, the playback & view range, for the sequence
    """
    # Set the frame rate, providing the numerator and denominator
    target_sequence.set_display_rate(unreal.FrameRate(fps, 1))
    # Set the range
    target_sequence.set_playback_end_seconds(length)
    target_sequence.set_view_range_end(length)    


def config_sequence_section(target_section, length):
    target_section.set_range_seconds(0, length)


def set_section_anim_key(target_section, channels_to_key, anim_range, interp=unreal.MovieSceneKeyInterpolation.LINEAR):
    """
    :param dict channels_to_key: {channel_name: (start_value, end_value)}
    :pararm tuple anim_range: start and end frame
    """
    
    # Only working on specified channel(s)
    section_channels = [channel for channel in target_section.get_channels() if channel.get_name() in channels_to_key.keys()]

    for channel in section_channels:
        values = channels_to_key[channel.get_name()]

        # first key
        channel.add_key(
            unreal.FrameNumber(anim_range[0]),
            values[0],
            interpolation=interp
        )

        # last key
        channel.add_key(
            unreal.FrameNumber(anim_range[1]),
            values[1],
            interpolation=interp
        )


def level_seq_setup_actor(level_seq, actor, length, channels, frames):
    
    # # # Doesn't work: Bring object to world origin
    # actor.set_actor_location(unreal.Vector(0, 0, 0), False, True)

    # Add the object Actor to the LevelSequence
    seq_bind_proxy, actor_track, actor_section = add_actor_to_sequence(
        level_seq, 
        actor, 
        unreal.MovieScene3DTransformTrack
    )

    # Set up the Section parameters for the object Actor
    config_sequence_section(actor_section, length)

    # Key the Section for object Actor
    set_section_anim_key(actor_section, channels, (0, frames))


def level_seq_setup_cam_cut(level_seq, length):
    # Create a CameraCut track
    master_cam_cut_track = level_seq.add_master_track(unreal.MovieSceneCameraCutTrack)  # 'MovieSceneTrack'
    master_cam_cut_section = master_cam_cut_track.add_section()

    # Set up the Section parameters for the CameraCut
    config_sequence_section(master_cam_cut_section, SEQ_LENGTH)

    # Create a Cinematic Camera
    cine_cam_seq_bind_proxy = level_seq.add_spawnable_from_class(unreal.CineCameraActor)
    # Store the Binding ID
    cine_cam_binding_id = level_seq.make_binding_id(cine_cam_seq_bind_proxy)

    # Add a Transform track and section for this Cinematic Camera
    cine_cam_track = cine_cam_seq_bind_proxy.add_track(unreal.MovieScene3DTransformTrack)
    cine_cam_section = cine_cam_track.add_section()
    config_sequence_section(cine_cam_section, SEQ_LENGTH)

    # Bind the CineCam to the Master CameraCut track
    master_cam_cut_section.set_camera_binding_id(cine_cam_binding_id)

    cine_cam_actor = cine_cam_seq_bind_proxy.get_object_template()  # Class 'CineCameraActor'

    return cine_cam_actor


def create_hdri_backdrop_actor(singleton=True):

    all_actors = tuple(unreal.EditorLevelLibrary.get_all_level_actors())  # convert from Array

    if singleton:
        # Delete all instances of the same type found, based on Actor name
        all_hdri_backdrop_actors = [actor for actor in all_actors if actor.get_name().find('HDRIBackdrop') != -1]
        for hdri_actor in all_hdri_backdrop_actors:
            unreal.EditorLevelLibrary.destroy_actor(hdri_actor)

    # Remove all the existing Skylight objects
    all_sky_light_actors = [actor for actor in all_actors if actor.get_name().find('SkyLight') != -1]
    for sky_light_actor in all_sky_light_actors:
            unreal.EditorLevelLibrary.destroy_actor(sky_light_actor)

    # Spawn the HDRI Backdrop actor
    return unreal.EditorLevelLibrary().spawn_actor_from_class(
        _HDRI_BACKDROP_CLASS, 
        unreal.Vector(0, 0, 0), 
        unreal.Rotator(0, 0, 0)
    )


def setup_hdri_backdrop(hdri_backdrop_actor):
    # Enable "Use Camera Projection"
    hdri_backdrop_actor.set_editor_property("UseCameraProjection", True)

    # C:\Epic Games\UE_4.24\Engine\Plugins\Runtime\HDRIBackdrop\Content\Textures
    # TODO: copy TextureCube.uasset to /HDRIBackdrop/Textures/ (?)

    # Clear the selection
    # unreal.EditorLevelLibrary.clear_actor_selection_set()
    unreal.EditorLevelLibrary.select_nothing()


def create_movie_capture(level_seq_path, output_path, img_format, res, asset_name, padding):
    """
    :param str level_seq_path:
    :param str output_path:
    """
    # Create the Settings object
    tt_MSC_settings = unreal.MovieSceneCaptureSettings()

    # Set the Settings parameters
    tt_MSC_settings.movie_extension = img_format[0]
    tt_MSC_settings.resolution = unreal.CaptureResolution(res[0], res[1])
    tt_MSC_settings.output_format = '{}'.format(asset_name) + '.{frame}'
    tt_MSC_settings.output_directory = unreal.DirectoryPath(output_path)
    tt_MSC_settings.zero_pad_frame_numbers = padding
    tt_MSC_settings.overwrite_existing = True

    # Create the Capture object
    tt_MovieSceneCapture = unreal.AutomatedLevelSequenceCapture()
    # Set the Capture Protocol
    tt_MovieSceneCapture.set_image_capture_protocol_type(img_format[1])

    # Update Capture object using the Settings object
    tt_MovieSceneCapture.settings = tt_MSC_settings
    # Set the LevelSequence for the Capture object
    tt_MovieSceneCapture.level_sequence_asset = unreal.SoftObjectPath(level_seq_path)

    return tt_MovieSceneCapture


def run_versioning_cmd(cfg, asset_token):

    cmd = 'C:/vsTools2/VsRunner.bat {} python3.7.0 {} {}'.format(asset_token['vsproject'],
                                                                cfg._VERSIONING_MODULE,
                                                                asset_token[cfg._TT_WORKSPACE_KEY])

    # print('VERSIONING CMD:', cmd)
    
    try:
        subprocess.call(cmd)
    except Exception as e:
        print('Failed to call versioning module due to {}'.format(e))
    else:
        print('Called versioning module successfully.')


def load_json(json_path, verbose=0):
    if not os.path.exists(json_path):
        json_dir = os.path.dirname(json_path)
        if not os.path.exists(json_dir):
            os.makedirs(json_dir)
        with open(json_path, 'w') as file:
            data = {}
            json.dump(data, file, indent=4, sort_keys=True)
    data_dict = {}

    with open(json_path) as file:
        data_dict = json.loads(file.read())
        if verbose:
            print('Loaded data from JSON successfully : {}'.format(json_path))
    return data_dict


def reread_json_py2(cfg):

    asset_token = load_json(cfg._HUNTER_CUR_PROJ_ASSET_JSON_FP)
    tt_root_dir = asset_token[cfg._TT_ROOT_KEY]

    if not os.path.exists(tt_root_dir):
        try:
            os.path.makedirs(tt_root_dir)
        except Exception as e:
            print('Unable to create folder {} due to: {}'.format(tt_root_dir, e))

    return asset_token, tt_root_dir


def setup_tt():
    """
    Setup the LevelSequence for turntable
    """
    global _MAIN_ACTOR, _CINE_CAM_ACTOR
    
    # Get selected object
    sel_objs = list_selection()  # an Array
    # Abort if nothing selected
    if sel_objs:
        # TODO: add support for multiple selected objects
        _MAIN_ACTOR = sel_objs[0]

        # Create and setup the HDRI Backdrop
        hdri_actor = create_hdri_backdrop_actor()
        setup_hdri_backdrop(hdri_actor)

        # Create a LevelSequence
        level_seq = create_new_level_sequence(LEVEL_SEQ_NAME, '/Game')
        # Set up the LevelSequence parameters
        config_level_sequence(level_seq, SEQ_LENGTH, SEQ_DISP_RATE)

        # Prepare the Camera Cut
        _CINE_CAM_ACTOR = level_seq_setup_cam_cut(
            level_seq, 
            SEQ_LENGTH
        )

        # Prepare the main Actor
        level_seq_setup_actor(
            level_seq, 
            _MAIN_ACTOR, 
            SEQ_LENGTH, 
            TT_CHANNELS, 
            SEQ_TOTAL_FRAMES
        )

        # Restore the object selection
        unreal.EditorLevelLibrary.set_selected_level_actors(sel_objs)
        
        # Automatically open the sequence
        # TODO: use UAssetEditorSubsystem instead (method below is deprecated)
        _ASSET_TOOLS.open_editor_for_assets([level_seq])

        # Doesn't update actual position and rotation of the piloted CineCam
        # Pilot the CineCamera to delegate user to adjust the camera composition
        # unreal.EditorLevelLibrary.pilot_level_actor(_CINE_CAM_ACTOR)

        return level_seq

    else:
        unreal.log_warning('Nothing selected. Please select at least one object and try again.')


def focus_cam_at_actor():
    """
    :param Actor actor:
    """
    global _MAIN_ACTOR
    
    # Could not get_actor_transform() of the global _CINE_CAM_ACTOR
    # Override this with user selection
    _CINE_CAM_ACTOR = list_selection()[0]

    unreal.log('_Main Actor: {}'.format(_MAIN_ACTOR))
    unreal.log('_Cinematic Camera: {}'.format(_CINE_CAM_ACTOR))

    if _MAIN_ACTOR and _CINE_CAM_ACTOR:
    
        horizon_dist = _CINE_CAM_ACTOR.get_horizontal_distance_to(_MAIN_ACTOR)
        half_vertical_dist = _CINE_CAM_ACTOR.get_vertical_distance_to(_MAIN_ACTOR) / 2
        approx_focus_dist = math.sqrt(math.pow(horizon_dist, 2) + math.pow(half_vertical_dist, 2))

        # unreal.log('__Horizontal distance: {}'.format(horizon_dist))
        # unreal.log('__Half Vertical distance: {}'.format(half_vertical_dist))
        unreal.log('__Approximated focus distance: {}'.format(approx_focus_dist))

        # Also can use get_cine_camera_component()
        _CINE_CAM_COMPONENT = _CINE_CAM_ACTOR.camera_component  # Class 'CineCameraComponent'

        # Create a CameraFocusSettings
        tt_CamFocusSettings = unreal.CameraFocusSettings()
        tt_CamFocusSettings.manual_focus_distance = approx_focus_dist

        # unreal.log('___CineCam Component: {}'.format(_CINE_CAM_COMPONENT))
        # unreal.log('___CamFocusSettings: {}'.format(tt_CamFocusSettings))

        # Apply the CameraFocusSettings to the CineCam component
        _CINE_CAM_COMPONENT.focus_settings = tt_CamFocusSettings


def export_tt(cfg=CUSTOM_CFG, level_seq_path=('/Game/' + LEVEL_SEQ_NAME), fix_blurred_frame=True):
    """
    Perform LevelSequence export to image sequence
    :param str level_seq_path:
    :param str output_path:
    """
    global _TT_MOVIESCENECAPTURE

    asset_token, tt_root_dir = reread_json_py2(cfg)

    # Modify the global MovieSceneCapture object
    _TT_MOVIESCENECAPTURE = create_movie_capture(
        level_seq_path,
        tt_root_dir,
        IMG_FORMAT,
        IMG_RESOLUTION,
        asset_token['asset_name'],
        FN_PADDING
    )

    if fix_blurred_frame:
        # Override the Start Frame to avoid motion-blurred frame 0
        _TT_MOVIESCENECAPTURE.use_custom_start_frame = True
        _TT_MOVIESCENECAPTURE.custom_start_frame = unreal.FrameNumber(-FIX_BLURRED_FRAME_RANGE)
        # Must set for custom_end_frame, too, or else it will strangely disregard current settings
        _TT_MOVIESCENECAPTURE.use_custom_end_frame = True
        _TT_MOVIESCENECAPTURE.custom_end_frame = unreal.FrameNumber(SEQ_TOTAL_FRAMES + FIX_BLURRED_FRAME_RANGE)
        # Same thing for custom_frame_rate
        _TT_MOVIESCENECAPTURE.settings.use_custom_frame_rate = True
        _TT_MOVIESCENECAPTURE.settings.custom_frame_rate = unreal.FrameRate(SEQ_DISP_RATE, 1)  # 3.0 fps

    # Perform Movie Render
    unreal.SequencerTools.render_movie(_TT_MOVIESCENECAPTURE, unreal.OnRenderMovieStopped())


def versioning_tt(cfg=CUSTOM_CFG, fix_blurred_frame=True):
    """
    Perform the versioning
    """
    global _TT_MOVIESCENECAPTURE

    asset_token, tt_root_dir = reread_json_py2(cfg)

    if fix_blurred_frame:
        # Clean up the exported buffer frame
        # TODO: change this to work in case FIX_BLURRED_FRAME_RANGE is larger than 1
        DELIMITER = '.'
        tt_fix_blurred_frame_buffer = _TT_MOVIESCENECAPTURE.settings.output_format  # CampCabins_BuildingCabin_MASTER.{frame}
        tt_fix_blurred_frame_buffer = DELIMITER.join([tt_fix_blurred_frame_buffer.rpartition(DELIMITER)[0], '-' + str(FIX_BLURRED_FRAME_RANGE).zfill(FN_PADDING - 1)]) + IMG_FORMAT[0]
        # CampCabins_BuildingCabin_MASTER.-001.jpg

        tt_fix_blurred_frame_buffer = os.path.join(tt_root_dir, tt_fix_blurred_frame_buffer)
        if os.path.exists(tt_fix_blurred_frame_buffer):
            unreal.log('Cleaning up "fix blurred frame buffer"')
            os.remove(tt_fix_blurred_frame_buffer)
    
    run_versioning_cmd(cfg, asset_token)


def show_results(cfg=CUSTOM_CFG):
    """
    Launch Windows Explorer at output location
    """
    asset_token, tt_root_dir = reread_json_py2(cfg)
    subprocess.Popen(['explorer', os.path.normpath(tt_root_dir)])
