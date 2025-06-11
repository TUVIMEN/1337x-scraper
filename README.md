# 1337x-scraper

A scraper for 1337x.

The program originally consisted of 2 scripts `torrents.py` and `links.py`, where you would first pass keywords to `links.py` which would search for torrents links by through all pages, by all categories and by all possible ways of sorting (all of that with optimizations). Then it would extract unique keywords from their titles and run continuously until nothing was left. Later links could be scraped by `torrents.py`.

This design was due to me not realizing that you can just iterate over the id's and 95% of them would be correct. Now `torrents.py` handles everything.

# output examples

```json
{
  "title": "The.Amateur.2025.1080p.WEB-DL.DDP5.1.x265-NeoNoir",
  "magnet": "magnet:?xt=urn:btih:495DF65F08FB18DFA91A881EC713CC8825865E4D&dn=The.Amateur.2025.1080p.WEB-DL.DDP5.1.x265-NeoNoir&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce&tr=http%3A%2F%2Fopen.tracker.cl%3A1337%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fexplodie.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fexodus.desync.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.ololosh.space%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.dump.cl%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker-udp.gbitt.info%3A80%2Fannounce&tr=udp%3A%2F%2Fretracker01-msk-virt.corbina.net%3A80%2Fannounce&tr=udp%3A%2F%2Fopen.free-tracker.ga%3A6969%2Fannounce&tr=udp%3A%2F%2Fns-1.x-fins.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=http%3A%2F%2Ftracker.openbittorrent.com%3A80%2Fannounce&tr=udp%3A%2F%2Fopentracker.i2p.rocks%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce",
  "tags": [],
  "infohash": "495DF65F08FB18DFA91A881EC713CC8825865E4D",
  "category": "Movies",
  "type": "HEVC/x265",
  "language": "English",
  "size": 2040109465,
  "uploader_link": "https://1337x.to/user/NeoNoir/",
  "uploader": "NeoNoir",
  "downloads": 37005,
  "checked": "2025-06-11T14:32:03.981344",
  "uploaded": "2025-06-10T15:32:03.981261",
  "seeders": 4559,
  "leechers": 1111,
  "description": "<img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/e4085ae54948676072755e14d8f00920.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/5018c1fbc7361c48e00c82e82fb82eab.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/a80f036e8b6503a00bd511de816a007c.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/8e141543a7a89cffaacff2382008df76.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/ccb2510bdbbd0f1d5edf996ff985e45c.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/5cc384ec82832344589064d36a07d274.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/a17fa11c0ea8dc46a7a7f24492cee24a.png\" class=\"img-responsive descrimg lazy\"/> <br/><img src=\"/images/profile-load.svg\" data-original=\"https://lookmyimg.com/images/2025/06/09/3010d5142528bae7a6b86e0e577f6a99.png\" class=\"img-responsive descrimg lazy\"/> <br/><br/><strong><span style=\"color:red;\">The.Amateur.2025.1080p.WEB-DL.DDP5.1.x265-NeoNoir</span> <br/><br/><a target=\"_blank\" href=\"https://www.imdb.com/title/tt0899043/\">https://www.imdb.com/title/tt0899043/</a> <br/><br/>Container.......: Matroska <br/>Size............: 1.94 GiB <br/>Duration........: 02:02:33.917  <br/>Source(s).......: The.Amateur.2025.1080p.iT.WEB-DL.DDPA5.1.H.264-HONE (thanks!) <br/><br/>Codec...........: HEVC <br/>Resolution......: 1920x804 <br/>Bit rate........: 2 007 kb/s <br/>Frame rate......: 24.000 fps <br/>Format..........: E-AC-3 <br/>Channels........: 6 <br/>Sample rate.....: 48.0 kHz <br/>Bit rate........: 256 kb/s <br/>Audio...........: English <br/>Subtitle(s).....: English (Forced), English, English (SDH), Spanish (Latin America) (Latin American), French (CA) (Canadian), <br/>  <br/><br/><span style=\"color:green;\">Greetings to all fellow encoders and p2p users!</span> <br/> </strong>",
  "trackers": [
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://open.demonii.com:1337/announce",
    "http://open.tracker.cl:1337/announce",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://explodie.org:6969/announce",
    "udp://exodus.desync.com:6969/announce",
    "udp://tracker.ololosh.space:6969/announce",
    "udp://tracker.dump.cl:6969/announce",
    "udp://tracker.bittor.pw:1337/announce",
    "udp://tracker-udp.gbitt.info:80/announce",
    "udp://retracker01-msk-virt.corbina.net:80/announce",
    "udp://open.free-tracker.ga:6969/announce",
    "udp://ns-1.x-fins.com:6969/announce",
    "udp://leet-tracker.moe:1337/announce"
  ],
  "files": [
    {
      "type": "movies",
      "name": "The.Amateur.2025.1080p.WEB-DL.DDP5.1.x265-NeoNoir.mkv",
      "size": 2040109465
    }
  ],
  "detail": {
    "cover": "https://lx1.dyncdn.cc/cdn/e8/e80eeaaa5d37dbba3202db76aa2ea0df.jpg",
    "rating": 66,
    "title": "The Amateur",
    "categories": [
      "Thriller",
      "Action"
    ],
    "description": "After his life is turned upside down when his wife is killed in a London terrorist attack, a brilliant but introverted CIA decoder takes matters into his own hands when his supervisors refuse to take action."
  },
  "id": 6419201
}
```

