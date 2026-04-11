# 🔧 CRITICAL FIXES - Real Data & Functionality

## Overview

Converting the application from demo/mock data to **REAL working functionality** with actual data extraction and analysis.

---

## 🚨 PRIORITY FIXES (Critical - Breaking Issues)

### 1. Profile Page Error - ADD LOGIN REQUIRED

**Issue:** Profile page shows error when accessed without login

**Fix:** Add `@login_required` decorator to profile view

**Location:** `analyzer/views.py` line 477

**Current:**

```python
def profile(request):
    """User profile page"""
```

**Should be:**

```python
@login_required(login_url='login')
def profile(request):
    """User profile page"""
```

---

### 2. Library - Add User Filter (SECURITY)

**Issue:** All users see all documents (critical privacy issue)

**Location:** `analyzer/views.py` line 330 in `library()` view

**Current code probably:**

```python
def library(request):
    documents = Document.objects.all()  # WRONG - all users see everything
```

**Should be:**

```python
@login_required(login_url='login')
def library(request):
    documents = Document.objects.filter(user=request.user).order_by('-created_at')
```

---

## 📥 ADD EXPORT/DOWNLOAD FUNCTIONALITY

### 3. Library - Add Download Result PDF

**Add to library.html results table** (each row needs download button):

```html
<a
  href="{% url 'download_result' document.id 'pdf' %}"
  class="btn-sm btn-primary"
  title="Download as PDF"
>
  <i class="fas fa-download"></i>
</a>
```

### 4. Library - Add Export Result Text

```html
<a
  href="{% url 'download_result' document.id 'txt' %}"
  class="btn-sm btn-secondary"
  title="Export as Text"
>
  <i class="fas fa-file-text"></i>
</a>
```

### 5. Library - Add Print Option

```html
<a
  href="#"
  onclick="printResult({{ document.id }})"
  class="btn-sm btn-info"
  title="Print"
>
  <i class="fas fa-print"></i>
</a>
```

### 6. Result Page - Add Export/Download Buttons

**The result.html already has buttons, but we need to ensure downloads work:**

Add to `urls.py`:

```python
path('download/<int:doc_id>/<str:format>/', views.download_result, name='download_result'),
```

Add to `views.py`:

```python
@login_required
def download_result(request, doc_id, format):
    """Download analysis result in specified format"""
    doc = get_object_or_404(Document, id=doc_id, user=request.user)
    analysis = AnalysisResult.objects.filter(document=doc).first()

    if format == 'pdf':
        return export_manager.export_to_pdf(doc, analysis)
    elif format == 'txt':
        return export_manager.export_to_text(doc, analysis)
    else:
        return JsonResponse({'error': 'Invalid format'}, status=400)
```

---

## 📊 REAL DATA FOR DASHBOARD

### 7. Dashboard - Connect to Real Database

**Issue:** Dashboard shows static mock numbers

**Location:** `analyzer/views.py` line 496

**Update dashboard view:**

```python
@login_required(login_url='login')
def dashboard(request):
    """User dashboard with real stats"""
    documents = Document.objects.filter(user=request.user)
    analyses = AnalysisResult.objects.filter(document__user=request.user)

    # Real stats
    total_papers = documents.count()

    # Average plagiarism score from real data
    avg_plagiarism = analyses.aggregate(
        Avg('plagiarism_score')
    )['plagiarism_score__avg'] or 0.0

    # Count unique keywords
    all_keywords = ' '.join([a.keywords or '' for a in analyses])
    unique_keywords = len(set(all_keywords.split()))

    # Papers this month
    from django.utils import timezone
    now = timezone.now()
    this_month = documents.filter(
        created_at__year=now.year,
        created_at__month=now.month
    ).count()

    # Weekly activity (last 7 days)
    from datetime import timedelta
    weekly_data = []
    for i in range(6, -1, -1):
        date = now - timedelta(days=i)
        count = documents.filter(
            created_at__date=date.date()
        ).count()
        weekly_data.append(count)

    context = {
        'total_papers': total_papers,
        'avg_plagiarism': round(avg_plagiarism, 1),
        'unique_keywords': unique_keywords,
        'this_month': this_month,
        'documents': documents.order_by('-created_at')[:5],
        'weekly_data': weekly_data,  # For Chart.js
    }
    return render(request, 'analyzer/dashboard.html', context)
```

**Update dashboard.html template to use real data:**

