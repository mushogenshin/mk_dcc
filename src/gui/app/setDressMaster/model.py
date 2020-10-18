class Model(object):
    """
    Model of all PhysX Painter, Swap Master, and Restore Instancing UI elements
    """
    def __init__(self):
        super(Model, self).__init__()
        # PhysX Painter
        self._data = {
            "PP_init": {
                "cloud_meshes": [],
                "scatter_meshes": [],
                "ground_meshes": [],
            },
            "PP_baked": {}
        }
        self.init_PP_mash_data()
        
        # Swap Master
        self.init_SM_data()

    def init_PP_mash_data(self):
        self._data["PP_mash"] = {
            "mash_network": None,
            "mash_waiter": None,
            "mash_distribute": None,
            "mash_repro": None,  # the instancer
            "mash_placer": None,
            "mash_dynamics": None,
            "mash_bullet": None,
        }

    def init_SM_data(self):
        SM_data = {
            "SM_component": {
                "north": {"component_enum": 0, "children": []},
                "south": {"component_enum": 0, "children": []},
                "yaw": {"component_enum": 0, "children": []},
            }
        }
        self._data.update(SM_data)
