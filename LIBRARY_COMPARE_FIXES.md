# 🔧 Library & Compare - Missing Functionality

## Library Page - Add Download/Export/Print Buttons

### 1. Update library.html table to add action buttons

In `templates/analyzer/library.html`, find the papers table and add action column with buttons.

**Add this to the table header:**

```html
<th>Actions</th>
```

**Add this to each table row:**

```html
<td>
  <div class="action-buttons">
    <a
      href="{% url 'download_result' doc.id 'pdf' %}"
      class="btn btn-sm btn-outline-primary"
      title="Download PDF"
    >
      <i class="fas fa-download"></i> PDF
    </a>
    <a
      href="{% url 'download_result' doc.id 'txt' %}"
      class="btn btn-sm btn-outline-secondary"
      title="Export Text"
    >
      <i class="fas fa-file-text"></i> TXT
    </a>
    <button
      onclick="printDocument({{ doc.id }})"
      class="btn btn-sm btn-outline-info"
      title="Print"
    >
      <i class="fas fa-print"></i> Print
    </button>
    <a
      href="{% url 'result' doc.id %}"
      class="btn btn-sm btn-primary"
      title="View Results"
    >
      <i class="fas fa-eye"></i> View
    </a>
  </div>
</td>
```

### 2. Add print function to library.html script

```html
<script>
  function printDocument(docId) {
    window.open("/result/" + docId + "/?print=true", "_blank");
  }
</script>
```

### 3. Add CSS for action buttons (in library.html style section)

```css
.action-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

@media print {
  .action-buttons {
    display: none;
  }
}
```

---

## Add Download/Export Endpoints

### 1. Add to `analyzer/urls.py`:

```python
path('download/<int:doc_id>/<str:fmt>/', views.download_result, name='download_result'),
```

### 2. Add to `analyzer/views.py`:

```python
from django.http import FileResponse
import os

@login_required(login_url='login')
def download_result(request, doc_id, fmt):
    """
    Download analysis result in PDF or TXT format
    """
    doc = get_object_or_404(Document, id=doc_id, user=request.user)
    analysis = AnalysisResult.objects.filter(document=doc).first()

    if not analysis:
        messages.error(request, "No analysis results found for this document")
        return redirect('library')

    try:
        if fmt.lower() == 'pdf':
            # Use existing export manager
            return export_manager.export_to_pdf(doc, analysis)
        elif fmt.lower() == 'txt':
            return export_manager.export_to_text(doc, analysis)
        else:
            return JsonResponse({'error': 'Invalid format'}, status=400)
    except Exception as e:
        logger.error(f"Download error: {e}")
        messages.error(request, f"Download failed: {str(e)}")
        return redirect('library')
```

---

## Compare Page - Fix Upload & Form

### 1. Add upload form to compare.html

Add this section before the comparison results:

```html
<div class="card mb-5">
  <div class="card-header bg-light">
    <h5 class="mb-0">
      <i class="fas fa-plus-circle me-2"></i>Upload Paper for Comparison
    </h5>
  </div>
  <div class="card-body">
    <form
      method="POST"
      action="{% url 'analyze_document' %}"
      enctype="multipart/form-data"
      id="compareUploadForm"
    >
      {% csrf_token %}

      <div class="row g-3">
        <div class="col-md-8">
          <label class="form-label"
            ><i class="fas fa-file-pdf me-2"></i>Upload PDF for
            Comparison</label
          >
          <input
            type="file"
            name="file"
            accept=".pdf"
            class="form-control"
            required
          />
          <input type="hidden" name="input_type" value="pdf" />
          <small class="form-text text-muted">Max 45MB PDF files</small>
        </div>
        <div class="col-md-4">
          <label class="form-label">&nbsp;</label>
          <button type="submit" class="btn btn-primary w-100">
            <i class="fas fa-upload me-2"></i>Upload & Analyze
          </button>
        </div>
      </div>
    </form>
  </div>
</div>
```

### 2. Update compare view in `analyzer/views.py`

Replace the existing compare function with this improved version:

```python
@login_required(login_url='login')
def compare(request):
    """Compare two papers side by side"""
    documents = Document.objects.filter(user=request.user).order_by('-created_at')

    paper_a_id = request.GET.get('paper_a')
    paper_b_id = request.GET.get('paper_b')

    comparison = None

    if paper_a_id and paper_b_id and paper_a_id != paper_b_id:
        try:
            paper_a = documents.get(id=paper_a_id)
            paper_b = documents.get(id=paper_b_id)

            analysis_a = AnalysisResult.objects.filter(document=paper_a).first()
            analysis_b = AnalysisResult.objects.filter(document=paper_b).first()

            if analysis_a and analysis_b:
                # Extract technologies
                tech_a = set([t.strip() for t in (analysis_a.technologies or '').split(',') if t.strip()])
                tech_b = set([t.strip() for t in (analysis_b.technologies or '').split(',') if t.strip()])
                common_tech = tech_a & tech_b

                # Extract keywords
                keywords_a = set([k.strip() for k in (analysis_a.keywords or '').split(',')[:10] if k.strip()])
                keywords_b = set([k.strip() for k in (analysis_b.keywords or '').split(',')[:10] if k.strip()])
                common_keywords = keywords_a & keywords_b

                # Calculate similarity percentage
                all_tech = tech_a | tech_b
                tech_similarity = len(common_tech) / max(len(all_tech), 1) * 100

                comparison = {
                    'paper_a': {
                        'id': paper_a.id,
                        'title': paper_a.title,
                        'authors': analysis_a.authors if analysis_a.authors else ['Unknown'],
                        'publication': analysis_a.publication or 'Not specified',
                        'methodology': analysis_a.methodology or 'Not specified',
                        'dataset': analysis_a.dataset or 'Not mentioned',
                        'impact': analysis_a.impact or 'Not specified',
                    },
                    'paper_b': {
                        'id': paper_b.id,
                        'title': paper_b.title,
                        'authors': analysis_b.authors if analysis_b.authors else ['Unknown'],
                        'publication': analysis_b.publication or 'Not specified',
                        'methodology': analysis_b.methodology or 'Not specified',
                        'dataset': analysis_b.dataset or 'Not mentioned',
                        'impact': analysis_b.impact or 'Not specified',
                    },
                    'common': {
                        'technologies': list(common_tech)[:10],
                        'keywords': list(common_keywords)[:10],
                        'similarity': round(tech_similarity, 1),
                    },
                    'different': {
                        'tech_a_only': list(tech_a - tech_b)[:5],
                        'tech_b_only': list(tech_b - tech_a)[:5],
                    }
                }
        except Exception as e:
            logger.error(f"Comparison error: {e}")
            messages.error(request, f"Comparison error: {str(e)}")

    context = {
        'documents': documents,
        'comparison': comparison,
        'selected_a': paper_a_id,
        'selected_b': paper_b_id,
    }

    return render(request, 'analyzer/compare.html', context)
```

