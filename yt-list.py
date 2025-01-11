import sys
import yt_dlp
import browser_cookie3
import tempfile
from pathlib import Path

# 固定配置
PROXY_URL = "http://127.0.0.1:10809"

def get_playlist_info(playlist_url):
    """
    获取播放列表中的所有视频信息
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'proxy': PROXY_URL,
        'cookiefile': 'cookies.txt',
    }
    
    videos_info = []
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if 'entries' in playlist_info:
                for index, entry in enumerate(playlist_info['entries'], 1):
                    if entry:
                        video_url = f"https://www.youtube.com/watch?v={entry['id']}"
                        
                        # 优先使用中文标题
                        title = get_preferred_title(entry)
                        
                        videos_info.append({
                            'index': index,
                            'title': title,
                            'url': video_url
                        })
            
            return videos_info
    except Exception as e:
        print(f"获取播放列表时出错: {str(e)}")
        return []

def get_preferred_title(entry):
    """
    获取视频的优先标题，优先中文
    """
    # 默认标题
    title = entry.get('title', 'Unknown Title')
    
    # 检查是否有多语言支持
    if 'title_translations' in entry:
        translations = entry['title_translations']
        
        # 优先返回中文标题
        if 'zh-Hans' in translations:  # 简体中文
            return translations['zh-Hans']
        elif 'zh-Hant' in translations:  # 繁体中文
            return translations['zh-Hant']
    
    return title  # 如果没有中文，则返回默认标题

def save_to_file(videos_info, output_file='playlist_info.txt'):
    """
    将视频信息保存到文件
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("播放列表视频信息：\n")
            f.write("=" * 80 + "\n\n")
            
            for video in videos_info:
                f.write(f"{video['index']:03d}. {video['title']}\n")
                f.write(f"    URL: {video['url']}\n")
                f.write("-" * 80 + "\n")
                
        print(f"信息已保存到文件: {output_file}")
        return True
    except Exception as e:
        print(f"保存文件时出错: {str(e)}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python script.py <YouTube视频链接>")
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    output_file = "playlist_info.txt"
    
    # 获取播放列表信息
    print("正在获取播放列表信息...")
    videos_info = get_playlist_info(playlist_url)
    
    if not videos_info:
        print("没有找到视频或获取播放列表失败")
        return
    
    print(f"找到 {len(videos_info)} 个视频")
    
    # 保存信息到文件
    if save_to_file(videos_info, output_file):
        print("处理完成！")
    else:
        print("保存文件失败！")

if __name__ == "__main__":
    main()
