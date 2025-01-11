import os
import sys
import yt_dlp

def download_video(video_url):
    """
    下载YouTube视频，合并音频，并使用cookies。
    如果字幕下载失败，继续下载视频和音频。
    """
    # 配置下载选项
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',  # 限制视频到1080p
        'merge_output_format': 'mp4',  # 输出格式为MP4
        'subtitleslangs': ['zh-Hans'],  # 下载所有语言的字幕
        'writeautomaticsub': True,  # 下载自动生成的字幕
        'embedsubtitles': True,  # 嵌入字幕
            
        'cookies': 'cookie.txt',  # 使用当前目录下的 cookie 文件
        'outtmpl': '%(title)s.%(ext)s',  # 输出文件名为视频标题
        'quiet': False,  # 显示下载过程
    }

    # 调用yt-dlp进行下载
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("下载完成！")
    except yt_dlp.utils.DownloadError as e:
        # 处理字幕下载失败的情况，仅下载视频和音频
        print(f"字幕下载失败: {e}，继续下载视频和音频...")
        ydl_opts['embedsubtitles'] = False  # 不嵌入字幕
        ydl_opts['writeautomaticsub'] = False  # 不下载自动生成的字幕
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            print("视频和音频下载完成！")
        except Exception as e:
            print(f"下载过程中发生错误: {e}")


def main():
    """
    主程序入口
    """
    if len(sys.argv) < 2:
        print("用法: python script.py <YouTube视频链接>")
        sys.exit(1)
    
    video_url = sys.argv[1]
    print(f"正在下载视频: {video_url}")
    download_video(video_url)


if __name__ == "__main__":
    main()
