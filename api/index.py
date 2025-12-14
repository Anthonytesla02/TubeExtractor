from flask import Flask, request, jsonify
import yt_dlp
import re
import os
from pathlib import Path

app = Flask(__name__)

def is_valid_youtube_url(url: str) -> bool:
    """Validate if the provided URL is a valid YouTube URL."""
    youtube_patterns = [
        r'^(https?://)?(www\.)?youtube\.com/watch\?.*v=[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/embed/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/v/[\w-]+',
        r'^(https?://)?(www\.)?youtube\.com/shorts/[\w-]+',
        r'^(https?://)?(www\.)?youtu\.be/[\w-]+(\?.*)?$',
        r'^(https?://)?(m\.)?youtube\.com/watch\?.*v=[\w-]+',
    ]
    url_stripped = url.strip()
    return any(re.match(pattern, url_stripped) for pattern in youtube_patterns)


def get_ydl_opts():
    """Get yt-dlp options with cookies if available."""
    opts = {
        'quiet': True,
        'no_warnings': True,
    }
    cookies_path = Path(__file__).parent.parent / 'cookies.txt'
    if cookies_path.exists():
        opts['cookiefile'] = str(cookies_path)
    return opts


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})


@app.route('/api/info', methods=['POST'])
def get_info():
    """Get video metadata without downloading."""
    data = request.get_json()
    url = data.get('url', '')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not is_valid_youtube_url(url):
        return jsonify({'error': 'Invalid YouTube URL'}), 400
    
    ydl_opts = get_ydl_opts()
    ydl_opts['extract_flat'] = False
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return jsonify({
                'success': True,
                'data': {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'channel': info.get('channel', info.get('uploader', 'Unknown')),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                }
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/download', methods=['POST'])
def download():
    """
    Note: Audio download functionality is limited on Vercel due to:
    - 10-second execution timeout for serverless functions
    - No persistent file storage
    - Limited system binaries (ffmpeg may not be available)
    
    For full download functionality, use Replit or Streamlit Cloud.
    """
    return jsonify({
        'error': 'Download functionality is not available on Vercel due to platform limitations. '
                 'Please use the Replit or Streamlit Cloud deployment for full functionality.',
        'alternatives': [
            'Deploy on Replit for full functionality',
            'Use Streamlit Community Cloud',
            'Self-host on a VPS with Docker'
        ]
    }), 501


if __name__ == '__main__':
    app.run(debug=True)
