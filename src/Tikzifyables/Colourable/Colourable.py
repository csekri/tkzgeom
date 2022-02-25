class Colourable:
    @staticmethod
    def tikzify_colour(colour):
        if colour["name"] == colour["mix_with"] or colour["mix_percent"] == 0:
            if colour["strength"] == 100:
                return colour["name"]
            return colour["name"] + '!' + str(colour["strength"])
        if colour["strength"] == 100:
            return colour["name"] + '!' + str(100-colour["mix_percent"]) + '!' + colour["mix_with"]
        return colour["name"] + '!' + str(100-colour["mix_percent"]) + '!' + colour["mix_with"] + '!' + str(colour["strength"])
