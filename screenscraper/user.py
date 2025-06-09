class UserInfo:
    def __init__(self, data: dict):
        self.raw = data
        self.username = data.get("id")
        self.user_id = data.get("numid")
        self.level = data.get("niveau")
        self.contribution = int(data.get("contribution", 0))
        self.upload_systems = int(data.get("uploadsysteme", 0))
        self.upload_infos = int(data.get("uploadinfos", 0))
        self.upload_media = int(data.get("uploadmedia", 0))
        self.rom_asso = int(data.get("romasso", 0))
        self.requests_today = int(data.get("requeststoday", 0))
        self.requests_ko_today = int(data.get("requestskotoday", 0))
        self.max_per_min = int(data.get("maxrequestspermin", 0))
        self.max_per_day = int(data.get("maxrequestsperday", 0))
        self.max_ko_per_day = int(data.get("maxrequestskoperday", 0))
        self.max_threads = int(data.get("maxthreads", 0))
        self.download_speed = int(data.get("maxdownloadspeed", 0))
        self.last_visit = data.get("datedernierevisite")
        self.fav_region = data.get("favregion")

    @property
    def daily_usage_pct(self):
        if self.max_per_day:
            return round((self.requests_today / self.max_per_day) * 100, 2)
        return None

    @property
    def ko_usage_pct(self):
        if self.max_ko_per_day:
            return round((self.requests_ko_today / self.max_ko_per_day) * 100, 2)
        return None

    def summary(self):
        return (
            f"👤 {self.username} (Level {self.level})\n"
            f"🔄 API today: {self.requests_today}/{self.max_per_day} "
            f"({self.daily_usage_pct}% used)\n"
            f"❌ Negative requests: {self.requests_ko_today}/{self.max_ko_per_day} "
            f"({self.ko_usage_pct}% used)\n"
            f"📥 Max download speed: {self.download_speed} KB/s\n"
            f"🧵 Threads allowed: {self.max_threads}\n"
            f"🗓 Last visit: {self.last_visit} (Region: {self.fav_region})"
        )
