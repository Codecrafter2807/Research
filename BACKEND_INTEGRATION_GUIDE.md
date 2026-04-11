# 🔧 Backend Integration Guide

Complete guide for finishing backend features for the new frontend pages.

---

## 1. Dashboard - Real Data Integration

**Current Status:** ✅ Frontend | ⏳ Backend (mock data)

### What needs to be done

The dashboard currently shows mock data. Need to query the database for real stats.

### Code to add in `analyzer/views.py`

```python
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.utils import timezone
from .models import Document, AnalysisResult
from datetime import timedelta

@login_required(login_url='login')
def dashboard(request):
    """
    Dashboard with user analytics
    """
    user = request.user
    user_docs = Document.objects.filter(user=user)

    # Total papers analyzed
    total_papers = user_docs.count()

    # Average plagiarism score
    avg_plagiarism = AnalysisResult.objects.filter(
        document__user=user
    ).aggregate(Avg('plagiarism_score'))['plagiarism_score__avg'] or 0.0

    # Unique keywords count (approximate)
    # This counts distinct keywords from all papers
    unique_keywords = len(set(' '.join([
        doc.keywords or '' for doc in user_docs
    ]).split()))

    # Papers this month
    now = timezone.now()
    this_month = user_docs.filter(
        created_at__year=now.year,
        created_at__month=now.month
    ).count()

    # Recent papers
    recent_papers = user_docs.order_by('-created_at')[:5]

    # Weekly activity data (last 7 days)
    weekly_data = []
    for i in range(6, -1, -1):
        date = now - timedelta(days=i)
        count = user_docs.filter(
            created_at__date=date.date()
        ).count()
        weekly_data.append(count)

    context = {
        'total_papers': total_papers,
        'avg_plagiarism': round(avg_plagiarism, 1),
        'unique_keywords': unique_keywords,
        'this_month': this_month,
        'recent_papers': recent_papers,
        'weekly_data': weekly_data,  # Pass to template
    }

    return render(request, 'analyzer/dashboard.html', context)
```

### Update `templates/analyzer/dashboard.html`

Replace the mock data in the chart initialization:

```html
<!-- In the script section, find the Chart.js code and replace data: -->
<script>
  const ctx = document.getElementById('activityChart').getContext('2d');
  const chart = new Chart(ctx, {
      type: 'line',
      data: {
          labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
          datasets: [{
              label: 'Papers Analyzed',
              data: {{ weekly_data|safe }},  {# Use real data from backend #}
              borderColor: 'var(--primary)',
              backgroundColor: 'rgba(79, 70, 229, 0.1)',
              tension: 0.4,
              fill: true
          }]
      },
      options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
              legend: { display: false }
          },
          scales: {
              y: { beginAtZero: true }
          }
      }
  });
</script>
```

### Update stat cards in template

```html
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

---

## 2. Library - Add User Filter

**Current Status:** ⏳ Shows all documents (security issue)

### Security Issue

Currently all users see all documents. This is a critical privacy bug.

### Fix in `analyzer/views.py`

Find the `library()` view and update it:

```python
def library(request):
    """
    Show all analyzed papers - FILTERED BY USER
    """
    if request.user.is_authenticated:
        # Only show documents for logged-in user
        documents = Document.objects.filter(user=request.user).order_by('-created_at')
    else:
        # Show public documents only (if your model supports this)
        documents = Document.objects.filter(is_public=True).order_by('-created_at')

    # Pagination
    paginator = Paginator(documents, 10)  # 10 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'documents': page_obj.object_list,
    }
    return render(request, 'analyzer/library.html', context)
```

### Update `templates/analyzer/library.html` to show pagination

```html
<!-- Add pagination buttons at bottom -->
<div class="pagination">
  {% if page_obj.has_previous %}
  <a href="?page=1">« First</a>
  <a href="?page={{ page_obj.previous_page_number }}">‹ Prev</a>
  {% endif %}

  <span class="current">
    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
  </span>

  {% if page_obj.has_next %}
  <a href="?page={{ page_obj.next_page_number }}">Next ›</a>
  <a href="?page={{ page_obj.paginator.num_pages }}">Last »</a>
  {% endif %}
