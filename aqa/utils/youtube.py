import pytube

def download_video(url, resolution):
    itag = choose_resolution(resolution)
    video = pytube.YouTube(url)
    stream = video.streams.get_by_itag(itag)
    stream.download()
    return stream.default_filename

def download_videos(urls, resolution):
    for url in urls:
        download_video(url, resolution)

def download_playlist(url, resolution):
    playlist = pytube.Playlist(url)
    download_videos(playlist.video_urls, resolution)

def choose_resolution(resolution):
    if resolution in ["low", "360", "360p"]:
        itag = 18
    elif resolution in ["medium", "720", "720p", "hd"]:
        itag = 22
    elif resolution in ["high", "1080", "1080p", "fullhd", "full_hd", "full hd"]:
        itag = 137
    elif resolution in ["very high", "2160", "2160p", "4K", "4k"]:
        itag = 313
    else:
        itag = 18
    return itag


def input_links():
    print("Enter the links of the videos (end by entering 'STOP'):")

    links = []
    link = ""

    while link != "STOP" and link != "stop":
        link = input()
        links.append(link)

    links.pop()

    return links

"""
TẠO VIDEO câu chuyện hoạt hình 3D dành cho trẻ em bằng CÔNG CỤ AI miễn phí
CÁC PHÂN ĐOẠN TRONG VIDEO:
00:00 - giới thiệu
1:49  - viết kịch bản với chátGPT
3:59  - tạo hình ảnh với leonardo.ai
8:49  - tạo video với Runway ml.com
13:05 - chuyển văn bản thành giọng nói với Vbee voice studio
14:23 - edit video với CAPCUT PC
16:21 - KẾT THÚC
"""

"""
Link app trong video hướng dẫn:
👉 AI Leonardo: https://vantheweb.com/leonardo
👉 AI RUNWAY: https://vantheweb.com/runwayml/
👉 TTSMP3: https://ttsmp3.com/
👉 AI VBEE: https://vbee.vn/?aff=vantheweb/
👉 CapCut Pro PC 
"""