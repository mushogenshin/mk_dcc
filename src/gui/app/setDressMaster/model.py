class Model(object):
    def __init__(self):
        super(Model, self).__init__()
        self.data = {
            "init": {
                "cloud_meshes": [],
                "scatter_meshes": [],
                "ground_meshes": [],
            },
            "mash": {
                "mash_network": None,
                "mash_placer": None,
                "mash_bullet": None,
            },
            "baked": {}
        }
