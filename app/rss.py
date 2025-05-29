from feedgen.feed import FeedGenerator
from datetime import datetime, timezone
import os

def generate_rss_feed(videos, playlist_id, public_base_url):
	fg = FeedGenerator()
	fg.title(f"YouTube Playlist {playlist_id}")
	fg.link(href=f"https://www.youtube.com/playlist?list={playlist_id}", rel='alternate')
	fg.description("Auto-generated podcast feed from YouTube audio")

	for video in videos:
		video_id = video.get('id')
		title = video.get('title')

		fe = fg.add_entry()
		fe.title(title)
		fe.link(href=f"https://www.youtube.com/watch?v={video_id}")
		fe.guid(video_id)

		# Fallback publish time
		fe.pubDate(datetime.utcnow().replace(tzinfo=timezone.utc))

		# Add enclosure
		audio_url = f"{public_base_url}/static/audio/{video_id}.mp3"
		local_path = os.path.join(os.path.dirname(__file__), 'static', 'audio', f"{video_id}.mp3")

		if os.path.exists(local_path):
			fe.enclosure(audio_url, 0, 'audio/mpeg')

	return fg.rss_str(pretty=True)