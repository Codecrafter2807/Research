# 🧪 COMPREHENSIVE TESTING GUIDE - April 1, 2026

## Before Testing: Setup Required

```bash
# 1. Make sure server is running
cd c:\Users\sanjn\paper\paper_analyzer
python manage.py runserver

# 2. Navigate to: http://localhost:8000/
# 3. Create test account if needed
```

---

## TEST BATCH 1: Register Page (2 min)

### ✅ Test 1.1: No Early Errors

```
Goal: Verify validation messages don't show before user input
Steps:
  1. Go to http://localhost:8000/register
  2. LOOK AT: Do you see red error text? (should be NO)
  3. Do the password fields show "This password is too common" etc? (should be NO)

Expected: Clean form with no error messages
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 1.2: Errors Show on Invalid Input

```
Goal: Verify errors DO appear when user enters bad data
Steps:
  1. Enter username: "test"
  2. Enter password: "123"
  3. TAB out of field or type in another field
  4. LOOK AT: Does red error appear? (should be YES)

Expected: Error message appears when input violates validation
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 1.3: Valid Registration Works

```
Goal: Verify user can register with valid data
Steps:
  1. Username: "testuser123" (new, unique)
  2. Email: "test@example.com"
  3. Password: "SecurePass123!@#"
  4. Password Confirm: "SecurePass123!@#"
  5. Click Register
  6. LOOK AT: Do you get redirected to login or dashboard?

Expected: Registration succeeds, redirects to next page
Result: ✅ PASS or ❌ FAIL

Note: If username already exists, try: "testuser" + random numbers
```

---

## TEST BATCH 2: Upload from URL (5 min)

### ✅ Test 2.1: Google Scholar PDF URL

