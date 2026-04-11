# YouTube Video Analysis Guide

## ✅ YouTube Support - ENABLED

Your PaperAIzer now supports analyzing YouTube videos! The backend was already configured with `yt-dlp` library to extract transcripts.

---

## How to Analyze YouTube Videos

### Method 1: From Home Page

1. Go to homepage
2. Click on **"URL/YouTube"** tab
3. Paste a YouTube URL:
   - Full URL: `https://www.youtube.com/watch?v=...`
   - Short URL: `https://youtu.be/...`
4. Click **"Analyze Paper"**
5. Wait for transcript extraction and analysis

### Method 2: From Upload Page

1. Go to `/upload/` page
2. Click **"URL/YouTube"** tab
3. Paste YouTube link in the URL field
4. Submit form

---

## What Gets Extracted from YouTube Videos

When you submit a YouTube link, the analysis automatically extracts:

✅ **Video Title** - Used as the analysis title  
✅ **Description** - Channel description/video summary  
✅ **Transcript/Subtitles** - Full auto-generated or manual subtitles (if available)  
✅ **Metadata** - Duration, uploader, upload date, view count, likes

### Example Output Analysis Includes:

- **Keywords**: Extracted from transcript (topics, technologies mentioned)
- **Summary**: Generated from full transcript
- **Research Gaps**: Identified from content
- **Technologies**: Mentioned frameworks/tools
- **Plagiarism Check**: Compare against your other papers
- **Word Count**: Transcript word count

---

## Supported YouTube Content

✅ **Supported:**

- Research paper presentations
- Academic lectures
- Tutorial videos
- Tech talks
- Webinars
- Conference presentations
- How-to educational videos

❌ **May Have Issues:**

- Age-restricted videos
- Private videos
- Removed videos
- Videos without subtitles (no transcript fallback)

---

## Example YouTube URLs to Test

```
🎥 AI Research Presentation:
https://www.youtube.com/watch?v=dQw4w9WgXcQ

📚 Academic Lecture:
https://youtu.be/jNQXAC9IVRw
```

---

## Troubleshooting

### "Could not extract transcript from this YouTube video"

- The video may not have subtitles available
- Try a different video with auto-generated captions enabled
- Or upload the paper as PDF/text instead

### "Request timed out"

- YouTube server is taking too long
- Wait a moment and try again
- Use a shorter video

### "Invalid URL"

- Make sure URL starts with `https://`
- Check that the video ID is correct
- Use full YouTube URL or youtu.be short link

---

## Features You Can Access After Analysis

After analyzing a YouTube video transcript, you can:

1. **View Results** - Full analysis with keywords, summary, technologies
2. **Compare** - Compare this video's content with other papers/videos
3. **Export** - Download analysis as PDF, JSON, or CSV
4. **Plagiarism Check** - See similarity with your other papers
5. **Add to Library** - Keep video analysis in your personal library

---

## Tips for Best Results

1. **Choose High-Quality Videos** - More complete transcripts = better analysis
2. **Academic Content** - Research talks, lectures, webinars work best
3. **Full Length** - Longer videos have more comprehensive transcripts
4. **Subtitles Enabled** - Ensure video has auto-generated or manual captions

---

## Behind the Scenes

**Technology Stack:**

- `yt-dlp` - Extracts video metadata and transcripts
- `pytesseract/Pillow` - For any visual text in thumbnails
- `nltk` - NLP analysis of transcript
- `transformers` - keyword and summary extraction

**Data Pipeline:**

1. URL → Video metadata fetched
2. Transcript extracted (English priority)
3. If no transcript, description used
4. NLP analysis runs on extracted text
5. Keywords, summary, technologies identified
6. Results displayed with plagiarism check

---

## Next Steps

✅ Go to [home page](/home/) and try it now!
✅ Click the **URL/YouTube** tab
✅ Paste a YouTube video link
✅ Watch the analysis happen! 🚀

---

_Last Updated: April 6, 2026_
