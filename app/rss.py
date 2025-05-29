from feedgen.feed import FeedGenerator
from datetime import datetime, timezone

def generate_rss_feed(videos, playlist_id):
	fg = FeedGenerator()
	fg.title(f"YouTube Playlist {playlist_id}")
	fg.link(href=f"https://www.youtube.com/playlist?list={playlist_id}", rel='alternate')
	fg.description("Auto-generated podcast feed from YouTube")

	for video in videos:
		fe = fg.add_entry()
		fe.title(video.get('title'))
		fe.link(href=f"https://www.youtube.com/watch?v={video.get('id')}")
		fe.guid(video.get('id'))
		fe.pubDate(datetime.utcnow().replace(tzinfo=timezone.utc))

	return fg.rss_str(pretty=True)