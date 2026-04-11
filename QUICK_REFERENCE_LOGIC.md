# Quick Reference: NLP, Plagiarism & Library

## 🎯 What Each Component Does

### NLP Processor (`nlp_processor.py`)
**Purpose:** Extract and analyze text from papers

| Feature | How It Works | Output |
|---------|-------------|--------|
| **Title** | Regex pattern matching on first 5 lines | String (e.g., "Machine Learning Survey") |
| **Abstract** | 4 regex patterns + validation | String (100-3000 chars) |
| **Keywords** | Try labeled keywords → fallback TF-IDF | List of 10 terms |
| **Summary** | Score sentences by word frequency | String (50-150 chars) |
| **Technologies** | Keyword matching in 6 categories | String (e.g., "ML/AI: neural network, LSTM") |
| **Methodology** | Keyword matching in 6 types | String (e.g., "Experimental") |

### Plagiarism (`plagiarism.py`)
**Purpose:** Check similarity against user's library

| Function | Does | Returns |
|----------|------|---------|
| `local_library_similarity()` | Compares text against 50 other docs using sequence matching + n-grams | `{similarity_percent: 35.2, matches: [...], risk_level: "medium"}` |
| `text_quality_check()` | Detects suspicious patterns (repeated chars, low diversity) | `{quality_score: 85, is_suspicious: false, issues: [...]}` |
| `extract_key_phrases()` | Finds 4-word phrases appearing >5 times | List of phrases with occurrence counts |
| `comprehensive_plagiarism_check()` | Combines all checks | Combined originality score |

### Library Page (`library.html` + `views.py`)
**Purpose:** Store, search, browse user's papers

| Feature | Backend Logic | Frontend Logic |
|---------|---------------|----------------|
| **Display** | `select_related('analysis')` joins Document + AnalysisResult | Renders 12 cards per page |
| **Search** | `Q(title__icontains search) \| Q(content__icontains=search)` | 500ms debounce, resets to page 1 |
| **Filter** | `.filter(input_type=type)` | JavaScript updates URL params |
| **Delete** | Cascade delete via `on_delete=CASCADE` | `deleteInProgress` flag prevents spam |
| **Pagination** | `Paginator(docs, 12)` | Bootstrap pagination |

---

## 🔄 Data Flow: Upload → Analysis → Library

```
1. User uploads paper (PDF/Text/URL)
   ↓
2. Extract text content
   ↓
3. NLP PROCESSOR runs:
   • extract_title()
   • extract_abstract()
   • extract_keywords() [TF-IDF]
   • generate_summary()
   • detect_technologies()
   • detect_methodology()
   ↓
4. PLAGIARISM CHECK runs:
   • local_library_similarity()
   • text_quality_check()
   • extract_key_phrases()
   ↓
5. Save to Database:
   • Document (title, content, word_count, input_type)
   • AnalysisResult (keywords, summary, tech, methodology, etc.)
   • PlagiarismCheck (similarity_score, matched_sources)
   ↓
6. Display in Results page
   ↓
7. Show in Library (search, filter, sort, delete)
```

---

## 📊 Algorithm Details

### TF-IDF Keyword Extraction
```
TF-IDF = (Term Frequency) × (Inverse Document Frequency)

TF = How often term appears in document
IDF = How rare the term is across all documents

Result: Terms that are frequent in THIS paper but rare overall = keywords
```

**Parameters:**
- Max features: 100 terms analyzed
- Stop words: English common words removed
- N-gram range: 1-2 (single words + 2-word phrases)
- Min df: 1 (appear at least once)
- Max df: 0.8 (don't appear in >80% of texts)

### Similarity Calculation
```
Similarity Score = max(
    SequenceMatcher(text1, text2),
    n_gram_overlap(text1, text2)
)

Where:
- SequenceMatcher = Longest common substring ratio
- n_gram_overlap = Jaccard similarity of 3-word chunks
```

**Risk Levels:**
- **0-25%:** LOW (original work)
- **25-50%:** MEDIUM (review recommended)
- **50-100%:** HIGH (manual review required)

### Extractive Summary
```
1. Split text into sentences
2. Score each sentence:
   score = sum(word_frequency[word] for word in sentence)
3. Select top 3 sentences
4. Sort by original order
5. Limit to 150 characters
```

---

## 🗄️ Database Models

```python
Document
  ├─ user (FK)
  ├─ input_type: pdf|text|url
  ├─ title: string
  ├─ content: text (full paper)
  ├─ file: PDF file reference
  ├─ url: URL if from web
  ├─ word_count: integer
  ├─ created_at: timestamp
  └─ updated_at: timestamp

AnalysisResult (OneToOne → Document)
  ├─ summary: text
  ├─ abstract: text
  ├─ keywords: JSON list
  ├─ methodology: JSON list
  ├─ technologies: JSON list
  ├─ goal, impact, publication_year: strings
  ├─ extracted_links: JSON list
  ├─ dataset_names/links: JSON lists
  ├─ references: JSON list
  ├─ authors: JSON list
  ├─ word_count, unique_words: integers
  ├─ extras: JSON (methodology_summary, visual_assets, etc.)
  └─ created_at, updated_at: timestamps

PlagiarismCheck (FK → Document, CASCADE)
  ├─ similarity_score: float (0-1)
  ├─ matched_sources: JSON list
  └─ checked_at: timestamp

AnalysisFeedback (FK → Document, CASCADE)
  ├─ rating: string
  ├─ comment: text
  └─ created_at: timestamp
```

---

## ⚙️ URL/View Endpoints

```
GET  /library/               → Show library with search/filter
POST /delete/<id>/           → Delete document (CASCADE)
GET  /result/<id>/           → Show analysis results
```

**Library Query Params:**
```
?q=keyword              # Search in title/content
?type=pdf|text|url      # Filter by type
?sort=-created_at       # Sort (-created_at, created_at, title, -title, word_count)
?page=2                 # Pagination
```

---

## ✅ Verification Checklist

- [x] NLP uses only: nltk, scikit-learn, re (no heavy transformers)
- [x] Plagiarism checks local library only (not internet)
- [x] Library has pagination (12 items/page)
- [x] Delete uses cascade (1 query not 3+)
- [x] Search has debounce (500ms)
- [x] Keywords optional: labeled → TF-IDF
- [x] Similar text: sequence + n-gram combo
- [x] Risk level: 3 tiers (low/medium/high)

---

## 🎯 TL;DR

1. **NLP:** Lightweight text analysis (TF-IDF keywords, regex title/abstract)
2. **Plagiarism:** Compares paper against user's 50 most recent documents
3. **Library:** Paginated (12/page) search/filter interface with cascade delete

All components are **fast ⚡ and lightweight 💾**!
