# CSRF Verification Failed - Fix

## 🚨 The Problem

You're seeing: **"Forbidden (403): CSRF verification failed. Request aborted."**

This happens because Django's CSRF protection is too restrictive and rejecting legitimate requests from your Render app.

## ✅ What I Fixed

### 1. **Enhanced CSRF_TRUSTED_ORIGINS**
Updated to accept requests from all Render subdomains:
```python
CSRF_TRUSTED_ORIGINS = [
    "https://research-nraq.onrender.com",
    "https://*.onrender.com",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
```

### 2. **Secure Cookie Settings**
Set to always be secure in production:
```python
SESSION_COOKIE_SECURE = True  # Always HTTPS
CSRF_COOKIE_SECURE = True     # Always HTTPS
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
```

### 3. **CSRF Failure Handler**
Added a graceful error handler that shows helpful messages:
```python
CSRF_FAILURE_VIEW = 'analyzer.views.csrf_failure'
```

## 🔍 How CSRF Protection Works

Django's CSRF (Cross-Site Request Forgery) protection works by:

1. **Token Generation**: Creates a unique token for each session
2. **Token Validation**: Checks token on POST/PUT/DELETE requests
3. **Origin Verification**: Ensures requests come from trusted sources
4. **Referer Check**: Verifies the request came from your domain

## 🧪 How to Verify CSRF is Working

### In Browser Console:
```javascript
// Check CSRF token is in the page
document.querySelector('[name=csrfmiddlewaretoken]').value

// Check cookies
document.cookie
```

### Check Server Logs:
```bash
# Look for CSRF success/failures
python manage.py runserver
# Watch for any CSRF-related warnings
```

## 🛠️ Common CSRF Issues & Solutions

| Problem | Cause | Solution |
|---------|-------|----------|
| 403 on form submission | Missing CSRF token | Add `{% csrf_token %}` to form |
| 403 on AJAX request | Token not sent | Add `X-CSRFToken` header |
| 403 from different domain | Origin not trusted | Add to `CSRF_TRUSTED_ORIGINS` |
| 403 after domain change | Old domain still cached | Clear browser cache/cookies |

## 📋 How to Fix CSRF in Your Templates

### For HTML Forms:
```html
<form method="POST" action="/your-endpoint/">
    {% csrf_token %}
    <!-- Your form fields -->
    <button type="submit">Submit</button>
</form>
```

### For AJAX Requests:
```javascript
// Method 1: Get token from DOM
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

// Method 2: Use fetch with headers
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCsrfToken(),
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

### For AJAX (jQuery):
```javascript
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:/.test(settings.url) || /^https:/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCsrfToken());
        }
    }
});
```

## 🔐 CSRF Token Lifetime

- **Default**: CSRF token is generated per session
- **Expires**: When user logs out or session expires
- **Renewed**: On each page load
- **Secure**: Never cached by browser

## 🚀 Production Checklist

- ✅ `CSRF_TRUSTED_ORIGINS` includes your domain
- ✅ `CSRF_COOKIE_SECURE = True` (HTTPS only)
- ✅ `DEBUG = False` (in production)
- ✅ All forms include `{% csrf_token %}`
- ✅ All AJAX requests include `X-CSRFToken` header
- ✅ Domain is in `ALLOWED_HOSTS`
- ✅ No `@csrf_exempt` on sensitive endpoints (unless necessary)

## 🆘 If You Still Get 403 Errors

1. **Clear browser cache and cookies**
2. **Check browser console for errors**
3. **Verify CSRF token is in page source**: `Ctrl+Shift+J`
4. **Check network tab**: Request headers for `X-CSRFToken`
5. **Enable DEBUG=True temporarily** to see error details
6. **Check Django logs** for CSRF failure reason
7. **Verify domain** matches `CSRF_TRUSTED_ORIGINS`

## 📊 CSRF Settings Reference

```python
# Basic CSRF Configuration
CSRF_COOKIE_SECURE = True           # Send token only over HTTPS
CSRF_COOKIE_HTTPONLY = True         # JavaScript cannot access token
CSRF_COOKIE_AGE = 31449600          # 1 year in seconds
CSRF_TRUSTED_ORIGINS = [...]        # List of trusted domains
CSRF_FAILURE_VIEW = 'app.views.csrf_error'  # Custom error handler

# Session Configuration
SESSION_COOKIE_SECURE = True        # Send session only over HTTPS
SESSION_COOKIE_HTTPONLY = True      # JavaScript cannot access session
SESSION_COOKIE_AGE = 2592000        # 30 days in seconds
SESSION_COOKIE_SAMESITE = 'Strict'  # Prevents cross-site cookie sending
```

## 🎯 Best Practices

1. **Always use HTTPS in production** (required for secure cookies)
2. **Never disable CSRF protection** unless absolutely necessary
3. **Use `@csrf_exempt` sparingly** (only for webhooks/APIs)
4. **Keep tokens fresh** - regenerate after login
5. **Test CSRF protection** - include in your test suite
6. **Monitor CSRF failures** - they might indicate attacks

## 📚 More Information

- [Django CSRF Protection](https://docs.djangoproject.com/en/stable/middleware/csrf/)
- [CSRF Token & Render](https://docs.render.com/deploy-django-app)
- [Web Security - CSRF Attacks](https://owasp.org/www-community/attacks/csrf)

---

**After these fixes, your CSRF errors should be resolved!** 🚀