```html
<!-- Replace mock stat cards with real data -->
<div class="stat-card">
  <div class="stat-value">{{ total_papers }}</div>
  <div class="stat-label">Total Papers</div>
</div>

<div class="stat-card">
  <div class="stat-value">{{ avg_plagiarism }}%</div>
  <div class="stat-label">Avg Plagiarism</div>
</div>

<div class="stat-card">
  <div class="stat-value">{{ unique_keywords }}</div>
  <div class="stat-label">Unique Keywords</div>
</div>

<div class="stat-card">
  <div class="stat-value">{{ this_month }}</div>
  <div class="stat-label">This Month</div>
</div>
```

**Update Chart.js to use real data:**

```javascript
<script>
    const weeklyData = {{ weekly_data|safe }};  // Real data from backend
    const ctx = document.getElementById('activityChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Papers Analyzed',
                data: weeklyData,
                borderColor: 'rgb(79, 70, 229)',
                backgroundColor: 'rgba(79, 70, 229, 0.1)',
                tension: 0.4,
                fill: true
            }]
        }
    });
</script>
```

---

## 📄 PROFILE PAGE - SHOW REAL DATA

### 8. Profile - Show Real Paper Count

**Current:** Profile might show static mock numbers

**Update profile view to pass real data:**

```python
@login_required(login_url='login')
def profile(request):
    """User profile page with real data"""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and email != request.user.email:
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.error(request, "Email already in use")
            else:
                request.user.email = email
                request.user.save()
                messages.success(request, "Profile updated successfully")
        return redirect('profile')

    # Get real paper data
    papers = Document.objects.filter(user=request.user).order_by('-created_at')
    paper_count = papers.count()

    context = {
        'documents': papers[:20],
        'paper_count': paper_count,
        'member_since': request.user.date_joined,
    }
    return render(request, 'analyzer/profile.html', context)
```

**Update profile.html to show:**

```html
<div class="stat-group">
  <div class="stat-item">
    <div class="stat-number">{{ paper_count }}</div>
    <div class="stat-label">Papers Analyzed</div>
  </div>
  <div class="stat-item">
    <div class="stat-date">{{ member_since|date:"M d, Y" }}</div>
    <div class="stat-label">Member Since</div>
  </div>
</div>
```

---

## 🔗 URL SCRAPER - FIX & IMPROVE

### 9. Add Google Scholar Support

**Issue:** URL scraper doesn't work with Google Scholar links

**Location:** `analyzer/url_scraper.py`

**Add Google Scholar handler:**

```python
def scrape_google_scholar(url):
    """
    Extract paper info from Google Scholar URL
    Example: https://scholar.google.com/scholar?q=...
    """
    try:
        # For Google Scholar, we'll use the query parameter
        import urllib.parse
        parsed = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(parsed.query).get('q', [''])[0]

        if query:
            # Try to get paper from the query
            # Note: Google Scholar might block scraping, use caution
            headers = {'User-Agent': 'Mozilla/5.0...'}
            response = requests.get(url, headers=headers, timeout=10)

            # Extract basic info from page
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.find('h3') or {}
            title_text = title.get_text(strip=True) if title else query

            return {
                'title': title_text,
                'content': f"Retrieved from Google Scholar: {query}",
                'source': 'Google Scholar',
                'url': url
            }
    except Exception as e:
        logger.error(f"Error scraping Google Scholar: {e}")

    return None
```

**Improve error messages:**

```python
def scrape_url(url):
    """Scrape content from various sources"""
    supported = ['arxiv.org', 'scholar.google.com', 'researchgate.net',
                 'github.com', 'medium.com', 'dev.to']

    if not any(domain in url for domain in supported):
        raise ValueError(
            f"Unsupported URL source. Supported: {', '.join(supported)}"
        )

    # ... rest of scraping logic
```

---

## 🔄 COMPARE PAGE - FIX & ADD UPLOAD

### 10. Compare Page - Add Upload Form for Comparison

**Issue:** Compare page doesn't have form to upload papers for comparison

**Update compare.html:**

Add form before the comparison results:

```html
<div class="card mb-4">
  <div class="card-header">
    <h5>Add Papers for Comparison</h5>
  </div>
  <div class="card-body">
    <form
      method="POST"
      action="{% url 'analyze_document' %}"
      enctype="multipart/form-data"
    >
      {% csrf_token %}
      <div class="row">
        <div class="col-md-6">
          <label>Upload PDF for Comparison</label>
          <input type="file" name="file" accept=".pdf" class="form-control" />
          <input type="hidden" name="input_type" value="pdf" />
        </div>
        <div class="col-md-6">
          <label>&nbsp;</label>
          <button type="submit" class="btn btn-primary w-100">
            <i class="fas fa-upload"></i> Upload & Analyze
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
```