</div>
```

---

## 3. Profile - Save Email Changes

**Current Status:** Form exists but doesn't save

### Code in `analyzer/views.py`

```python
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url='login')
def profile(request):
    """
    User profile page - view and edit
    """
    user = request.user

    if request.method == 'POST':
        new_email = request.POST.get('email')

        # Validate email
        if not new_email or '@' not in new_email:
            messages.error(request, 'Invalid email address')
        elif User.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, 'Email already in use')
        else:
            user.email = new_email
            user.save()
            messages.success(request, 'Email updated successfully!')

    # Get user's papers
    documents = Document.objects.filter(user=user).order_by('-created_at')

    # Get category counts for filters
    categories = {
        'all': documents.count(),
        'ai_ml': documents.filter(category='AI/ML').count(),
        'cv': documents.filter(category='Computer Vision').count(),
        'nlp': documents.filter(category='NLP').count(),
        'healthcare': documents.filter(category='Healthcare').count(),
    }

    # Get selected category
    category = request.GET.get('category', 'all')
    if category != 'all':
        documents = documents.filter(category=category)

    context = {
        'user': user,
        'documents': documents[:10],  # Show last 10
        'categories': categories,
        'selected_category': category,
    }

    return render(request, 'analyzer/profile.html', context)
```

### Update form in `templates/analyzer/profile.html`

Make sure the email input has the right name:

```html
<form method="POST" class="profile-form">
  {% csrf_token %}

  <div class="form-group">
    <label for="email">Email</label>
    <input
      type="email"
      name="email"
      id="email"
      value="{{ user.email }}"
      required
    />
  </div>

  <button type="submit" class="btn btn-primary">Save Changes</button>
</form>

<!-- Show messages -->
{% if messages %} {% for message in messages %}
<div class="alert alert-{{ message.tags }}">{{ message }}</div>
{% endfor %} {% endif %}
```

---

## 4. Contact Form - Email & Database

**Current Status:** Frontend form exists, but doesn't send emails

### Create model for storing submissions

Add to `analyzer/models.py`:

```python
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"

    class Meta:
        ordering = ['-created_at']
```

### Then run migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Add view in `analyzer/views.py`

```python
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

def contact(request):
    """
    Handle contact form submissions
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate
        if not all([name, email, subject, message]):
            return JsonResponse({'error': 'All fields required'}, status=400)

        if len(message) < 10:
            return JsonResponse({'error': 'Message must be at least 10 characters'}, status=400)

        try:
            # Save to database
            from .models import ContactMessage
            contact_msg = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )

            # Send email to admin
            send_mail(
                subject=f"Contact Form: {subject}",
                message=f"""
New message from {name} ({email}):

{message}

