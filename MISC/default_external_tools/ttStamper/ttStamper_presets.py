import os
from pathlib import Path
from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow
from collections import namedtuple

from ui_ttStamper import Ui_ttStamperWindow
from ttStamper_vars import *


StampingConfig = namedtuple("StampConfig", ['content', 'pos', 'override_size'])

# company logos
own_logo_path = Path(__file__).parent / 'company_logos/Sparx_Logo_Red.png'


class TTStamperMainWindow(QMainWindow):
    def __init__(self):
        super(TTStamperMainWindow, self).__init__()
        self.ui = Ui_ttStamperWindow()
        self.ui.setupUi(self)

        self.ui.MasterConfig = {'project': os.environ.get('VSPROJECT', UNSPECIFIED),

                                DEFAULT_OUTPUT_DIR: os.path.join(os.environ['USERPROFILE'], "Pictures"),
                                
                                METADATA_TXT: {
                                                AUTO_DATE: ([get_qdate(), P_TOP_RIGHT, -1], self.ui.autoDate_checkBox.isChecked),
                                                # last item is a validating method
                                            },                    

                                CUST_TXT_MARGIN: (-1, -1),

                                CUST_TXT_FONT: 'arialbd.ttf', # bold type, regular: 'arial.ttf'
                                CUST_TXT_FONT_SIZE: 35,
                                CUST_TXT_FONT_FILL: (255, 255, 255, 255),  # full opague white
                                CUST_TXT_STROKE_WIDTH: 2,
                                CUST_TXT_STROKE_FILL: (0, 0, 0, 255),  # full opague black

                                CUST_TXT_POS: {
	                                            P_TOP_LEFT: (ALIGN_LEFT, ),
	                                            P_TOP_MID: (ALIGN_CENTER, ),
	                                            P_TOP_RIGHT: (ALIGN_RIGHT, ),
	                                            P_BTM_LEFT: (ALIGN_LEFT, ),
	                                            P_BTM_MID: (ALIGN_CENTER, ),
	                                            P_BTM_RIGHT: (ALIGN_RIGHT, ),
                                            },

                                METADATA_IMG: {
                                                OWN_LOGO: (StampingConfig(own_logo_path, P_BTM_RIGHT, 15), self.ui.companyLogo_checkBox.isChecked),
                                                # last item is a validating method
                                                # "override_size" is width percentage in this context
                                            },
                                }

        self.ui.browseOutput_btn.path = Path(self.ui.MasterConfig[DEFAULT_OUTPUT_DIR])

        # ZBRUSH SLOTS
        self.ui.zb_hiRes_listWdg.stampingConfig =  StampingConfig('Hi-Res', P_BTM_MID, -1)
        self.ui.zb_loRes_listWdg.stampingConfig = StampingConfig('Lo-Res', P_BTM_MID, -1)

        # SUBSTANCE PAINTER SLOTS
        self.ui.sp_baseColor_listWdg.stampingConfig = StampingConfig('Base Color', P_BTM_MID, -1)
        self.ui.sp_metallic_listWdg.stampingConfig = StampingConfig('Metallic', P_BTM_MID, -1)
        self.ui.sp_roughness_listWdg.stampingConfig = StampingConfig('Roughness', P_BTM_MID, -1)
        self.ui.sp_normal_listWdg.stampingConfig = StampingConfig('Normal', P_BTM_MID, -1)
        self.ui.sp_height_listWdg.stampingConfig = StampingConfig('Height', P_BTM_MID, -1)
        self.ui.sp_ao_listWdg.stampingConfig = StampingConfig('AO', P_BTM_MID, -1)
        self.ui.sp_emissive_listWdg.stampingConfig = StampingConfig('Emissive', P_BTM_MID, -1)

        # INVALID SLOTS
        self.ui.basicTemplate_listWdg.stampingConfig = None
        self.ui.basicSrc_listWdg.stampingConfig = None
        self.ui.clamp_vid_size_listWdg.stampingConfig = None


def get_qdate():
    currentDate = QtCore.QDate.currentDate()
    return currentDate.toString(QtCore.Qt.ISODate)
