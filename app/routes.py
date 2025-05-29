from flask import Blueprint, request, Response
from .youtube import fetch_playlist_videos
from .rss import generate_rss_feed
import os

main = Blueprint('main', __name__)

@main.route('/rss')
def rss_feed():
	playlist_id = request.args.get('playlist_id')
	if not playlist_id:
		return "Missing playlist_id", 400

	# Render gives you your public domain via environment variable
	base_url = os.environ.get("RENDER_EXTERNAL_URL", "http://localhost:5000")

	videos = fetch_playlist_videos(playlist_id, download_audio=True)
	rss_xml = generate_rss_feed(videos, playlist_id, public_base_url=base_url)
	return Response(rss_xml, mimetype='application/rss+xml')