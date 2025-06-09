class GameInfo:
    def __init__(self, data: dict):
        self.raw = data
        self.id = data.get("id")
        self.names = data.get("noms", [])
        self.synopsis = data.get("synopsis", [])
        self.system = data.get("systeme", {}).get("text")
        self.publisher = data.get("editeur", {}).get("text")
        self.developer = data.get("developpeur", {}).get("text")
        self.players = data.get("joueurs", {}).get("text")
        self.year = (data.get("dates", [{}])[0]).get("text")
        self.genres = [entry["noms"][0]["text"] for entry in data.get("genres", []) if entry.get("noms")]
        self.media = data.get("medias", [])

    def title(self, region="us"):
        for name in self.names:
            if name.get("region") == region:
                return name["text"]
        return self.names[0]["text"] if self.names else "Unknown"

    def description(self, lang="en"):
        for desc in self.synopsis:
            if desc.get("langue") == lang:
                return desc["text"]
        return None