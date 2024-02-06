
class Utils:

    @staticmethod
    def get_model(device):
        try:
            return device["modelAlias"]
        except KeyError:
            return device["model"]