```json
{
  "title": "DRAGON BALL SUPER (2015-2018) - The Complete TV Series, Season 1,2,3,4,5 S01-S05 plus 3 Movies (Z: Battle of Gods, Resurrection \"F\" Frieza, Broly) - 1080p BluRay DUAL AUDIO x264",
  "magnet": "magnet:?xt=urn:btih:C9F7A4E3E1AF25E4F0EFCC38720F29E156F4CA1A&dn=DRAGON+BALL+SUPER+%282015-2018%29+-+The+Complete+TV+Series%2C+Season+1%2C2%2C3%2C4%2C5+S01-S05+plus+3+Movies+%28Z%3A+Battle+of+Gods%2C+Resurrection+%26quot%3BF%26quot%3B+Frieza%2C+Broly%29+-+1080p+BluRay+DUAL+AUDIO+x264&tr=http%3A%2F%2Fnyaa.tracker.wf%3A7777%2Fannounce&tr=http%3A%2F%2Fanidex.moe%3A6969%2Fannounce&tr=http%3A%2F%2Ftracker.anirena.com%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.uw0.xyz%3A6969&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fipv4.tracker.harry.lu%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fretracker.lanta-net.ru%3A2710%2Fannounce&tr=udp%3A%2F%2Ftracker.moeking.me%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce&tr=udp%3A%2F%2Ftracker.zer0day.to%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Fcoppersurfer.tk%3A6969%2Fannounce",
  "tags": [
    "pokemon digimon",
    "one piece z gt",
    "naruto boruto",
    "shippuden my",
    "hero academia",
    "dorohedoro",
    "mighty morphin",
    "power rangers"
  ],
  "infohash": "C9F7A4E3E1AF25E4F0EFCC38720F29E156F4CA1A",
  "category": "Anime",
  "type": "Dual Audio",
  "language": "English",
  "size": 86543591014,
  "uploader_link": "https://www.1337xx.to/user/g01ngf0rward/",
  "uploader": "g01ngf0rward",
  "downloads": 133,
  "checked": "2020-12-19T00:00:00",
  "uploaded": "2020-12-16T00:00:00",
  "seeders": 16,
  "leechers": 84,
  "description": "Hello everybody, this torrent contains the COMPLETE \"Dragon Ball SUPER\" Anime Series that aired from 2015-2018 as well as the 3 MOVIES that have came out related to it (so far)! This is all this DUAL AUDIO torrent contains (in 1080p resolution), guys:\n\nTV Series (2015-2018):\n\nSeason 1 (2015)\nSeason 2 (2015-16)\nSeason 3 (2016)\nSeason 4 (2016-17)\nSeason 5 (2017-18)\nSeries EXTRAS\n\nMovies (2013-2018):\n\nDragon Ball Z: Battle of Gods - EXTENDED Director's CUT (2013) + EXTRAS\nDragon Ball Z: Resurrection \"F\" aka Frieza (2015) + 2 MORE \"Alternate\" Films AND EXTRAS\nDragon Ball Super: Broly (2018) + EXTRAS\n\nPlot Synopsis:\n\nDragon Ball SUPER: The Series (2015-2018) - \"With Majin Buu defeated half-a-year prior, peace returns to Earth, where Son Goku (now a radish farmer) and his friends now live peaceful lives. However, a new threat appears in the form of Beerus, the God of Destruction. Considered the most terrifying being in the entire universe, Beerus is eager to fight the legendary warrior seen in a prophecy foretold decades ago known as the Super Saiyan God. The series retells the events from the two Dragon Ball Z films, Battle of Gods and Resurrection 'F' before proceeding to an original story about the exploration of alternate universes.\"\n\nDragon Ball Z: Battle of Gods (2013) - \"The events of Battle of Gods take place some years after the battle with Majin Buu, which determined the fate of the entire universe. Bills, the God of Destruction, is tasked with maintaining some sort of balance in the universe. After awakening from a long slumber, Bills is visited by Whis and learns that the galactic overlord Frieza has been defeated by a Super Saiyan from the North Quadrant of the universe named Goku, who is also a former student of the North Kai. Ecstatic over the new challenge, Goku ignores King Kai's advice and battles Bills, but he is easily overwhelmed and defeated. Bills leaves, but his eerie remark of \"Is there nobody on Earth more worthy to destroy?\" lingers on. Now it is up to the heroes to stop the God of Destruction before all is lost.\"\n\nDragon Ball Z: Resurrection \"F\" aka Frieza (2015) - \"After the God of Destruction Beerus decided to not destroy the Earth, the planet is back again in peace. But, Sorube and Tagoma, previous Freeza's servants, decide to revive his leader using the Dragon Balls. Succesful in his plan, Freeza decides to return to earth to start his revenge against the Saiya-jin who humiliated him once.\"\n\nDragon Ball Super: Broly (2018) - \"Forty-one years ago on Planet Vegeta, home of the infamous Saiyan warrior race, King Vegeta noticed a baby named Broly whose latent power exceeded that of his own son. Believing that Broly's power would one day surpass that of his child, Vegeta, the king sends Broly to the desolate planet Vampa. Broly's father Paragus follows after him, intent on rescuing his son. However, his ship gets damaged, causing the two to spend years trapped on the barren world, unaware of the salvation that would one day come from an unlikely ally.\n\nYears later on Earth, Gokuu Son and Prince Vegeta—believed to be the last survivors of the Saiyan race—are busy training on a remote island. But their sparring is interrupted when the appearance of their old enemy Frieza drives them to search for the last of the wish-granting Dragon Balls on a frozen continent. Once there, Frieza shows off his new allies: Paragus and the now extremely powerful Broly. A legendary battle that shakes the foundation of the world ensues as Gokuu and Vegeta face off against Broly, a warrior without equal whose rage is just waiting to be unleashed.\"\n\n_____________________________\n\n\nName (Title): DRAGON BALL SUPER (2015-2018) - The Complete TV Series, Season 1,2,3,4,5 S01-S05 plus 3 Movies (Z: Battle of Gods, Resurrection \"F\" Frieza, Broly) - 1080p BluRay DUAL AUDIO x264.\n\nCategory Type: TV Series and Movies.\n\nLength (Duration): 22+ Minutes per Episode and Movies VARY in Length.\n\nYear(s): 2015-2018 (Series) and 2013-2018 (Movies)..\n\nGenre(s): Superhero, Action, Supernatural, Fantasy, Comedy, Suspense, Crime, Mystery, Kids, etc...\n\nResolution: 1080p.\n\nRip Type (Source): BluRay -\n\n\"Dragon Ball Super S00-S05 REPACK2 1080p BluRay Dual Audio FLAC 5.1 x264-KaiDubs\"\n\n\"Dragon.Ball.Super.The.Movie.Broly.2018.MANGA.UK.DUAL.AUDiO.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-SBLX\"\n\n\"[Pendekar] Dragon Ball Z - Movie 15 - Resurrection F [Dual Audio].mkv\"\n\n\"Dragon.Ball.Super.The.Movie.Broly.2018.MANGA.UK.DUAL.AUDiO.1080p.BluRay.REMUX.AVC.DTS-HD.MA.5.1-SBLX\"\n\nCodec Type: x264.\n\nFormat of File(s): MKV(s) for pretty much everything but a few of the Extras (which are in MP4 format).\n\nAudio Format & Language(s): DUAL AUDIO -> ENGLISH and JAPANESE audios, mainly:\n\nSERIES -> ENGLISH Audio in AC3 5.1 6-Channel Format (640 KBPs) and JAPANESE Audio in AC3 2.0 2-Channel Format (224 KBPs).\n\nMOVIES -> English AND Japanese Audios in AC3 5.1 6-Channel Format (640 KBPs).\n\nSubtitles: YES -> ENGLISH Internal \"SSA/SRT\" Subs Muxed into the MKVs.\n\nChapters: Yes.\n\nInformation Link(s):\n\nhttps://dragonball.fandom.com/wiki/Dragon_Ball_Super_(anime)\n\nhttps://www.imdb.com/title/tt4644488/\n\nhttps://www.imdb.com/title/tt2263944/\n\nhttps://www.imdb.com/title/tt3819668/\n\nhttps://www.imdb.com/title/tt7961060/",
  "trackers": [
    "http://nyaa.tracker.wf:7777/announce",
    "http://anidex.moe:6969/announce",
    "http://tracker.anirena.com:80/announce",
    "udp://tracker.uw0.xyz:6969",
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://tracker.coppersurfer.tk:6969/announce",
    "udp://9.rarbg.com:2710/announce",
    "udp://tracker.leechers-paradise.org:6969/announce",
    "udp://ipv4.tracker.harry.lu:80/announce",
    "udp://tracker.tiny-vps.com:6969/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://retracker.lanta-net.ru:2710/announce",
    "udp://tracker.moeking.me:6969/announce",
    "udp://open.stealth.si:80/announce",
    "udp://tracker.cyberia.is:6969/announce",
    "udp://tracker.internetwarriors.net:1337/announce",
    "udp://zephir.monocul.us:6969/announce",
    "udp://tracker3.itzmx.com:6961/announce",
    "udp://bt1.archive.org:6969/announce",
    "udp://exodus.desync.com:6969/announce"
  ],
  "files": [
    {
      "type": "folder",
      "name": "DRAGON BALL SUPER (2015-2018) - Complete TV Series and 3 Movies - 1080p DUAL AUDIO x264",
      "size": 0
    },
    {
      "type": "folder",
      "name": "Movie 1 (2013)",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - Battle of Gods, DIRECTOR's CUT (2013 BluRay - 1080p DUAL AUDIO).mkv",
      "size": 2147483648
    },
    {
      "type": "folder",
      "name": "Movie 1 Extras",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - Battle of Voice Actors (1080p).mp4",
      "size": 229847859
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - IMax TV Spot 1 (1080p).mkv",
      "size": 8283750
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - IMax TV Spot 2 (1080p).mkv",
      "size": 16882073
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - The Voices of DBZ Unveiled (1080p).mp4",
      "size": 336592896
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - Trailers (1080p).mkv",
      "size": 106430464
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - BoG Extras - TV Spots (1080p).mkv",
      "size": 85249228
    },
    {
      "type": "folder",
      "name": "Movie 2 (2015)",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - Resurrection 'F' aka Frieza (2015 BluRay - 1080p DUAL AUDIO).mkv",
      "size": 2684354560
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - Resurrection 'F', Future Trunks Special Edition (2016 WebRip - 1080p JAP Audio).mp4",
      "size": 1073741824
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - Resurrection 'F', SUPER Fan Edit (2016 BluRay - 720p JAP AUDIO).mkv",
      "size": 1503238553
    },
    {
      "type": "folder",
      "name": "Movie 2 Extras",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - ED (1080p).mp4",
      "size": 74868326
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - ED English (1080p).mp4",
      "size": 74763468
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - NCED English (1080p).mkv",
      "size": 47290777
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - The Return of DBZ (1080p).mkv",
      "size": 1288490188
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - The Voices of DBZ (1080p).mp4",
      "size": 219886387
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - Trailer (1080p).mkv",
      "size": 49912217
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - Trailers (1080p).mkv",
      "size": 108842188
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - TV Spots (1080p).mkv",
      "size": 64906854
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - US Menu (1080p).mkv",
      "size": 22963814
    },
    {
      "type": "movies",
      "name": "Dragon Ball Z - RF Extras - 'Z' No Chikai Music Video (720p).mp4",
      "size": 89024102
    },
    {
      "type": "folder",
      "name": "Movie 3 (2018)",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY (2018 BluRay - 1080p DUAL Audio).mkv",
      "size": 3113851289
    },
    {
      "type": "folder",
      "name": "Movie 3 Extras",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Are You Smarter Than a Voice Actor (1080p).mp4",
      "size": 110205337
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Christopher R. Sabat Answers Your Questions (1080p).mp4",
      "size": 95210700
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - DB Super The Legacy (1080p).mp4",
      "size": 138831462
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Ian Sinclair Answers Your Questions (1080p).mp4",
      "size": 47395635
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Interviews With The Cast of DBS Broly (1080p).mp4",
      "size": 588565708
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Jason Douglas Answers Your Questions (1080p).mp4",
      "size": 50121932
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Monica Rial Answers Your Questions (1080p).mp4",
      "size": 58720256
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Sean Schemmel Answers Your Questions (1080p).mp4",
      "size": 64172851
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - SP00, Menu (1080p).mp4",
      "size": 1677721
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - SP01, PV Collection (1080p).mp4",
      "size": 171966464
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - SP02, Game Information Collection (1080p).mp4",
      "size": 115343360
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Tokuten DVD, Promo Video (480p).mp4",
      "size": 24326963
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Tokuten DVD, Theater Greeting Event (480p).mp4",
      "size": 189058252
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Tokuten DVD, TV-CM (480p).mp4",
      "size": 50331648
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Tokuten DVD, World Premiere in Nippon Budokan (480p).mp4",
      "size": 177209344
    },
    {
      "type": "movies",
      "name": "Dragon Ball Super - BROLY Extras - Trailers (1080p).mkv",
      "size": 185493094
    },
    {
      "type": "folder",
      "name": "ORIGINAL DBZ Series, HERE",
      "size": 0
    },
    {
      "type": "book",
      "name": "DRAGON BALL Z (1989-2018) - The COMPLETE UNCUT Series, DBZ Movies, Specials - 720p x264.txt",
      "size": 8499
    },
    {
      "type": "book",
      "name": "DRAGON BALL Z (1989-2019) - The COMPLETE UNCUT Series, DBZ Movies, Specials - 1080p x264.txt",
      "size": 10649
    },
    {
      "type": "folder",
      "name": "OTHER Anime Packs YOU'd LOVE, Here",
      "size": 0
    },
    {
      "type": "book",
      "name": "1980s ANIME Movies (Pack 1) - 10 Films-OVAs from 1980-1989 - 720p-1080p x264.txt",
      "size": 10240
    },
    {
      "type": "book",
      "name": "1980s ANIME Movies (Pack 2) - 10 Films-OVAs from 1982-1989 - 720p-1080p x264.txt",
      "size": 9625
    },
    {
      "type": "book",
      "name": "APPLESEED (1988-2014) - Complete OVA, Movies, Series - 480p-720p x264.txt",
      "size": 4300
    },
    {
      "type": "book",
      "name": "BUBBLEGUM Crisis (1987-2003) - 2 OVAs, 1 Series, 3 Spinoffs - 480p-720p DUAL Audio x264.txt",
      "size": 5734
    },
    {
      "type": "book",
      "name": "CASSHERN (1973-2008) - Complete Series, OVA, and Film - 480p-720p x264.txt",
      "size": 4096
    },
    {
      "type": "book",
      "name": "CRUSHER JOE and DIRTY PAIR - Complete Movie, OVA, TV Series - 720p-1080p BluRay x264.txt",
      "size": 9420
    },
    {
      "type": "book",
      "name": "CRYING Freeman (1988-1995) - Anime OVA and LIVE-Action Movies Pack - 480p-720p x264 .txt",
      "size": 4198
    },
    {
      "type": "book",
      "name": "CYBERSIX (1999) - Complete Animated TV Series, Season 1 S01 - 480p DVDRip x264.txt",
      "size": 4096
    },
    {
      "type": "book",
      "name": "DARKER Than BLACK (2007-2010) - Complete Series, OVAs, OSTs - 720p DUAL Audio x264.txt",
      "size": 4505
    },
    {
      "type": "book",
      "name": "DarkStalkers - Night Warriors Revenge ANIME and The ANIMATED Series - 480p DVDRip x264.txt",
      "size": 2867
    },
    {
      "type": "book",
      "name": "FINAL FANTASY Anime (1994-2019) - Complete TV, Movie, LIVE-Action Series - 480p-720p OR 1080p x264.txt",
      "size": 9113
    },
    {
      "type": "book",
      "name": "FIST of the NORTH STAR (Hokuto no Ken) - COMPLETE 1984-2015 Series, Movies, OVAs - 480p-720p x264.txt",
      "size": 3891
    },
    {
      "type": "book",
      "name": "F-Zero - GP Legend of Falcon (Falcon Densetsu) - 480p x264.txt",
      "size": 2662
    },
    {
      "type": "book",
      "name": "GANTZ (2004-2016) - Complete Anime Series, 3 Movies, Gantz O - 480p-720p DUAL Audio x264.txt",
      "size": 4608
    },
    {
      "type": "book",
      "name": "GHOST in the SHELL (1995-2015) - Complete Series, Movies, OVAs - 1080p DUAL Audio x264.txt",
      "size": 8601
    },
    {
      "type": "book",
      "name": "GHOST in the SHELL (1995-2015) - Complete Series, Movies, OVAs - 720p DUAL Audio x264.txt",
      "size": 7577
    },
    {
      "type": "book",
      "name": "GODZILLA Anime TRILOGY (2017-2018) - Part 1, 2, 3 - 720p-1080p DUAL Audio x264.txt",
      "size": 4812
    },
    {
      "type": "book",
      "name": "GOLGO 13 (1973-2009) - Anime Series, OVAs, LIVE-Action Movies - 480p-720p x264.txt",
      "size": 3993
    },
    {
      "type": "book",
      "name": "GUNDAM Series (Pack 1) - Mobile Suit 0079, MSG Zeta, ZZ, 7 Movies - 720p DUAL Audio x264.txt",
      "size": 6246
    },
    {
      "type": "book",
      "name": "GUNDAM Series (Pack 2) - 0080 OVA, F91 Movie, 0083, M. Suit Victory, Mobile Fighter G - 720p x264.txt",
      "size": 6553
    },
    {
      "type": "book",
      "name": "GUNDAM Series (Pack 3) - MSG Wing, The 08th MS Team, After War X, Turn A - 720p DUAL Audio x264.txt",
      "size": 8601
    },
    {
      "type": "book",
      "name": "GUNDAM Series (Pack 4) - MSG Seed and Destiny, SD Force, MS IGLOO 1-2 - 720p DUAL Audio.txt",
      "size": 7372
    },
    {
      "type": "book",
      "name": "KIKAIDER (2000-02) - Android, 01 The Animation, Guitar OVA, 2 OSTs - 480p DUAL Audio x264.txt",
      "size": 4300
    },
    {
      "type": "book",
      "name": "MARVEL Anime (2010-2014) - 720p - Wolverine, X-Men, Iron Man and 480p - Blade.txt",
      "size": 2662
    },
    {
      "type": "book",
      "name": "MASAMUNE Shirow - 1987-2006 OVA Collection (480p - DUAL Audio).txt",
      "size": 5324
    },
    {
      "type": "book",
      "name": "Sakigake Otokojuku - ANIME Series, Movie, and LIVE-Action Film - 480p x264.txt",
      "size": 2355
    },
    {
      "type": "book",
      "name": "SHINICHIRO WATANABE Anime (1994-2019) - 8 Complete TV Series, 1 OVA, 3 Movies - 720p-1080p x264.txt",
      "size": 12800
    },
    {
      "type": "book",
      "name": "SPACE Adventure COBRA (1982-2010) - The Movie, Series, Animation, OVA, OST - 720p x264.txt",
      "size": 4403
    },
    {
      "type": "book",
      "name": "STREET FIGHTER (1994-2010) - Anime and Cartoon Collection - 480p-720p x264.txt",
      "size": 2764
    },
    {
      "type": "book",
      "name": "TEKKEN (1997-2014) - Movie and Anime Collection - 480p-720p x264.txt",
      "size": 3481
    },
    {
      "type": "folder",
      "name": "Season 1 (2015)",
      "size": 0
    },
    {
      "type": "movies",
      "name": "Dragon Ball SUPER - S01 E01 - A Peacetime Reward (1080p BluRay - DUAL Audio).mkv",
      "size": 496081305
    },
    {
      "type": "movies",
      "name": "Dragon Ball SUPER - S01 E02 - To the Promised Resort (1080p BluRay - DUAL Audio).mkv",
      "size": 534354329
    },
    {
      "type": "movies",
      "name": "Dragon Ball SUPER - S01 E03 - Where Does the Dream Pic",
      "size": 0
    }
  ],
  "detail": {
    "cover": "",
    "rating": 0,
    "title": "",
    "categories": [],
    "description": ""
  },
  "id": 4711160
}
```