### 11. Compare - Improve Comparison Algorithm

**Add real comparison logic to compare view:**

```python
@login_required(login_url='login')
def compare(request):
    """Compare two papers with real data"""
    documents = Document.objects.filter(user=request.user).order_by('-created_at')

    paper_a_id = request.GET.get('paper_a')
    paper_b_id = request.GET.get('paper_b')

    comparison = None
    if paper_a_id and paper_b_id:
        try:
            paper_a = documents.get(id=paper_a_id)
            paper_b = documents.get(id=paper_b_id)

            analysis_a = AnalysisResult.objects.filter(document=paper_a).first()
            analysis_b = AnalysisResult.objects.filter(document=paper_b).first()

            if analysis_a and analysis_b:
                # Extract real data
                tech_a = set((analysis_a.technologies or '').split(','))
                tech_b = set((analysis_b.technologies or '').split(','))
                common_tech = tech_a & tech_b

                keywords_a = set((analysis_a.keywords or '').split(',')[:10])
                keywords_b = set((analysis_b.keywords or '').split(',')[:10])
                common_keywords = keywords_a & keywords_b

                # Calculate similarity
                all_tech = tech_a | tech_b
                similarity = len(common_tech) / max(len(all_tech), 1) * 100

                comparison = {
                    'paper_a': {
                        'title': paper_a.title,
                        'authors': analysis_a.authors or [],
                        'publication': analysis_a.publication or 'N/A',
                        'dataset': analysis_a.dataset or 'Not mentioned',
                        'impact': analysis_a.impact or 'Not specified',
                        'goal': analysis_a.goal or 'Not specified',
                    },
                    'paper_b': {
                        'title': paper_b.title,
                        'authors': analysis_b.authors or [],
                        'publication': analysis_b.publication or 'N/A',
                        'dataset': analysis_b.dataset or 'Not mentioned',
                        'impact': analysis_b.impact or 'Not specified',
                        'goal': analysis_b.goal or 'Not specified',
                    },
                    'common': {
                        'technologies': list(common_tech)[:10],
                        'keywords': list(common_keywords)[:10],
                        'similarity': round(similarity, 1)
                    }
                }
        except Exception as e:
            logger.error(f"Comparison error: {e}")

    context = {
        'documents': documents,
        'comparison': comparison,
    }
    return render(request, 'analyzer/compare.html', context)
```

---

## 🎯 REAL PLAGIARISM DETECTION

### 12. Plagiarism - Real Cross-Reference Analysis

**Current Issue:** Plagiarism detection is AI-based assumption, not real cross-reference

**Real implementation requires:**

1. **Local Library Detection** - Check against uploaded papers:

```python
def check_plagiarism_against_library(document_content, user):
    """
    Check plagiarism against user's own papers
    """
    user_docs = Document.objects.filter(user=user).exclude(id=document.id)

    plagiarism_results = []
    for other_doc in user_docs:
        similarity = local_library_similarity(
            document_content[:5000],  # First 5000 chars
            other_doc.content[:5000]
        )
        if similarity > 30:  # 30% threshold
            plagiarism_results.append({
                'document': other_doc,
                'similarity': similarity
            })

    return plagiarism_results
```

2. **Public Database Integration** - For real plagarism, integrate with:
   - Academic paper databases (CrossRef, OpenAlex)
   - Previous student papers
   - Published research

3. **Plagiarism Score Calculation:**

```python
def calculate_plagiarism_score(document, analysis):
    """
    Real plagiarism calculation
    """
    # Check local library
    local_plagiarism = check_plagiarism_against_library(
        document.content,
        document.user
    )

    # Get max similarity from local check
    local_max = max(
        [p['similarity'] for p in local_plagiarism],
        default=0
    )

    # Weight factors:
    # - Local matches: 60%
    # - Paraphrasing detection: 25%
    # - Citation analysis: 15%

    plagiarism_score = (local_max * 0.6) + \
                       (detect_paraphrasing(document.content) * 0.25) + \
                       (analyze_citations(document.content) * 0.15)

    return min(100, round(plagiarism_score, 1))
```

---

## 📝 RESULT PAGE - SHOW REAL DATA

### 13. Result Page - Show Real Authors, Dataset, Impact

**Current issue:** Shows mock/placeholder data

**Ensure AnalysisResult model has these fields:**

