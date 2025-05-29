import yt_dlp

def fetch_playlist_videos(playlist_id):
	url = f"https://www.youtube.com/playlist?list={playlist_id}"
	ydl_opts = {
		'quiet': True,
		'extract_flat': True,
		'skip_download': True,
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		info = ydl.extract_info(url, download=False)

	return info.get('entries', [])