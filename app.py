import streamlit as st
import yt_dlp
import os
import re
import tempfile
import shutil
from pathlib import Path


def is_valid_youtube_url(url: str) -> bool:
    """Validate if the provided URL is a valid YouTube URL."""
    youtube_regex = r'^(https?://)?(www\.)?(youtube\.com/(watch\?v=|embed/|v/|shorts/)|youtu\.be/)[\w-]+'
    return bool(re.match(youtube_regex, url.strip()))


def get_video_info(url: str) -> dict | None:
    """Fetch video metadata without downloading."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'channel': info.get('channel', info.get('uploader', 'Unknown')),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', ''),
            }
    except Exception as e:
        st.error(f"Error fetching video info: {str(e)}")
        return None


def format_duration(seconds: int) -> str:
    """Convert seconds to human-readable duration."""
    if seconds < 0:
        return "Unknown"
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"


def format_views(count: int) -> str:
    """Format view count with commas."""
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M views"
    elif count >= 1_000:
        return f"{count / 1_000:.1f}K views"
    return f"{count:,} views"


def download_audio(url: str, quality: str, progress_callback=None) -> tuple[bytes, str] | None:
    """Download and extract audio from YouTube video."""
    
    quality_map = {
        '128 kbps': '128',
        '192 kbps': '192',
        '320 kbps': '320',
    }
    bitrate = quality_map.get(quality, '192')
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
            'outtmpl': output_template,
            'quiet': True,
            'no_warnings': True,
        }
        
        if progress_callback:
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if d.get('total_bytes'):
                        percent = d['downloaded_bytes'] / d['total_bytes']
                        progress_callback(percent * 0.7, "Downloading audio...")
                    elif d.get('total_bytes_estimate'):
                        percent = d['downloaded_bytes'] / d['total_bytes_estimate']
                        progress_callback(percent * 0.7, "Downloading audio...")
                elif d['status'] == 'finished':
                    progress_callback(0.7, "Converting to MP3...")
            
            ydl_opts['progress_hooks'] = [progress_hook]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'audio')
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'\s+', '_', safe_title)
        
        if progress_callback:
            progress_callback(0.9, "Processing file...")
        
        mp3_files = list(Path(temp_dir).glob('*.mp3'))
        if mp3_files:
            mp3_path = mp3_files[0]
            with open(mp3_path, 'rb') as f:
                audio_data = f.read()
            
            if progress_callback:
                progress_callback(1.0, "Complete!")
            
            return audio_data, f"{safe_title}.mp3"
        
        return None
        
    except Exception as e:
        st.error(f"Error downloading audio: {str(e)}")
        return None
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    st.set_page_config(
        page_title="YouTube to MP3 Extractor",
        page_icon="🎵",
        layout="centered"
    )
    
    st.title("🎵 YouTube to MP3 Extractor")
    st.markdown("Extract high-quality audio from any YouTube video")
    
    st.divider()
    
    url = st.text_input(
        "Enter YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Paste a valid YouTube video URL"
    )
    
    quality = st.selectbox(
        "Audio Quality",
        options=['128 kbps', '192 kbps', '320 kbps'],
        index=1,
        help="Higher quality means larger file size"
    )
    
    if url:
        if not is_valid_youtube_url(url):
            st.error("Please enter a valid YouTube URL")
        else:
            with st.spinner("Fetching video information..."):
                info = get_video_info(url)
            
            if info:
                st.divider()
                st.subheader("Video Information")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if info['thumbnail']:
                        st.image(info['thumbnail'], use_container_width=True)
                
                with col2:
                    st.markdown(f"**{info['title']}**")
                    st.caption(f"Channel: {info['channel']}")
                    st.caption(f"Duration: {format_duration(info['duration'])}")
                    if info['view_count']:
                        st.caption(format_views(info['view_count']))
                
                st.divider()
                
                if st.button("🎵 Extract Audio", type="primary", use_container_width=True):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    def update_progress(percent, status):
                        progress_bar.progress(percent)
                        status_text.text(status)
                    
                    result = download_audio(url, quality, update_progress)
                    
                    if result:
                        audio_data, filename = result
                        
                        st.success("Audio extracted successfully!")
                        
                        st.audio(audio_data, format='audio/mp3')
                        
                        st.download_button(
                            label="⬇️ Download MP3",
                            data=audio_data,
                            file_name=filename,
                            mime="audio/mpeg",
                            use_container_width=True
                        )
                    else:
                        st.error("Failed to extract audio. Please try again or use a different video.")
    
    st.divider()
    st.caption("Note: Please ensure you have the right to download and use the audio content.")


if __name__ == "__main__":
    main()
