# ✨ NEW FEATURE: URL/File Path Detection

**Date: April 1, 2026**

---

## 🎯 What's New

The **"Enter URL or File Path"** input now supports **BOTH**:

- ✅ **Online Links** (URLs starting with http://, https://, ftp://)
- ✅ **Local File Paths** (C:\..., /home/..., ~/...)

The system **automatically detects** which one you're providing and handles it correctly!

---

## 📖 HOW IT WORKS

### **Step 1: User Input**

User pastes either:

```
https://arxiv.org/pdf/2110.12345.pdf           ← Online link
C:\Users\John\Papers\research.pdf              ← Windows path
/home/john/papers/research.pdf                 ← Linux/Mac path
~/research.pdf                                 ← Home shortcut
```

### **Step 2: Smart Detection**

The system checks:

```python
is_url = url_or_path.startswith(('http://', 'https://', 'ftp://'))
is_file_path = os.path.exists(url_or_path)
```

### **Step 3: Route to Handler**

- **If URL** → Use URL scraper (download & extract content)
- **If File Path** → Read file from disk

### **Step 4: Extract Content**

- PDF files → extract text
- Text files → read as-is
- Doc files → convert to text

### **Step 5: Analyze**

Same as always → extract metadata, keywords, plagiarism check, etc.

---

## ✅ SUPPORTED INPUTS

### **Online URLs** ✓

```
https://arxiv.org/pdf/2110.12345.pdf
https://scholar.google.com/scholar?id=abc...
https://researchgate.net/publication/123
https://example.com/paper.pdf
http://academic-site.edu/papers/study.pdf
https://proceedings.mlr.press/v139/doe21a.pdf
```

### **Local File Paths** ✓

**Windows:**

- `C:\Users\YourName\Documents\paper.pdf`
- `C:\Users\YourName\Desktop\research.pdf`
- `D:\papers\old_study.pdf`

**Mac/Linux:**

- `/home/username/papers/research.pdf`
- `/Users/john/Documents/paper.pdf`
- `~/papers/study.pdf` ← Home folder
- `~/Desktop/paper.pdf`

### **File Types**

- ✅ `.pdf` - PDF documents
- ✅ `.txt` - Plain text files
- ✅ `.doc` - Word documents
- ✅ `.docx` - Modern Word documents

### **What Won't Work**

- ❌ `.jpg`, `.png` - Images (use PDF upload instead)
- ❌ `.docm` - Macro-enabled docs
- ❌ Invalid paths (`C:\doesnt\exist\file.pdf`)
- ❌ Network paths that aren't accessible

---

## 🚀 USE CASES

### **Case 1: Analyze Paper from Web**

```
Input: https://arxiv.org/pdf/2301.12345.pdf
Result: System downloads PDF and analyzes it
Perfect for: Academic papers, conference proceedings
```

### **Case 2: Analyze Local PDF**

```
Input: C:\Users\John\Desktop\my_research.pdf
Result: System reads from disk and analyzes
Perfect for: Your own papers, local documents
```

### **Case 3: Analyze Text File**

```
Input: /home/john/papers/notes.txt
Result: System reads text and analyzes
Perfect for: Notes, exported text, plain documents
```

### **Case 4: Analyze Word Document**

```
Input: ~/Documents/paper_draft.docx
Result: System extracts text and analyzes
Perfect for: In-progress papers, drafts
```

---

## 🔍 DETECTION LOGIC

```
Input: "https://arxiv.org/pdf/123.pdf"
├─ Starts with http://? NO
├─ Starts with https://? YES ✓
└─ Route: URL Scraper → Download & Extract

Input: "C:\Users\John\paper.pdf"
├─ Starts with http/https/ftp? NO
├─ File exists at path? YES ✓
└─ Route: File Reader → Read from Disk

Input: "/nonexistent/path/paper.pdf"
├─ Starts with http/https/ftp? NO
├─ File exists at path? NO ✗
└─ Error: "File not found"

Input: "example.com/paper.pdf" (missing http://)
├─ Starts with http/https/ftp? NO
├─ File exists at path? NO ✗
└─ Error: "Invalid input"
```

---

## 🛠️ TECHNICAL DETAILS

### File Added Logic (in `views.py`)

```python
elif input_type == 'url':
    url_or_path = request.POST.get('url_input', '').strip()

    # Step 1: Detect input type
    is_url = url_or_path.lower().startswith(('http://', 'https://', 'ftp://'))
    is_file_path = os.path.exists(url_or_path)

    if is_url:
        # Handle online link
        result = url_scraper.scrape(url_or_path)
        content = result['content']

    elif is_file_path:
        # Handle local file
        file_ext = os.path.splitext(url_or_path)[1].lower()

        if file_ext == '.pdf':
            result = pdf_processor.extract_text(open(url_or_path, 'rb'))
            content = result['text']
        elif file_ext in ['.txt', '.doc', '.docx']:
            with open(url_or_path, 'r') as f:
                content = f.read()
    else:
        # Error: neither URL nor valid file path
        return error("Invalid input")
```

### Supported File Formats

| Format | Detection             | Handler                        |
| ------ | --------------------- | ------------------------------ |
| PDF    | `.pdf` extension      | `pdf_processor.extract_text()` |
| Text   | `.txt` extension      | `open()` with UTF-8            |
| Word   | `.doc`, `.docx`       | `open()` with UTF-8            |
| URL    | `http://`, `https://` | `url_scraper.scrape()`         |

---

## ⚠️ ERROR HANDLING

### **Error: File Not Found**

```
Input: C:\Users\John\nonexistent.pdf
Error: "File not found: C:\Users\John\nonexistent.pdf"
Solution: Check file path, ensure file exists
```

### **Error: File Too Small**

```
Input: C:\Users\john\notes.txt  ← Only 20 chars
Error: "File content is too short (minimum 50 characters)"
Solution: Provide larger documents
```

### **Error: Encoding Issues**

```
Input: C:\Users\john\file.txt  ← Non-UTF8 encoding
Error: "Could not read text file. Please ensure it UTF-8 encoded."
Solution: Save file as UTF-8 encoding
```

### **Error: Unsupported Format**

```
Input: C:\Users\john\image.jpg
Error: "Unsupported file type: .jpg. Supported: .pdf, .txt, .doc, .docx"
Solution: Use PDF upload button for images, or convert to PDF
```

### **Error: Invalid URL Format**

```
Input: example.com/paper.pdf  ← Missing http://
Error: "Invalid input: Please provide valid URL (http://...) or file path"
Solution: Add http:// prefix or use absolute file path
```

---

## 💡 EXAMPLES

### **Example 1: Analyze arXiv Paper**

Input:

```
https://arxiv.org/pdf/2301.12345v2.pdf
```

Output:

- Title: "Novel Deep Learning Architecture for NLP"
- Authors: "Smith et al."
- Abstract: [extracted]
- Keywords: [ML, NLP, Transformer, ...]
- Plagiarism: "0% - First paper in library"

---

### **Example 2: Analyze Local Paper**

Input:

```
C:\Users\Jane\Documents\my_research_2024.pdf
```

Output:

- Same analysis as Example 1
- Note: "Paper loaded from local path: my_research_2024.pdf"

---

### **Example 3: Analyze Text Draft**

Input:

```
~/Papers/draft_v3.txt
```

Content extracted from text file and analyzed same way

---

## 🎓 BEST PRACTICES

1. **Use Full Paths**
   - ✅ Good: `C:\Users\John\Desktop\paper.pdf`
   - ❌ Bad: `paper.pdf` (relative path might not work)

2. **Include Protocol for URLs**
   - ✅ Good: `https://arxiv.org/pdf/123.pdf`
   - ❌ Bad: `arxiv.org/pdf/123.pdf`

3. **Ensure Files Are Readable**
   - Check file exists
   - Check file isn't corrupted
   - Ensure you have read permissions

4. **Keep Files Reasonably Sized**
   - PDFs: Usually fine up to 100 MB
   - Text files: Full papers OK (typically 100 KB - 5 MB)

5. **Use Standard Paths**
   - Windows: Use full paths from drive letter
   - Unix: Use absolute paths or `~` for home

---

## 🧪 TESTING

Try these inputs:

### **Test 1: Online URL**

```
https://arxiv.org/pdf/2110.14575.pdf
Expected: Downloaded and analyzed ✓
```

### **Test 2: Local PDF (if you have one)**

```
C:\Users\YourName\Desktop\paper.pdf
Expected: Read from disk and analyzed ✓
```

### **Test 3: Invalid Path**

```
C:\invalid\path\paper.pdf
Expected: Error "File not found" ✓
```

### **Test 4: Missing Protocol**

```
arxiv.org/pdf/2110.14575.pdf
Expected: Error "Invalid input" ✓
```

---

## 📊 FLOW DIAGRAM

```
User Input (URL or Path)
        ↓
   Auto-Detect
   /         \
URL?       File Path?
 |            |
 ↓            ↓
Online     Local
Scraper    Reader
 |            |
 ├─PDF     ├─PDF
 ├─HTML    ├─TXT
 └─JSON    ├─DOC
           └─DOCX
        ↓
   Extract Content
        ↓
   Run Full Analysis
        ↓
   Save to Database
        ↓
   Display Result
```

---

## 🔐 SECURITY NOTES

- ✅ File paths only work for files you have access to
- ✅ URLs are fetched with proper SSL verification
- ✅ Content is stored in your personal library only
- ✅ No access to other users' files or system files

---

## 🆘 TROUBLESHOOTING

| Problem                           | Solution                             |
| --------------------------------- | ------------------------------------ |
| "File not found"                  | Use full absolute path, not relative |
| "Invalid input"                   | Add `http://` or `https://` to URL   |
| "File content too short"          | Use documents with >50 characters    |
| "Could not read text file"        | Save file as UTF-8 encoding          |
| URL appears to work but no result | File might be too large (>100MB)     |

---

## ✨ WHAT THIS ENABLES

- 🔗 Share papers by link (no download needed)
- 📁 Organize papers locally and analyze directly
- 🚀 Batch analyze from your computer
- 🌐 Mix online and local sources
- 📱 Works with academic URLs from any source

---

## 🎉 SUMMARY

This feature makes paper analysis **FLEXIBLE** and **INTELLIGENT**:

- Accepts URLs **OR** file paths
- Automatically detects which one you provided
- Routes to correct handler
- Extracts and analyzes
- All in **one simple input field**

No need to:

- Download files first
- Choose different buttons
- Know whether it's URL or path

Just paste or type, **and let the system figure it out!**
