import requests
import hashlib
import json
import os
import time
from .game import GameInfo
from .user import UserInfo
from .region import RegionInfo




class ScreenScraperClient:
    BASE_URL = "https://www.screenscraper.fr/api2"

    def __init__(self, dev_user: str, dev_pass: str, software: str, ssid: str = None, sspassword: str = None):
        """
        :param dev_user: Developer ID
        :param dev_pass: Developer password
        :param software: Registered software name
        :param ssid: Optional user login (ScreenScraper ID)
        :param sspassword: Optional user password
        """
        self.dev_user = dev_user
        self.dev_pass = dev_pass
        self.software = software
        self.ssid = ssid
        self.sspassword = sspassword

    def _base_params(self):
        params = {
            "devid": self.dev_user,
            "devpassword": self.dev_pass,
            "softname": self.software,
            "output": "json"
        }
        if self.ssid:
            params["ssid"] = self.ssid
        if self.sspassword:
            params["sspassword"] = self.sspassword
        return params
    
    @classmethod
    def from_credentials_file(cls, filepath: str):
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"⚠️ Credentials file '{filepath}' not found.")

        with open(filepath, "r", encoding="utf-8") as f:
            creds = json.load(f)

        required_keys = ["dev_id", "dev_password", "software", "ssid", "sspassword"]
        for key in required_keys:
            if key not in creds:
                raise ValueError(f"Missing '{key}' in credentials file.")

        return cls(
            dev_user=creds.get("dev_id"),
            dev_pass=creds.get("dev_password"),
            software=creds.get("software"),
            ssid=creds.get("ssid"),
            sspassword=creds.get("sspassword")
        )
    
    
    
    
    # Caches -----------
        
    def _cached_get_json(self, url: str, params: dict, max_age: int = 86400) -> dict:
        full_url = requests.Request("GET", url, params=params).prepare().url
        cached = self._get_cached_response(full_url, max_age=max_age)
        if cached:
            return cached

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        self._set_cached_response(full_url, data)
        return data
    
    def _get_cached_response(self, url: str, max_age: int = 86400):
        """
        Try to load a cached response if it's not older than `max_age` seconds.
        """
        os.makedirs(".cache", exist_ok=True)
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(".cache", f"{cache_key}.json")

        if os.path.exists(cache_path):
            if time.time() - os.path.getmtime(cache_path) < max_age:
                with open(cache_path, "r", encoding="utf-8") as f:
                    print(f"🗃 Using cache for {url}")
                    return json.load(f)

        return None

    def _set_cached_response(self, url: str, data: dict):
        os.makedirs(".cache", exist_ok=True)
        cache_key = hashlib.md5(url.encode()).hexdigest()
        cache_path = os.path.join(".cache", f"{cache_key}.json")

        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(data, f)
            
    def clear_cache(self):
        import shutil
        shutil.rmtree(".cache", ignore_errors=True)
        print("🧹 Cache cleared.")


    # Endpoints ----    

    def get_platforms_list(self):
        """
        Retrieve the list of platforms from the ScreenScraper API.
        """
        url = f"{self.BASE_URL}/systemesListe.php"
        params = self._base_params()

        data = self._cached_get_json(url, params)
        return data.get("response", {}).get("systemes", [])
    
    def get_game_info(self, rom_filename=None, crc=None, md5=None, sha1=None, game_id=None, system_id=None):
        url = f"{self.BASE_URL}/jeuInfos.php"
        params = self._base_params()

        if game_id:
            params["id"] = game_id
        if rom_filename:
            params["romnom"] = rom_filename
        if crc:
            params["romcrc"] = crc
        if md5:
            params["rommd5"] = md5
        if sha1:
            params["romsha1"] = sha1
        if system_id:
            params["systemeid"] = system_id

        if not any([game_id, rom_filename, crc, md5, sha1]):
            raise ValueError("You must provide at least one of: game_id, rom_filename, crc, md5, sha1")

        full_url = requests.Request("GET", url, params=params).prepare().url
        cached = self._get_cached_response(full_url)
        if cached:
            game = cached.get("response", {}).get("jeu")
            return GameInfo(game) if game else None

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        self._set_cached_response(full_url, data)

        game = data.get("response", {}).get("jeu")
        return GameInfo(game) if game else None
    
    
    def get_server_info(self):
        """
        Get current ScreenScraper server and quota status.
        """
        url = f"{self.BASE_URL}/ssinfraInfos.php"
        params = self._base_params()
        data = self._cached_get_json(url, params, max_age=300)
        return data.get("response", {}).get("serveurs", {})
    
    
    def get_user_info(self):
        """
        Retrieve information about the current ScreenScraper user (requires ssid and sspassword).
        """
        if not self.ssid or not self.sspassword:
            raise ValueError("User info requires ssid and sspassword.")

        url = f"{self.BASE_URL}/ssuserInfos.php"
        params = self._base_params()
        data = self._cached_get_json(url, params, max_age=300)  # 5 minutes cache

        return UserInfo(data.get("response", {}).get("ssuser", {}))
    

    def get_regions(self):
        url = f"{self.BASE_URL}/regionsListe.php"
        params = self._base_params()
        data = self._cached_get_json(url, params, max_age=86400)

        regions_dict = data.get("response", {}).get("regions", {})
        return [RegionInfo(region_data) for region_data in regions_dict.values()]
    
   
    # Skipped endpoints
    # - userlevelsListe
    # - nbJoueursListe
    # - supportTypesListe
    # - romTypesListe
    # - genresList
    # - languagesList
    # - classificationListe
    # - mediasSystemeListe
    
    
    
    
    
 