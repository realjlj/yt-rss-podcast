from flask import Blueprint, request, Response
from .youtube import fetch_playlist_videos
from .rss import generate_rss_feed

main = Blueprint('main', __name__)

@main.route('/rss')
def rss_feed():
	playlist_id = request.args.get('playlist_id')
	if not playlist_id:
		return "Missing playlist_id", 400

	videos = fetch_playlist_videos(playlist_id)
	rss_xml = generate_rss_feed(videos, playlist_id)
	return Response(rss_xml, mimetype='application/rss+xml')