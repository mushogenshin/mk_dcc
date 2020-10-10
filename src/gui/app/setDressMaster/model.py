class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self._data = {
            "init": {
                "cloud_meshes": [],
                "scatter_meshes": [],
                "ground_meshes": [],
            },
            "baked": {}
        }
        self.init_mash_data()

    def init_mash_data(self):
        self._data["mash"] = {
            "mash_network": None,
            "mash_waiter": None,
            "mash_distribute": None,
            "mash_repro": None,  # the instancer
            "mash_placer": None,
            "mash_dynamics": None,
            "mash_bullet": None,
        }
