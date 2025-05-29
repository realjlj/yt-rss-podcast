import yt_dlp
import os

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')

def fetch_playlist_videos(playlist_id, download_audio=False):
	url = f"https://www.youtube.com/playlist?list={playlist_id}"
	ydl_opts = {
		'quiet': True,
		'extract_flat': True,
		'skip_download': True,
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)

	videos = info.get('entries', [])

	if download_audio:
		for video in videos:
			video_id = video['id']
			download_audio_file(video_id)

	return videos

def download_audio_file(video_id):
	output_path = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
	if os.path.exists(output_path):
		return  # already downloaded

	ydl_opts = {
		'format': 'bestaudio/best',
		'quiet': True,
		'outtmpl': os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s"),
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([f"https://www.youtube.com/watch?v={video_id}"])