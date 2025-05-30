import yt_dlp
import os

AUDIO_DIR = os.path.join(os.path.dirname(__file__), 'static', 'audio')

from datetime import datetime, timezone, timedelta

def fetch_playlist_videos(playlist_id, download_audio=False):
	url = f"https://www.youtube.com/playlist?list={playlist_id}"
	ydl_opts = {
		'quiet': True,
		'extract_flat': False,  # must be False to get video publish dates
		'skip_download': True,
		'save_cookie': False,
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)

	videos = info.get('entries', [])

	# Filter videos published in the last 7 days
	one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
	recent_videos = []

	for video in videos:
		upload_date = video.get('upload_date')
		if not upload_date:
			continue
		# Convert YouTube date string (e.g., '20250522') to datetime
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
		'outtmpl': AUDIO_OUTPUT_TEMPLATE,
		'cookiefile': '/etc/secrets/youtube_cookies.txt',
		'cookiesfrombrowser': None,
		'nocookiefile': False,
		'noplaylist': False,
		'quiet': True,
		'nooverwrites': True,
		'writethumbnail': False,
		'writeinfojson': False,
		'cachedir': False,
		'no_color': True,
		'progress_hooks': [],
		'consoletitle': False,
		'ignoreerrors': True,
		'source_address': None,
		'usenetrc': False,
		'usenetrc_all': False,
		'writeautomaticsub': False,
		'writedescription': False,
		'writelink': False,
		'writesubtitles': False,
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'noconfig': True,
		'save_cookie': False,  # <--- THIS is the key line to stop yt-dlp from trying to write
	}
	
	try:
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
		return True
	except Exception as e:
		print(f"Failed to download {video_id}: {e}")
		return False