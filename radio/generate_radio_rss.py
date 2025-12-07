import requests
from datetime import datetime
import xml.etree.ElementTree as ET

# ======= 网易云 Cookie（你的） =======
cookies = {
    '__oc_uuid': '0093e7b0-4d45-11ef-971e-eb1d976c3494',
    'JSESSIONID-WYYY': 'HyCf6aDH1FwbBJvhbOsvVGEFdrCkjBuZnBQFWQOYO68TE6mAnqSkNWGnuN9WJ2a0h1F0jizgKgv7OmOVn94zuFbvf1IFvunenFQ3poh4TTRByh/y/OnFEMxrqiba13DIZscvtAkNzxosl5FOSQ4JBpNmDHn00SmZI6rdd6CEl\\JETA4I:1765084274207',
    '_iuqxldmzr_': '32',
    '_ntes_nnid': '142f9f61597730eb7ad18cbff883ad67,1765082474265',
    '_ntes_nuid': '142f9f61597730eb7ad18cbff883ad67',
    'MUSIC_U': '0030676A6CE0D6B1E71C4337A5E967A18909CDA000343EE53AA1AC98BC2418FFBEDF0CB7A8895D4193DD91BDE4D2E3FC843AF3552564982AF4F995A08CDA38181FAEC78E1912B4F8CB37A7C94681C7D111A4719C596EFA42F6D5DF2824F31D125F2C3200485B3D2D65566762802608C2AFBC400795EAA3E1874DAA768D2ECF905570AEC90FD0238461A286BB58B2EEFD6C5FDA93A425E9B7BFE7BCBD3BE3E9D2DBD6581C9C65B48E4DE0B9134AE04C31B1113A5CBED555E8854EDDC72572B6CA83EE8BBCEC43F2D9D88A7CBF4D42C8050D492DF432E362E120EE561A78DF8C7EDC02CFF3DC69B90E84BE163CBA0B2BD60C82DC2D18DE7EBA465C341817B0DDB320BF2569DF683F9EC6B3FF65F168D2AE04E519FA0BB61E2170F0A2635150E7439ABD50F5FE8ED9AE90415C8687F96B60D5938C8D3DE79AA96C2224C9276AFF30CCCF953909A506BEB64F21FE1776C80AE473DDC900A43F98A3A874441C567B1E4378DE2E0BD981E988F733630B279F570E9FC56B8B95D59D62706715736FCA2E7D1CBBB2F701D3E5F4B79CA7A761D531F4',
    '__csrf': '52ed22506983875d69c7b80e9588eafd'
}

# ======= 电台 ID =======
radio_id = '965615738'

# ======= API URL =======
radio_api = f'https://music.163.com/api/program/playlist/get?radioId={radio_id}&limit=50'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Referer': f'https://y.music.163.com/m/radio?id={radio_id}',
}

resp = requests.get(radio_api, headers=headers, cookies=cookies)
data = resp.json()

# ======= 生成 RSS =======
rss = ET.Element('rss', version='2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = '经典老歌（网易云电台）'
ET.SubElement(channel, 'link').text = f'https://y.music.163.com/m/radio?id={radio_id}'
ET.SubElement(channel, 'description').text = '经典老歌电台 - 播客兼容 RSS'
ET.SubElement(channel, 'language').text = 'zh-CN'
ET.SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0800')
ET.SubElement(channel, 'generator').text = '网易云电台播客 RSS'

for item_data in data.get('programs', []):
    item = ET.SubElement(channel, 'item')
    ET.SubElement(item, 'title').text = item_data.get('name', '未知节目')
    main_song = item_data.get('mainSong')
    audio_url = main_song.get('mp3Url') if main_song else 'https://example.com/audio.mp3'
    ET.SubElement(item, 'enclosure', url=audio_url, length='12345678', type='audio/mpeg')
    ET.SubElement(item, 'description').text = item_data.get('description', '')
    create_time = item_data.get('createTime', datetime.now().timestamp()*1000)
    ET.SubElement(item, 'pubDate').text = datetime.fromtimestamp(create_time/1000).strftime('%a, %d %b %Y %H:%M:%S +0800')
    ET.SubElement(item, 'guid', isPermaLink='true').text = audio_url

tree = ET.ElementTree(rss)
tree.write('radio_965615738_podcast_real.xml', encoding='utf-8', xml_declaration=True)
print('✅ RSS 文件已生成：radio_965615738_podcast_real.xml')
