# replit.md

## Overview

This is a YouTube to MP3 audio extractor application built with Streamlit. The application allows users to input YouTube URLs, validates them, fetches video metadata (title, duration, thumbnail, channel, view count, upload date), extracts audio, converts to MP3, and provides download functionality using yt-dlp and ffmpeg as the backend.

## Deployment Options

See `DEPLOYMENT.md` for detailed deployment instructions:
- **Replit**: Full functionality (recommended)
- **Vercel**: Limited to video info only (download not supported due to serverless limitations)
- **Streamlit Community Cloud**: Full functionality alternative

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - A Python-based web framework for building interactive data applications
- **Rationale**: Streamlit provides rapid prototyping capabilities with minimal frontend code, making it ideal for utility applications like video downloaders
- **UI Pattern**: Single-page application with form inputs for URL submission and display of video metadata

### Backend Architecture
- **Download Engine**: yt-dlp - A feature-rich command-line audio/video downloader
- **Rationale**: yt-dlp is the most actively maintained YouTube downloading library with broad format support and regular updates to handle YouTube changes
- **Pattern**: Synchronous processing with temporary file handling for downloads

### Data Flow
1. User submits YouTube URL via Streamlit input
2. URL validation using regex patterns (supports youtube.com, youtu.be, shorts, mobile URLs)
3. Metadata extraction via yt-dlp without downloading
4. Video download to temporary directory when requested
5. File served to user, then cleaned up

### File Handling
- Uses Python's `tempfile` module for temporary storage during downloads
- `pathlib.Path` for cross-platform file path handling
- Cleanup of temporary files after download completion

## External Dependencies

### Python Libraries
- **streamlit**: Web UI framework
- **yt-dlp**: YouTube video downloading and metadata extraction
- **Standard library**: `os`, `re`, `tempfile`, `shutil`, `pathlib`

### External Services
- **YouTube**: Video hosting platform (source of content)
- No database required - stateless application
- No authentication system - public access tool