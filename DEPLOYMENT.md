# YouTube to MP3 Extractor - Deployment Guide

This document provides step-by-step instructions for deploying the YouTube to MP3 Extractor application.

---

## Part 1: Deploying on Replit

### Prerequisites
- A Replit account (free or paid)
- A valid `cookies.txt` file from your browser (for YouTube authentication)

### Step-by-Step Instructions

#### Step 1: Create a New Replit Project
1. Go to [replit.com](https://replit.com) and log in
2. Click the **+ Create Repl** button
3. Select **Python** as the template
4. Give your project a name (e.g., "youtube-mp3-extractor")
5. Click **Create Repl**

#### Step 2: Set Up the Project Files
1. Delete the default `main.py` file
2. Create the following files by copying the code from this repository:
   - `app.py` - Main application code
   - `cookies.txt` - Your YouTube cookies file
   - `.streamlit/config.toml` - Streamlit configuration

#### Step 3: Configure Streamlit
Create a folder called `.streamlit` and add a file named `config.toml` with:

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000
```

#### Step 4: Install Python Dependencies
In the Replit Shell, run:

```bash
pip install streamlit yt-dlp
```

Or update your `pyproject.toml` dependencies:

```toml
[project]
dependencies = [
    "streamlit>=1.40.0",
    "yt-dlp",
]
```

#### Step 5: Install FFmpeg System Dependency
FFmpeg is required for audio conversion. In Replit, add it via the Packages pane:
1. Click on the **Packages** icon in the left sidebar
2. Search for "ffmpeg" in the System Dependencies section
3. Click to install it

Alternatively, you can verify ffmpeg is available by running in the Shell:
```bash
ffmpeg -version
```

#### Step 6: Configure the Run Command
In your `.replit` file, ensure the deployment run command is set:

```toml
[deployment]
run = ["streamlit", "run", "app.py", "--server.port", "5000"]
```

#### Step 7: Add Your Cookies File
1. Export cookies from your browser using a browser extension like "Get cookies.txt" or "EditThisCookie"
2. Upload the `cookies.txt` file to your Replit project root
3. Make sure the file is in Netscape cookie format and contains valid YouTube session cookies

#### Step 8: Run the Application
1. Click the **Run** button in Replit
2. The application will start on port 5000
3. A webview will open showing your application

#### Step 9: Deploy (Publish)
1. Click the **Deploy** button in the top right
2. Select **Autoscale** deployment
3. Follow the prompts to publish your application
4. Your app will be available at `https://your-project-name.repl.app`

---

## Part 2: Vercel Deployment (Limited Functionality)

### Important Limitations

**Audio download functionality is NOT supported on Vercel** due to platform constraints:
- Vercel serverless functions have a 10-second execution timeout
- No persistent file storage between requests  
- FFmpeg and other system binaries are not available
- Audio conversion is not possible

The Vercel deployment only supports **fetching video information** (title, thumbnail, duration, etc.). For full download functionality, use Replit or Streamlit Community Cloud.

### If You Still Want to Deploy on Vercel

The repository includes a basic Flask API (`api/index.py`) and static frontend (`public/index.html`) for Vercel, but you'll need to complete the setup:

#### Step 1: Create requirements.txt
Create a file named `requirements.txt` in your project root with:

```
flask>=2.0.0
yt-dlp
```

#### Step 2: Push to GitHub
Push your code to a GitHub repository.

#### Step 3: Deploy on Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Vercel will auto-detect the configuration from `vercel.json`
4. Deploy

#### What Works on Vercel
- Fetching video metadata (title, thumbnail, duration, channel)
- URL validation

#### What Does NOT Work on Vercel
- Audio extraction and download
- MP3 conversion
- Any functionality requiring ffmpeg

---

## Part 3: Streamlit Community Cloud (Recommended Alternative)

Streamlit Community Cloud is the best free alternative for full functionality.

### Step-by-Step Instructions

1. Push your code to a **public** GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click **New app**
5. Select your repository and branch
6. Set the main file path to `app.py`
7. In **Advanced settings**, add your `cookies.txt` content as a secret
8. Click **Deploy**

### Adding Cookies as a Secret
In the Streamlit Cloud dashboard, go to your app settings and add a secret:
```toml
[cookies]
content = """
# Paste your cookies.txt content here
"""
```

Then modify your app to read from secrets when the file doesn't exist.

---

## About Databases

This application is **stateless** and does not require a database. Each download is processed independently without storing any user data or download history.

If you want to add features like download history or user accounts in the future, you can integrate a PostgreSQL database from services like Neon.tech, but this is not required for the core functionality.

---

## Troubleshooting

### Common Issues

**1. 403 Forbidden Error**
- Your `cookies.txt` file may be expired
- Export fresh cookies from your browser and replace the file
- Make sure you're logged into YouTube when exporting cookies

**2. FFmpeg Not Found**
- Ensure ffmpeg is installed as a system dependency
- On Replit: Use the Packages pane to install ffmpeg
- Verify with: `ffmpeg -version`

**3. Download Fails or Times Out**
- Some videos may have restrictions or be very long
- Try a shorter video to verify the app is working
- Check if your cookies are still valid

**4. Cookies.txt Not Working**
- Make sure the file is in Netscape cookie format (starts with `# Netscape HTTP Cookie File`)
- The file should be in the project root directory
- Try exporting cookies again from a fresh browser session

**5. "No audio formats found" Error**
- The video may not have audio available
- Try a different video

---

## File Structure

```
youtube-mp3-extractor/
├── app.py                 # Main Streamlit application
├── cookies.txt            # YouTube authentication cookies
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── api/
│   └── index.py           # Flask API for Vercel (limited functionality)
├── public/
│   └── index.html         # Static frontend for Vercel
├── vercel.json            # Vercel configuration
├── pyproject.toml         # Python dependencies (Replit)
├── .replit                # Replit configuration
├── replit.md              # Project documentation
└── DEPLOYMENT.md          # This file
```
