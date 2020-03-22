import subprocess
import re
from datetime import timedelta
from pathlib import Path, PureWindowsPath
from functools import partial
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
import logging

logger = logging.getLogger(__name__)

import ttStamper_utils


_OUTPUT_EXT = '.mov'
# Get the ffmpeg binary path
try:
    from asset.tools.turntable import FFMPEG_BIN
except ImportError as e:
    logger.warning('{}: Opening TT Stamper from Hunter is recommended'.format(e))
    FFMPEG_BIN = "C:/vsTools2/library/bin/ffmpeg2018.N89936/ffmpeg.exe"

def ui_init(ui, asset_token):
    pass
    
def create_connections(ui, win):
    ui.clamp_vid_size_execute_btn.clicked.connect(partial(
        clamp_video_size,
        ui=ui
    ))

def clamp_video_size(ui):
    # Get the video file list
    # namedtuple ttsListWdgData: (list of QUrls, stampingConfig value)
    video_files = ttStamper_utils.get_list_wdg_items(ui.clamp_vid_size_listWdg).QUrls
    video_files = [Path(qurl.toLocalFile()) for qurl in video_files]

    jobs = len(video_files)

    # Get the clamping specs
    clamp_value, clamp_suffix = get_clamp_value(ui=ui)

    if Path(FFMPEG_BIN).exists():
        for job, video_file in enumerate(video_files, 1):
            perform_clamp_video_size(
                FFMPEG_BIN,
                video_file,
                clamp_value,
                clamp_suffix
            )
            # updates the progress bar
            ui.performStamp_progressBar.setValue(round(job / jobs * 100))
    else:
        logger.error('Unable to locate ffmpeg binary. Aborted.')
        return False

def perform_clamp_video_size(ffmpeg_bin, video_file, clamp_value, clamp_suffix):

    # Get the clip duration
    video_duration = get_duration(ffmpeg_bin, video_file)  
    logger.info('Processing video "{}". Duration: {}s'.format(video_file.name, video_duration))
   
    target_bitrate = get_target_video_bitrate(clamp_value, video_duration)
    logger.info('Target video bitrate: {}'.format(target_bitrate))

    output_name = get_output_name(video_file, clamp_value, clamp_suffix)

    pass1 = [
        '-y',
        '-i', video_file.as_posix(),
        '-pix_fmt', 'yuv420p',
        '-c:v', 'libx264',
        '-b:v', target_bitrate,
        '-pass', '1',
        '-f', 'null', '-'
    ]

    pass2 = [
        '-i', video_file.as_posix(),
        '-pix_fmt', 'yuv420p',
        '-c:v', 'libx264',
        '-b:v', target_bitrate,
        '-pass', '2',
        video_file.with_name(output_name).as_posix()
    ]

    ffmpeg_cmd = [ffmpeg_bin] + pass1 + ['&&', ffmpeg_bin] + pass2
    logger.debug('FFMPEG COMMANDS: {}'.format(ffmpeg_cmd))

    try:
        subprocess.call(ffmpeg_cmd, shell=True)
    except Exception as e:
        logger.warning(e)
    else:
        logger.info('Success')

def get_duration(ffmpeg_bin, video_file):
    decode_result = subprocess.run(
        [ffmpeg_bin,
        '-i', video_file.as_posix(),
        '-f', 'null', '-'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    decode_result = decode_result.stdout.decode('utf-8')  # decoding from bytes object

    time_pattern = re.compile('time=(\d+:\d+:\d+.\d+)')
    video_duration = time_pattern.findall(decode_result)[-1]  # true duration in HOURS:MM:SS.MICROSECONDS format

    dur_h, dur_m, dur_s = map(float, video_duration.split(':'))
    video_duration = timedelta(
        hours=dur_h,
        minutes=dur_m,
        seconds=dur_s
    ).total_seconds()  # float in seconds

    return video_duration

def get_target_video_bitrate(clamp_value, video_duration):
    target_bitrate = round(clamp_value * 8192 / video_duration)  # kilobits/s
    return str(target_bitrate) + 'k'
    
def get_clamp_value(ui):
    return ui.clamp_vid_size_spinBox.value(), ui.clamp_vid_size_spinBox.suffix()

def get_output_name(video_file, clamp_value, clamp_suffix):
    return '_'.join([video_file.stem, str(clamp_value) + clamp_suffix.strip()]) + _OUTPUT_EXT