# torrents.py

Under the working directory it creates `torrents-nonexistent` file where unused ids are stored, `torrents-failed` file where ids of failed attempts are stored and `torrents-results` directory where json files named by ids of torrents are stored.

When run in the same working directory nonexistent ids won't be retried, failed attempts will be retried and removed upon success, and already existing torrent files will be skipped.

You can download torrents by specific urls

```shell
./torrents.py 'https://1337x.to/torrent/6416873/Murderbot-S01E05-1080p-x265-ELiTE/' 'https://1337x.to/torrent/6417145/The-Surfer-2024-1080p-WEB-DL-DDP5-1-x265-NeoNoir/'
```

If no urls arguments are given the whole site is scraped, in this case using 6 threads

```shell
./torrents.py -t 6
```

```
usage: torrents.py [-h] [-d DIR] [-t THREADS] [-D DOMAIN] [-w TIME]
                   [-W MILISECONDS] [-r NUM] [--retry-wait TIME]
                   [--force-retry] [-m TIME] [-k] [-L] [-A UA] [-x DICT]
                   [-H HEADER] [-b COOKIE] [-B BROWSER]
                   [URL ...]

Tool for getting torrents from 1337x

positional arguments:
  URL                   urls

options:
  -h, --help            Show this help message and exit
  -d, --directory DIR   Use DIR as working directory
  -t, --threads THREADS
                        amount of threads used for scraping
  -D, --domain DOMAIN   set DOMAIN, by default set to https://www.1337xx.to

Request settings:
  -w, --wait TIME       Sets waiting time for each request
  -W, --wait-random MILISECONDS
                        Sets random waiting time for each request to be at max
                        MILISECONDS
  -r, --retries NUM     Sets number of retries for failed request to NUM
  --retry-wait TIME     Sets interval between each retry
  --force-retry         Retry no matter the error
  -m, --timeout TIME    Sets request timeout
  -k, --insecure        Ignore ssl errors
  -L, --location        Allow for redirections, can be dangerous if
                        credentials are passed in headers
  -A, --user-agent UA   Sets custom user agent
  -x, --proxies DICT    Set requests proxies dictionary, e.g. -x
                        '{"http":"127.0.0.1:8080","ftp":"0.0.0.0"}'
  -H, --header HEADER   Set curl style header, can be used multiple times e.g.
                        -H 'User: Admin' -H 'Pass: 12345'
  -b, --cookie COOKIE   Set curl style cookie, can be used multiple times e.g.
                        -b 'auth=8f82ab' -b 'PHPSESSID=qw3r8an829'
  -B, --browser BROWSER
                        Get cookies from specified browser e.g. -B firefox
```

