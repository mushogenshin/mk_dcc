import miniTools2_ui as mnT2_ui
reload(mnT2_ui)

if __name__ == "__main__":
    try:
        mnT2DialogInst.close()
        mnT2DialogInst.deleteLater()
    except:
        pass

    mnT2DialogInst = mnT2_ui.mnT2Dialog()
    mnT2DialogInst.show()