---
You can reply to: {email}
Message ID: {contact_msg.id}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL or settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            # Send confirmation to user
            send_mail(
                subject="We received your message",
                message=f"""
Hi {name},

Thank you for contacting us. We received your message and will get back to you within 24 hours.

Your message:
{message}

---
Paper Analyzer Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return JsonResponse({'success': 'Message sent! We\'ll reply soon.'})

        except Exception as e:
            return JsonResponse({'error': f'Failed to send: {str(e)}'}, status=500)

    return render(request, 'analyzer/contact.html')
```

### Configure email in `paper_analyzer/settings.py`

```python
# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Or your email provider
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')
ADMIN_EMAIL = 'admin@paperanalyzer.com'  # Or your admin email
```

### Update frontend form to handle AJAX

In `templates/analyzer/contact.html`, update the form handling:

```javascript
<script>
    document.getElementById('contactForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;

        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            const response = await fetch('{% url "contact" %}', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (response.ok) {
                showMessage('success', data.success);
                this.reset();
            } else {
                showMessage('error', data.error);
            }
        } catch (error) {
            showMessage('error', 'Failed to send message');
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    });

    function showMessage(type, text) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'}`;
        alertDiv.textContent = text;

        const form = document.getElementById('contactForm');
        form.parentNode.insertBefore(alertDiv, form);

        setTimeout(() => alertDiv.remove(), 5000);
    }
</script>
```

---

## 5. Forgot Password - Email Reset Link

**Current Status:** Form exists, but doesn't send reset email

### Code in `analyzer/views.py`

```python
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import uuid

def forgot_password(request):
    """
    Password reset - send email with link
    """
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            # Generate reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Build reset link
            reset_link = request.build_absolute_uri(
                reverse('reset_password_confirm', args=[uid, token])
            )

            # Send email
            send_mail(
                subject='Reset Your Paper Analyzer Password',
                message=f"""
Hi {user.first_name or user.username},

Click the link below to reset your password:
{reset_link}

This link expires in 24 hours.

If you didn't request this, ignore this email.

---
Paper Analyzer Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(
                request,
                'If this email exists, you\'ll receive a reset link shortly.'
            )

        except User.DoesNotExist:
            # For security, don't reveal if email exists
            messages.success(
                request,
                'If this email exists, you\'ll receive a reset link shortly.'
            )
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')

    return render(request, 'analyzer/forgot_password.html')

# Also add URL pattern in urls.py:
# path('reset-password/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm')

def reset_password_confirm(request, uidb64, token):
    """
    Handle password reset confirmation
    """
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth.tokens import default_token_generator

    if request.method == 'POST':
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                new_password = request.POST.get('password')
                confirm_password = request.POST.get('confirm_password')

                if not new_password or len(new_password) < 6:
                    messages.error(request, 'Password must be at least 6 characters')
                elif new_password != confirm_password:
                    messages.error(request, 'Passwords do not match')
                else:
                    user.set_password(new_password)
                    user.save()
                    messages.success(request, 'Password reset successful! Please login.')
                    return redirect('login')
            else:
                messages.error(request, 'Reset link expired')
        except Exception as e:
            messages.error(request, 'Invalid reset link')

    return render(request, 'analyzer/reset_password_confirm.html')
```

---

## 6. Compare Papers - Comparison Algorithm

**Current Status:** Frontend exists with mock data

### Code in `analyzer/views.py`

```python
@login_required(login_url='login')
def compare(request):
    """
    Compare two papers side by side
    """
    user = request.user
    user_documents = Document.objects.filter(user=user)

    paper_a_id = request.GET.get('paper_a')
    paper_b_id = request.GET.get('paper_b')

    comparison = None

    if paper_a_id and paper_b_id:
        try:
            paper_a = user_documents.get(id=paper_a_id)
            paper_b = user_documents.get(id=paper_b_id)

            # Get analysis results
            result_a = AnalysisResult.objects.filter(document=paper_a).first()
            result_b = AnalysisResult.objects.filter(document=paper_b).first()

            if result_a and result_b:
                # Extract technologies
                tech_a = set((result_a.technologies or '').split(','))
                tech_b = set((result_b.technologies or '').split(','))
                common_tech = tech_a & tech_b

                # Extract keywords
                keywords_a = set((result_a.keywords or '').split(',')[:10])
                keywords_b = set((result_b.keywords or '').split(',')[:10])
                common_keywords = keywords_a & keywords_b

                # Calculate similarity
                similarity = len(common_tech) / max(len(tech_a | tech_b), 1) * 100

                comparison = {
                    'paper_a': {
                        'title': paper_a.title,
                        'technologies': [t.strip() for t in tech_a if t.strip()],
                        'keywords': list(keywords_a)[:5],
                        'plagiarism': result_a.plagiarism_score,
                        'date': paper_a.created_at,
                    },
                    'paper_b': {
                        'title': paper_b.title,
                        'technologies': [t.strip() for t in tech_b if t.strip()],
                        'keywords': list(keywords_b)[:5],
                        'plagiarism': result_b.plagiarism_score,
                        'date': paper_b.created_at,
                    },
                    'common': {
                        'technologies': list(common_tech)[:5],
                        'keywords': list(common_keywords)[:5],
                        'similarity': round(similarity, 1),
                    }
                }
        except Exception as e:
            pass

    context = {
        'documents': user_documents.order_by('-created_at'),
        'comparison': comparison,
        'selected_a': paper_a_id,
        'selected_b': paper_b_id,
    }

    return render(request, 'analyzer/compare.html', context)
```

### Update template to show comparison

In `templates/analyzer/compare.html`:

```html
{% if comparison %}
<div class="comparison-results">
  <!-- Comparison table -->
  <table class="comparison-table">
    <tr>
      <th>Attribute</th>
      <th>Paper A: {{ comparison.paper_a.title }}</th>
      <th>Paper B: {{ comparison.paper_b.title }}</th>
    </tr>
    <tr>
      <td>Technologies</td>
      <td>{{ comparison.paper_a.technologies|join:", " }}</td>
      <td>{{ comparison.paper_b.technologies|join:", " }}</td>
    </tr>
    <tr>
      <td>Keywords</td>
      <td>{{ comparison.paper_a.keywords|join:", " }}</td>
      <td>{{ comparison.paper_b.keywords|join:", " }}</td>
    </tr>
    <tr>
      <td>Plagiarism Score</td>
      <td>{{ comparison.paper_a.plagiarism }}%</td>
      <td>{{ comparison.paper_b.plagiarism }}%</td>
    </tr>
    <tr>
      <td>Analyzed Date</td>
      <td>{{ comparison.paper_a.date|date:"M d, Y" }}</td>
      <td>{{ comparison.paper_b.date|date:"M d, Y" }}</td>
    </tr>
  </table>

  <!-- Overlap analysis -->
  <div class="overlap-analysis">
    <h3>Overlap Analysis</h3>
    <p class="similarity">
      {{ comparison.common.similarity }}% Technology Similarity
    </p>

    <div class="common-items">
      <h4>Common Technologies</h4>
      <div class="tech-list">
        {% for tech in comparison.common.technologies %}
        <span class="tech-badge">{{ tech }}</span>
        {% empty %}
        <p>No common technologies</p>
        {% endfor %}
      </div>
    </div>

    <div class="common-items">
      <h4>Common Keywords</h4>
      <div class="keyword-list">
        {% for keyword in comparison.common.keywords %}
        <span class="keyword-badge">{{ keyword }}</span>
        {% empty %}
        <p>No common keywords</p>
        {% endfor %}
      </div>
    </div>
  </div>
</div>
{% else %}
<div class="empty-state">
  <p>Select two papers to compare</p>
</div>
{% endif %}
```

---

## 7. Upload - Verify Integration

**Current Status:** Frontend complete, verify backend

### Test the upload endpoint

Make sure the form in `templates/analyzer/upload.html` POSTs to the right endpoint.

Verify in your existing code (should already be there):

```python
# In analyzers/urls.py - you should already have:
path('analyze/', views.analyze_document, name='analyze_document'),

# In analyze_document view - verify it handles:
# 1. POST requests
# 2. file uploads
# 3. text input
# 4. url parsing
```

---

## Installation & Configuration Summary

### 1. Install dependencies (if not already installed)

```bash
pip install django-crispy-forms  # for better form rendering
```

### 2. Update settings.py

```python
# Add to INSTALLED_APPS:
INSTALLED_APPS = [
    ...
    'crispy_forms',
]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# CSRF settings
CSRF_COOKIE_SECURE = False  # Set True in production
SESSION_COOKIE_SECURE = False  # Set True in production
```

### 3. Create .env file

```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Update URLs

```python
# Add to analyzer/urls.py:
path('reset-password/<uidb64>/<token>/', views.reset_password_confirm, name='reset_password_confirm'),
```

---

## Testing Each Integration

### Dashboard

```python
# Shell test
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from analyzer.models import Document
>>> user = User.objects.first()
>>> Document.objects.filter(user=user).count()
```

### Contact Form

1. Go to /contact/
2. Fill form
3. Submit
4. Check database: `SELECT * FROM analyzer_contactmessage`

### Compare

1. Create 2 documents
2. Go to /compare/
3. Select both
4. Verify comparison displays

---

## Deployment Checklist

- [ ] All email credentials in environment variables
- [ ] Database migrations run
- [ ] Static files collected: `python manage.py collectstatic`
- [ ] DEBUG = False in production
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled
- [ ] CSRF settings correct
- [ ] Email backend tested

---

**Follow this guide to complete all backend integrations!**