```python
class AnalysisResult(models.Model):
    document = models.OneToOneField(Document, on_delete=models.CASCADE)

    # Real extracted data
    authors = models.JSONField(default=list)  # ['Author 1', 'Author 2']
    publication = models.CharField(max_length=255, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    dataset = models.TextField(blank=True)
    technologies = models.TextField(blank=True)
    methodology = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    goal = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    abstract = models.TextField(blank=True)
    summary = models.TextField(blank=True)

    # Images from PDF
    extracted_images = models.JSONField(default=list)  # ['path/to/img1.jpg', ...]

    # Plagiarism
    plagiarism_score = models.FloatField(default=0.0)
    plagiarism_matches = models.JSONField(default=list)
```

**Make sure ML extraction is complete:**

```python
# In ml_model.py - ensure these functions extract REAL data, not assumed

def extract_authors(text):
    """Extract real author names from paper"""
    # Look for patterns like "John Smith1, Jane Doe2"
    # Use NLP to identify author names
    return authors_list

def extract_publication_info(text):
    """Extract where paper was published, when"""
    # Look for journal name, conference, year
    return {
        'publication': publication_name,
        'year': year,
        'venue': venue
    }

def extract_dataset_names(text):
    """Extract real dataset names mentioned"""
    # Look for: "We used the MNIST dataset", "on the ImageNet dataset"
    return datasets_list

def extract_real_methodology(text):
    """Extract actual methodology used"""
    # Parse "We propose", "We use", "Our method"
    return methodology_description

def extract_impact_statement(text):
    """Extract real impact/contributions"""
    # Look for contribution statements
    return impact_statement
```

---

## 🖼️ IMAGES - Extract from PDFs

### 14. PDF Images - Actually Extract, Don't Just Count

**Issue:** Currently only counts images, doesn't extract

**Improve pdf_processor.py:**

```python
def extract_images(pdf_path, output_dir):
    """
    Extract actual images from PDF
    """
    import fitz  # PyMuPDF
    images_list = []

    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]

        # Get images on page
        images = page.get_images(full=True)

        for img_index, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            # Save image
            image_path = f"{output_dir}/page{page_num}_img{img_index}.png"
            pix.save(image_path)

            images_list.append({
                'path': image_path,
                'page': page_num,
                'caption': f"Figure {img_index + 1} from Page {page_num + 1}"
            })

    doc.close()
    return images_list
```

**Store extracted images in database:**

```python
analysis.extracted_images = [
    {'path': img['path'], 'caption': img['caption']}
    for img in extracted_imgs
]
analysis.save()
```

**Display in result.html:**

```html
{% if analysis.extracted_images %}
<div class="mb-4">
  <h5><i class="fas fa-images"></i> Extracted Images</h5>
  <div class="row">
    {% for img in analysis.extracted_images %}
    <div class="col-md-6 mb-3">
      <figure>
        <img
          src="{% url 'media_file' img.path %}"
          alt="{{ img.caption }}"
          class="img-fluid rounded"
        />
        <figcaption>{{ img.caption }}</figcaption>
      </figure>
    </div>
    {% endfor %}
  </div>
</div>
{% endif %}
```

---

## ✅ IMPLEMENTATION CHECKLIST

### Phase 1: Critical Fixes (Do This First)

- [ ] Add `@login_required` to profile view
- [ ] Add user filter to library view
- [ ] Fix library pagination
- [ ] Verify export buttons work

### Phase 2: Add Missing Features

- [ ] Add download/export/print buttons to library
- [ ] Add upload form to compare page
- [ ] Implement real comparison algorithm
- [ ] Fix URL scraper error messages

### Phase 3: Real Data Connection

- [ ] Update dashboard with real database queries
- [ ] Update profile with real paper counts
- [ ] Ensure result page shows real extracted data
- [ ] Test all stat calculations

### Phase 4: Advanced Features

- [ ] Extract images from PDFs
- [ ] Implement real plagiarism detection algorithm
- [ ] Add Google Scholar support
- [ ] Add author/publication extraction

### Phase 5: Quality & Testing

- [ ] Test all pages with real data
- [ ] Verify exports work properly
- [ ] Test responsive design
- [ ] User acceptance testing

---

## 🚀 QUICK START FOR FIXES

**Step 1:** Fix critical issues (5 minutes)

```bash
# Edit analyzer/views.py
# - Add @login_required to profile
# - Add user filter to library
```

**Step 2:** Add export/download (10 minutes)

```bash
# Edit library.html
# - Add download button
# - Add export button
# - Add print button
```

**Step 3:** Connect real data (30 minutes)

```bash
# Edit views.py
# - Update dashboard with real queries
# - Update profile with real data
# - Update compare with real algorithm
```

**Step 4:** Test everything

```bash
python manage.py runserver
# Test each page with real data
```

---

**Priority order: 1 → 2 → 3 → 4 → 5**