# sources ( important! )

Script is fully compatible with [official sites](https://1337x.to/), unfortunately they are very restrictive and will block you with cloudflare.

That's why an copycat, [honeypot site is used](https://1337xx.to) by default. I'll claim that it's a honeypot because:

- It's not listed in official proxy list
- It has it's own, independent and short list of proxies, where they redirect to the main site anyway upon search.
- It doesn't display comments, which are even more guarded by cloudflare by official site.
- It doesn't allow to post comments or new torrent, functionalities that would have to otherwise be synced with official sites
- It's protection is extremely weak, it uses cloudflare but in very specific endpoints for example `/search/` is protected, but `/sort-search/` absolutely isn't.

Above all the contents on it are well kept and frequently updated, that's why it's perfect for scraping. It also allows for a lot of consecutive requests and doesn't ban ips. I've managed to download the whole 6.4 million pages from a single ip in a week. Using 6 threads which gives me roughly 60 requests per second, above that more and more requests start failing.



# links.py (no longer required)

Under the working directory it creates `links-keys-found`, `links-keys-used`, `links-saved` files.

```
usage: links.py [-f FILE] [-h] [-d DIR] [-D DOMAIN] [-w TIME] [-W MILISECONDS]
                [-r NUM] [--retry-wait TIME] [--force-retry] [-m TIME] [-k]
                [-L] [-A UA] [-x DICT] [-H HEADER] [-b COOKIE] [-B BROWSER]
                [KEY ...]

Tool for getting links from 1337x

positional arguments:
  KEY                   key to feed the crawler

options:
  -f, --file FILE       Load keys from file
  -h, --help            Show this help message and exit
  -d, --directory DIR   Use DIR as working directory
  -D, --domain DOMAIN   set DOMAIN, by default set to https://www.1337xx.to

Request settings:
  -w, --wait TIME       Sets waiting time for each request
  -W, --wait-random MILISECONDS
                        Sets random waiting time for each request to be at max
                        MILISECONDS
  -r, --retries NUM     Sets number of retries for failed request to NUM
  --retry-wait TIME     Sets interval between each retry
  --force-retry         Retry no matter the error
  -m, --timeout TIME    Sets request timeout
  -k, --insecure        Ignore ssl errors
  -L, --location        Allow for redirections, can be dangerous if
                        credentials are passed in headers
  -A, --user-agent UA   Sets custom user agent
  -x, --proxies DICT    Set requests proxies dictionary, e.g. -x
                        '{"http":"127.0.0.1:8080","ftp":"0.0.0.0"}'
  -H, --header HEADER   Set curl style header, can be used multiple times e.g.
                        -H 'User: Admin' -H 'Pass: 12345'
  -b, --cookie COOKIE   Set curl style cookie, can be used multiple times e.g.
                        -b 'auth=8f82ab' -b 'PHPSESSID=qw3r8an829'
  -B, --browser BROWSER
                        Get cookies from specified browser e.g. -B firefox
```
