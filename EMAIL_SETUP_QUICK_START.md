# Email Setup - Quick Start Guide

## 🚨 Current Issue on Render

Your app is currently **NOT sending OTP emails**. The `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` environment variables are not set on Render.

This means when a user requests an OTP, it only gets logged to the console (visible in Render logs) instead of being emailed.

## ⚡ 5-Minute Setup on Render

### Step 1: Get Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Ensure 2-Step Verification is enabled
3. Select:
   - App: **Mail**
   - Device: **Windows Computer** (or your device)
4. Google will generate a 16-character password
5. Copy the entire password (including spaces)

**Example:** `abcd efgh ijkl mnop`

### Step 2: Set Environment Variables on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Select your **paper-analyzer** web service
3. Click **Environment** tab
4. Add these two variables:

```
EMAIL_HOST_USER: your-email@gmail.com
EMAIL_HOST_PASSWORD: abcd efgh ijkl mnop  (the 16-char password from Step 1)
```

5. Click **Save** - App will auto-redeploy
6. Wait for deployment to complete (~2 minutes)

### Step 3: Test the Setup

After deployment:

1. Go to https://research-nraq.onrender.com/forgot-password/
2. Enter your email address
3. Check your email inbox for the OTP (usually arrives within 10 seconds)
4. Enter the OTP to complete password reset

### Step 4: Check Logs if Email Doesn't Arrive

If no email:

1. Go to Render Dashboard → **paper-analyzer** → **Logs**
2. Look for one of these messages:
   - ✅ `"OTP email sent successfully"` - Email working!
   - ❌ `"LOCAL OTP SIMULATOR"` - Email NOT configured
   - ❌ `"Failed to send OTP email"` - Credentials wrong or connection error

## 📋 Local Development Setup

To test email locally before deploying:

### Option 1: Use Console (Email Goes to Console Output)

```bash
# No setup needed! OTP will print to console:
# =========================================
#   OTP FOR user@example.com: 123456
# =========================================
```

### Option 2: Set Real Email (Test With Live Email)

Create a `.env` file:

```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop  (16-char app password)
DEFAULT_FROM_EMAIL=PaperAIzer <your-email@gmail.com>
```

Run locally:

```bash
python manage.py runserver
```

Then test forgot password - OTP will be emailed to you!

### Option 3: Quick Email Test

```bash
python manage.py shell

# In Django shell:
from django.core.mail import send_mail
result = send_mail(
    'Test Email',
    'This is a test from PaperAIzer',
    'your-email@gmail.com',
    ['recipient@example.com'],
    fail_silently=False,
)
print(f"Emails sent: {result}")  # Should print: Emails sent: 1
```

If you get an error, check your credentials.

## 🔧 Troubleshooting
3. Check console for OTP
4. Go to http://localhost:8000/verify-otp/
5. Enter OTP
6. Set new password
7. Login with new password

### Step 5: Deploy to Render

1. Go to Render Dashboard
2. Select your service
3. Go to "Environment"
4. Add these variables:
   - `EMAIL_HOST` = `smtp.gmail.com`
   - `EMAIL_PORT` = `587`
   - `EMAIL_USE_TLS` = `True`
   - `EMAIL_HOST_USER` = your Gmail
   - `EMAIL_HOST_PASSWORD` = App password
   - `DEFAULT_FROM_EMAIL` = your email

5. Click "Save"
6. Service will auto-redeploy

---

## ✅ Verification Checklist

- [ ] Email credentials in .env
- [ ] Test email sends successfully
- [ ] Forgot password OTP arrives
- [ ] Can reset password with OTP
- [ ] Contact form saves messages
- [ ] Credentials added to Render
- [ ] Service redeployed on Render

---

## 🔧 Troubleshooting

### "SMTPAuthenticationError"
- Check Gmail app password is correct
- Verify 2FA is enabled on Gmail
- Try generating new app password

### "Connection refused"
- Check EMAIL_HOST and EMAIL_PORT
- Verify firewall allows SMTP
- Check EMAIL_USE_TLS is True

### "Email not received"
- Check spam folder
- Verify recipient email is correct
- Check logs for errors

### "Timeout"
- Increase EMAIL_TIMEOUT in settings.py
- Check internet connection
- Try different email provider

---

## 📧 Email Providers

### Gmail (Recommended)
- Free
- Reliable
- Easy setup
- 500 emails/day limit

### SendGrid
- 100 free emails/day
- Better for production
- More reliable

### AWS SES
- Pay-per-use
- Best for high volume
- More complex setup

---

## 🚀 Production Tips

1. **Use environment variables** - Never hardcode credentials
2. **Monitor email logs** - Check for delivery failures
3. **Set up alerts** - Get notified of email errors
4. **Test regularly** - Verify email still works
5. **Use transactional email service** - For production scale

---

**Setup Time:** ~5 minutes  
**Difficulty:** Easy ⭐
