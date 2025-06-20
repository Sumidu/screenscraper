import json
from screenscraper.client import ScreenScraperClient


def test_get_platforms_list():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    try:
        result = client.get_platforms_list()
        platforms = result
        print(f"✅ Found {len(platforms)} platforms.")
        assert isinstance(platforms, list)
    except Exception as e:
        print(f"❌ API call failed: {e}")
        raise
    
def test_get_game_info():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    game = client.get_game_info(rom_filename="Super Mario Bros..nes", system_id="75")
    print("🎮 Title:", game.title("us"))
    print("📅 Year:", game.year)
    print("🧑‍💻 Developer:", game.developer)
    print("🧑‍🎨 Publisher:", game.publisher)
    print("🕹 Players:", game.players)
    print("📝 Description:", game.description("en"))
    print("🏷 Genres:", ", ".join(game.genres))
    
def test_get_server_info():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    server_info = client.get_server_info()
    print("🖥 Server Info:")
    for key, value in server_info.items():
        print(f"  {key}: {value}")
    assert "cpu1" in server_info
    
def test_get_user_info():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    user = client.get_user_info()
    print(user.summary())

    assert user.requests_today <= user.max_per_day

def test_get_regions():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    regions = client.get_regions()
    print("🌍 Available regions:")
    for region in regions[:5]:
        print(f"  {region}")
    assert len(regions) > 0

def test_get_system_medialist():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")
    media_list = client.get_system_media_list()
    assert len(media_list) > 0
    
def test_get_company_media():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")

    result = client.get_company_media(
        company_id=3,  # Use a known ID like Nintendo or Sega
        media="logo-monochrome",
        outputformat="png",
        max_age=5  # Low cache time for testing
    )

    if isinstance(result, bytes):
        print("✅ Received media content.")
        assert len(result) > 0
    else:
        print("⚠️ Server response:", result)
        assert result in ("CRCOK", "MD5OK", "SHA1OK", "NOMEDIA")
    

def test_clear_cache():
    client = ScreenScraperClient.from_credentials_file("screenscraper_credentials.json")
    client.clear_cache()
    print("✅ Cache cleared.")
   

if __name__ == "__main__":
    #test_clear_cache()
    test_get_server_info()
    test_get_platforms_list()
    test_get_game_info()
    test_get_user_info()
    test_get_regions()
    test_get_system_medialist()
    test_get_company_media()
