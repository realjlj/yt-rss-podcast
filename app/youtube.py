import yt_dlp
import os
from datetime import datetime, timezone, timedelta

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')
cookies_path = '/etc/secrets/youtube_cookies.txt'

def fetch_playlist_videos(playlist_id, download_audio=False):
	url = f"https://www.youtube.com/playlist?list={playlist_id}"
	ydl_opts = {
		'quiet': True,
		'extract_flat': False,
		'skip_download': True,
		'cookiefile': cookies_path,
		'save_cookie': False,
		'nocookiefile': True,
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.cookiejar.save = lambda *args, **kwargs: None
		info = ydl.extract_info(url, download=False)

	videos = info.get('entries', [])
	one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
	recent_videos = []

	for video in videos:
		upload_date = video.get('upload_date')
		if not upload_date:
			continue
		video_date = datetime.strptime(upload_date, '%Y%m%d').replace(tzinfo=timezone.utc)
		if video_date >= one_week_ago:
			video['parsed_date'] = video_date
			if download_audio:
				success = download_audio_file(video['id'])
				video['audio_downloaded'] = success
			recent_videos.append(video)

	return recent_videos

def download_audio_file(video_id):
	output_path = os.path.join(AUDIO_DIR, f"{video_id}.mp3")
	if os.path.exists(output_path):
		return True

	ydl_opts = {
		'format': 'bestaudio/best',
		'outtmpl': os.path.join(AUDIO_DIR, f"{video_id}.%(ext)s"),
		'cookiefile': cookies_path,
		'nocookiefile': True,  # ✅ important
		'quiet': True,
		'nooverwrites': True,
		'noconfig': True,
		'save_cookie': False,
		'nocookiefile': True,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
	}

	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.cookiejar.save = lambda *args, **kwargs: None
			ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
		return True
	except Exception as e:
		print(f"Failed to download {video_id}: {e}")
		return False