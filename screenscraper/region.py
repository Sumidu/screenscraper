class RegionInfo:
    def __init__(self, data):
        self.id = int(data["id"])
        self.shortname = data.get("nomcourt")
        self.name_en = data.get("nom_en")
        self.name_de = data.get("nom_de")
        self.name_fr = data.get("nom_fr")
        self.name_es = data.get("nom_es")
        self.name_it = data.get("nom_it")
        self.name_pt = data.get("nom_pt")
        self.parent = int(data.get("parent", 0))

    def __repr__(self):
        return f"<Region {self.id}: {self.name_en}>"