```
Goal: Test URL extraction of abstract, conclusion, summary
Steps:
  1. Login to dashboard
  2. Go to Upload (or analyze)
  3. Select "URL Input" tab
  4. Find a research paper URL, e.g.:
     - https://arxiv.org/pdf/2405.00000.pdf (any arxiv paper)
     - Or find from Google Scholar
  5. Paste URL
  6. Click Analyze
  7. Wait for processing...
  8. View Results

What to Check:
  ✅ Abstract appears (not empty)
  ✅ Conclusion appears (not empty)
  ✅ Summary appears (not empty, not just first paragraph)
  ✅ Text has line breaks (not all squished together)
  ✅ All text is readable paragraphs (not single line)

Expected: All data extracted cleanly
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 2.2: arXiv Paper

```
Goal: Test with another academic source
Steps:
  1. Go to https://arxiv.org/
  2. Copy a PDF link (e.g., https://arxiv.org/pdf/2308.xxxxx.pdf)
  3. Upload to analyzer
  4. Check results (same as Test 2.1)

Expected: Extracts abstract and conclusion
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 2.3: ResearchGate Link (Optional)

```
Goal: Test with non-PDF URL
Steps:
  1. Find a public ResearchGate paper link
  2. Paste HTML URL (not PDF)
  3. Analyze
  4. Check if any content extracted

Expected: Graceful handling, extraction if possible
Result: ✅ PASS or ❌ FAIL
```

---

## TEST BATCH 3: Upload from Local File Path (3 min)

### ✅ Test 3.1: Windows File Path (PDF)

```
Goal: Test local PDF file upload via path
Steps:
  1. Save a PDF to a known location, e.g.:
     C:\Users\sanjn\Downloads\test_paper.pdf
  2. Go to Upload → "Enter URL or File Path"
  3. Paste the full path:
     C:\Users\sanjn\Downloads\test_paper.pdf
  4. Click Analyze
  5. Wait for processing...

What to Check:
  ✅ System recognized it as file path (not trying to fetch as URL)
  ✅ File content extracted
  ✅ Abstract/Conclusion appear
  ✅ No "Connection Error" messages

Expected: File processed successfully
Result: ✅ PASS or ❌ FAIL

Note: Can also test with .txt, .doc, .docx files
```

### ✅ Test 3.2: Invalid Path Error Handling

```
Goal: Test error message for non-existent file
Steps:
  1. Enter fake path: C:\Users\sanjn\nonexistent\file.pdf
  2. Click Analyze

What to Check:
  ✅ Friendly error message appears
  ✅ Error clearly explains the problem
  ✅ User doesn't get server error

Expected: Clear error message
Result: ✅ PASS or ❌ FAIL
```

---

## TEST BATCH 4: Data Extraction Quality (5 min)

### ✅ Test 4.1: Abstract Extraction

```
Goal: Verify abstracts are found even if deep in document
Steps:
  1. Upload any paper
  2. Go to Results page
  3. Scroll to "Abstract" section
  4. LOOK AT: Is it 3-5 sentences? (good) or 1 sentence or ALL text?

Expected: Proper abstract (not too short, not entire paper)
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 4.2: Conclusion Extraction

```
Goal: Verify conclusions are found
Steps:
  1. Same paper from 4.1
  2. Scroll to "Conclusion" section (or "Conclusions & Future Work")
  3. LOOK AT: Is it 2-4 paragraphs? (good) or missing? or entire last section?

Expected: Proper conclusion section
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 4.3: Methodology Clearly Readable

```
Goal: Verify methodology has line breaks, not all squished
Steps:
  1. Same paper
  2. Scroll to "Methodology"
  3. LOOK AT: Can you read it easily? Is it formatted with paragraphs?

Expected: Readable paragraphs with proper spacing
Result: ✅ PASS or ❌ FAIL

Note: This was the main "formatting lost" bug being fixed
```

### ✅ Test 4.4: Keywords Extracted

```
Goal: Verify keyword extraction works
Steps:
  1. Same paper
  2. Scroll to "Key Concepts"
  3. LOOK AT: Are keywords relevant to paper? (not random words)

Expected: 10-20 relevant keywords
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 4.5: Research Gaps Found

```
Goal: Verify research gaps detection
Steps:
  1. Same paper
  2. Scroll to "Research Gaps & Future Work"
  3. LOOK AT: Are gaps listed? Related to the paper topic?

Expected: 1-3 gaps related to paper topic
Result: ✅ PASS or ❌ FAIL
```

---

## TEST BATCH 5: Plagiarism Detection (5 min)

### ✅ Test 5.1: First Upload Shows 0% (Not 100%)

```
Goal: Critical bug fix - first paper shouldn't show 100% plagiarism
Steps:
  1. Create a NEW user or clear library
  2. Upload first paper
  3. LOOK AT: Plagiarism shows 0%? or 100%?

Expected: Shows 0% (correct) or low % with message "no papers to compare"
Result: ✅ PASS or ❌ FAIL

This was a MAJOR BUG FIX - must pass!
```

### ✅ Test 5.2: Second Upload Compares Against First

```
Goal: Verify plagiarism detection actually compares
Steps:
  1. Upload second paper
  2. LOOK AT: Plagiarism % is realistic (1-50%)?

Expected: Shows comparison % not 100%
Result: ✅ PASS or ❌ FAIL
```

---

## TEST BATCH 6: Comparison Feature (10 min)

### ✅ Test 6.1: Comparison Page Loads

```
Goal: Access comparison page
Steps:
  1. Go to Library
  2. Select 2 papers from your uploaded list
  3. Click "Compare Papers"
  4. Wait 2-3 seconds

What to Check:
  ✅ Page loads (no 404 error)
  ✅ Shows Paper 1 title
  ✅ Shows Paper 2 title
  ✅ Shows comparison data (not empty)

Expected: Comparison results display
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 6.2: Common Keywords Shown

```
Goal: Verify keyword overlap calculation
Steps:
  1. View comparison (from Test 6.1)
  2. Look for "Common Keywords" section
  3. LOOK AT: Lists keywords both papers share?

Expected: Shows 1-5+ common keywords with %
Result: ✅ PASS or ❌ FAIL

Example output:
  Paper 1 Keywords: machine learning, neural networks, data
  Paper 2 Keywords: neural networks, deep learning, data
  Common: neural networks (67% overlap), data (67% overlap)
```

### ✅ Test 6.3: Unique Keywords Listed

```
Goal: Verify unique items per paper
Steps:
  1. Same comparison
  2. Look for "Unique Keywords" or similar
  3. LOOK AT: Does it show keywords unique to each paper?

Expected: Clearly identifies what's unique
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 6.4: Methods Comparison

```
Goal: Verify method comparison works
Steps:
  1. Same comparison
  2. Look for "Methods" or "Common Methods"
  3. LOOK AT: Shows methods from both? Common methods marked?

Expected: Methods comparison section
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 6.5: Research Gaps Shown

```
Goal: Verify gaps appear in comparison
Steps:
  1. Same comparison
  2. Look for "Research Gaps" section
  3. LOOK AT: Shows gaps from Paper 1 and Paper 2?

Expected: Gaps from both papers compared
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 6.6: Success Message

```
Goal: Verify completion message appears
Steps:
  1. Same comparison
  2. Look at top or bottom of page
  3. LOOK AT: Any success message? "Comparison completed" or similar?

Expected: User sees indication that comparison succeeded
Result: ✅ PASS or ❌ FAIL
```

---

## TEST BATCH 7: Dashboard & Profile (3 min)

### ✅ Test 7.1: Dashboard Shows Real Stats

```
Goal: Verify dashboard uses real data
Steps:
  1. Upload 2-3 papers
  2. Go to Dashboard
  3. LOOK AT:
     - "Papers Analyzed" count (should match uploaded, not hardcoded)
     - "Avg Plagiarism" (should be calculated, not always "15%")
     - "Recent Papers" list (should show YOUR papers, not mock)
     - "Weekly Activity" chart (should reflect your uploads)

Expected: All stats match real data
Result: ✅ PASS or ❌ FAIL
```

### ✅ Test 7.2: Profile Shows Real Data

```
Goal: Verify profile stats are real
Steps:
  1. Go to Profile
  2. LOOK AT:
     - Paper count (should match your uploads)
     - Plagiarism average (should be calculated)
     - Keywords count (should match actual extracted)

Expected: Real data matching dashboard
Result: ✅ PASS or ❌ FAIL
```

---

## SCORE TRACKING

```
Batch 1 (Register):      ___ / 3 tests ✅
Batch 2 (URL Upload):    ___ / 3 tests ✅
Batch 3 (File Path):     ___ / 2 tests ✅
Batch 4 (Extraction):    ___ / 5 tests ✅
Batch 5 (Plagiarism):    ___ / 2 tests ✅
Batch 6 (Comparison):    ___ / 6 tests ✅
Batch 7 (Dashboard):     ___ / 2 tests ✅

TOTAL SCORE:              ___ / 23 tests

TARGET: All tests ✅ PASS
```

---

## WHAT TO DO IF TESTS FAIL

### ❌ Register Page Still Shows Errors

```
Check: Is the CSS in register.html correct?
File: c:\Users\sanjn\paper\paper_analyzer\templates\analyzer\register.html
Look for: <style> section with .invalid-feedback
```

### ❌ URL Analysis Missing Sections

```
Check: Are ml_model.py changes applied?
File: c:\Users\sanjn\paper\paper_analyzer\analyzer\ml_model.py
Functions to verify: extract_abstract(), extract_conclusion()
Also check: url_scraper.py has separator='\n\n'
```

### ❌ Comparison Page 404

```
Check: Is URL routing added?
File: c:\Users\sanjn\paper\paper_analyzer\analyzer\urls.py
Look for: path('compare/papers/<int:doc1_id>/<int:doc2_id>/', views.compare_papers)
```

### ❌ Comparison Shows Weird Data

```
Check: Is compare_papers() function in views.py?
File: c:\Users\sanjn\paper\paper_analyzer\analyzer\views.py
Look for: def compare_papers(request, doc1_id, doc2_id):
Must return JsonResponse with comparison data
```

---

## 🎯 SUCCESS CRITERIA

All 8 original issues should be fixed:

1. ✅ Register page clean (no early errors)
2. ✅ URL abstract extracted
3. ✅ URL conclusion extracted
4. ✅ URL summary relevant
5. ✅ Image count honest (not misleading)
6. ✅ Comparison real (not static)
7. ✅ Methods shown in comparison
8. ✅ Gaps shown in comparison

If all tests PASS → Project is ready for production/deployment
If any test FAILS → See troubleshooting section above

---

## 📞 QUESTIONS DURING TESTING?

If you encounter issues:

1. Check the file mentioned in error message
2. Verify changes were applied correctly
3. Look for typos in code
4. Restart server (`Ctrl+C`, then `python manage.py runserver`)
5. Clear browser cache (Ctrl+Shift+Delete)

Good luck! 🚀
