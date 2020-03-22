# -*- coding: utf-8 -*-
# !/usr/bin/env python

TAB_TEXTS = {'tabA': {'EN': 'Lib', 'VI': u'ThưViện'},
             'tabB': {'EN': 'Toolbox', 'VI': u'Toolbox'},
             'tabC': {'EN': 'Utils_1', 'VI': u'TiệnÍch_1'},
             'tabD': {'EN': '_2', 'VI': u'_2'},
             'tabE': {'EN': 'Misc_3', 'VI': u'LặtVặt_3'},
             'tabF': {'EN': '_4', 'VI': u'_4'},
             'tabG': {'EN': 'Export', 'VI': u'XuấtFile'}}

BUTTON_LABELS = {'OKB': {'EN': 'KitBash Browser', 'VI': u'Mở ILM KitBash'},
                 'OEN': {'EN': 'Environment Browser', 'VI': u'Mở ILM Environment'},
                 'OCO': {'EN': 'Costume Browser', 'VI': u'Mở ILM Costume'},
                 'OCH': {'EN': 'Characters Browser', 'VI': u'Mở ILM Characters'},
                 'OAC': {'EN': 'Animals/Creatures Browser', 'VI': u'Mở ILM Animals/Creatures'},

                 'PHP': {'EN': 'PhysX Painter', 'VI': u'TTMM: Tool tô mây mưa'},
                 'SBC': {'EN': 'Setup Soft-Body Collision', 'VI': u'Setup "Chân cứng đá mềm"'},

                 'RMC': {'EN': 'Replace mesh w/ GPU cache', 'VI': u'Thay mesh = GPU cache'},
                 'RMO1': {'EN': 'Setup loc', 'VI': u'Setup loc'},
                 'RMO2': {'EN': 'From guide', 'VI': u'Copy từ "guide"'},

                 'PI2': {'EN': "Pivot to", 'VI': u'Dời pivot về'},

                 'CCH1': {'EN': 'One', 'VI': u'Tạo một'},
                 'CCH2': {'EN': 'Multiple', 'VI': u'Tạo nhiều'},
                 'CCH3': {'EN': 'W/ Config', 'VI': u'Kèm thông số'},

                 'FCC': {'EN': "Croquet's Couture tool", 'VI': u'Mở Couture của Croquet'},
                 'CNC': {'EN': 'Combine curves', 'VI': u'Gộp curve'},
                 'SNC': {'EN': 'Separate curves', 'VI': u'Tách curve'},
                 'TSM': {'EN': 'Tag as scalp', 'VI': u'Tag làm da đầu'},
                 'S2S': {'EN': 'Snap hair roots', 'VI': u'Bám chân tóc vào'},
                 'P2R': {'EN': 'Pivot to crv root', 'VI': u'Dời pivot về chân'},
                 'P2T': {'EN': 'Pivot to crv tip', 'VI': u'Dời pivot về ngọn'},
                 'DBT': {'EN': 'Dissect before Transfer', 'VI': u'Tách + phân tích trước khi Transfer'},

                 'SEE': {'EN': 'Select every', 'VI': u'Chọn xen kẽ'},
                 'SEA': {'EN': 'Select all', 'VI': u'Chọn toàn bộ'},
                 'SMP': {'EN': 'Make ScaleManip "screen-space"', 'VI': u'Xoay ScaleManip về "screen-space"'},

                 'SAN': {'EN': 'Save As: f.name from selected', 'VI': u'Save As: file name từ vật đang chọn'},
                 'ATP': {'EN': 'Prep animated thumbnail', 'VI': u'Chuẩn bị cho chụp CB thumbnail'},
                 'BTW': {'EN': 'Bring all to world origin', 'VI': u'Trả tất cả về tâm thế giới'},
                 'RAW': {'EN': 'Reset all windows', 'VI': u'Hiện lại cửa sổ bị ẩn'},

                 'PFD': {'EN': 'Change "file drop" options',
                         'VI': u'Setup cách drop file vào maya (với nhiều options hơn)'},

                 'ESF': {'EN': 'Export .fbx separately', 'VI': u'Xuất rời .fbx'},
                 'ESM': {'EN': 'Export .ma separately', 'VI': u'Xuất rời .ma'},
                 'ESO': {'EN': 'Export .obj separately', 'VI': u'Xuất rời .obj'},

                 'STR': {'EN': 'Strip the Rig', 'VI': u'Xuất skeletal mesh cho engines'},

                 # 'MUV': {'EN': 'Create morphed-UV mesh', 'VI': u'Sửa mesh trên bản trải UV'},
                 # 'UMT': {'EN': 'UDIM manual tiling', 'VI': u'Tạo UDIM tiling thủ công'},
                 # 'MNT2': {'EN': 'Update all miniTools2 module files',
                 # 'VI': u'Cập nhật toàn bộ module miniTools2'},
                 4: {'EN': '', 'VI': u''}}

BUTTON_TOOLTIPS = {'OKB': {'EN': "Open Maya's Content Browser, navigated to the KitBash folder in ILM/share.",
                           'VI': u'Mở cửa sổ Content Browser của Maya, dẫn sẵn đến thư mục KitBash của ILM'},
                   'OEN': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'OCO': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'OCH': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'OAC': {'EN': '', 'VI': u''},  # TODO: write tooltip here

                   'PHP': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'SBC': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'FCC': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'RMC': {'EN': 'Select the mesh(es) and run to replace them by GPU cache.',
                           'VI': u'Chọn một hay nhiều mesh rồi chạy, để thế bằng GPU cache.'},
                   'RMO1': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'RMO2': {'EN': 'Select the guide first. Select the "frozen" meshes last.',
                            'VI': u'Chọn vật "hướng dẫn" trước, chọn những mesh đã bị freeze transform cuối cùng.'},

                   'CCH1': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'CCH2': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'CCH3': {'EN': '', 'VI': u''},  # TODO: write tooltip here

                   'CNC': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'SNC': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'TSM': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'S2S': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'P2R': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'P2T': {'EN': '', 'VI': u''},  # TODO: write tooltip here

                   'DBT': {'EN': '', 'VI': u''},  # TODO: write tooltip here

                   'ESF': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'ESM': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'STR': {'EN': '', 'VI': u''},  # TODO: write tooltip here

                   'BTW': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'ATP': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'SAN': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'SMP': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'MUV': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'RAW': {'EN': 'Use this when some windows do not show up due to outdated preferences.',
                           'VI': u'Dùng trong trường hợp một số cửa sổ không chịu hiện ra, nhất là sau khi thay đổi \
màn hình.'},
                   'UMT': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   'MNT2': {'EN': '', 'VI': u''},  # TODO: write tooltip here
                   4: {'EN': '', 'VI': u''}}