### 3. Update compare.html comparison display section

Add this after the paper selection form:

```html
{% if comparison %}
<div class="comparison-results mt-5">
  <h4 class="mb-4">
    <i class="fas fa-balance-scale me-2" style="color: var(--primary);"></i>
    Comparison Results
  </h4>

  <!-- Similarity Score -->
  <div class="card mb-4">
    <div class="card-body text-center">
      <h6 class="text-muted mb-2">Technology Similarity</h6>
      <div style="font-size: 3rem; font-weight: 700; color: var(--primary);">
        {{ comparison.common.similarity }}%
      </div>
      <p class="text-muted mt-2">Based on extracted technologies and methods</p>
    </div>
  </div>

  <!-- Comparison Table -->
  <div class="card mb-4">
    <div class="card-body">
      <h6 class="mb-3">Paper Details</h6>
      <table class="table">
        <thead>
          <tr>
            <th>Aspect</th>
            <th>{{ comparison.paper_a.title|truncatechars:30 }}</th>
            <th>{{ comparison.paper_b.title|truncatechars:30 }}</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Authors</strong></td>
            <td>{{ comparison.paper_a.authors|join:", "|truncatechars:40 }}</td>
            <td>{{ comparison.paper_b.authors|join:", "|truncatechars:40 }}</td>
          </tr>
          <tr>
            <td><strong>Publication</strong></td>
            <td>{{ comparison.paper_a.publication }}</td>
            <td>{{ comparison.paper_b.publication }}</td>
          </tr>
          <tr>
            <td><strong>Methodology</strong></td>
            <td>{{ comparison.paper_a.methodology|truncatechars:40 }}</td>
            <td>{{ comparison.paper_b.methodology|truncatechars:40 }}</td>
          </tr>
          <tr>
            <td><strong>Dataset</strong></td>
            <td>{{ comparison.paper_a.dataset|truncatechars:40 }}</td>
            <td>{{ comparison.paper_b.dataset|truncatechars:40 }}</td>
          </tr>
          <tr>
            <td><strong>Impact</strong></td>
            <td>{{ comparison.paper_a.impact|truncatechars:40 }}</td>
            <td>{{ comparison.paper_b.impact|truncatechars:40 }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Common Elements -->
  <div class="row g-4">
    {% if comparison.common.technologies %}
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h6 class="card-title mb-3">
            <i class="fas fa-microchip me-2"></i>Common Technologies
          </h6>
          <div>
            {% for tech in comparison.common.technologies %}
            <span class="badge bg-primary me-2 mb-2">{{ tech }}</span>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>
    {% endif %} {% if comparison.common.keywords %}
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h6 class="card-title mb-3">
            <i class="fas fa-key me-2"></i>Common Keywords
          </h6>
          <div>
            {% for keyword in comparison.common.keywords %}
            <span class="badge bg-success me-2 mb-2">{{ keyword }}</span>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>
    {% endif %}
  </div>

  <!-- Differences -->
  <div class="row g-4 mt-4">
    {% if comparison.different.tech_a_only %}
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h6 class="card-title mb-3">Unique to Paper A</h6>
          <div>
            {% for tech in comparison.different.tech_a_only %}
            <span class="badge bg-warning me-2 mb-2">{{ tech }}</span>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>
    {% endif %} {% if comparison.different.tech_b_only %}
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h6 class="card-title mb-3">Unique to Paper B</h6>
          <div>
            {% for tech in comparison.different.tech_b_only %}
            <span class="badge bg-info me-2 mb-2">{{ tech }}</span>
            {% endfor %}
          </div>
        </div>
      </div>
    </div>
    {% endif %}
  </div>
</div>
{% endif %}
```

---

## Quick Implementation Steps

1. **Update library.html** to add action buttons (5 min)
2. **Add download_result view** to views.py (5 min)
3. **Add URL pattern** to urls.py (2 min)
4. **Update comparison view** with real data (10 min)
5. **Update compare.html** with upload form and better display (10 min)
6. **Test everything** (10 min)

Total: ~40 minutes to complete all features!
