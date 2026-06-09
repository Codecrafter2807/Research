# Database Data Loss Fix - SQLite to PostgreSQL Migration

## 🚨 The Problem

Your application is currently using **SQLite** (`db.sqlite3`) on **Render's free tier**. This causes your data to be **automatically deleted** every few minutes when:

1. **Container restarts** - Render's free tier has ephemeral storage that wipes files on restart
2. **New deployments** - The entire container is recreated
3. **Inactivity** - If your app goes idle, the free tier dyno spins down and data is lost

## ✅ The Solution

Use **PostgreSQL** instead of SQLite. Render provides a persistent PostgreSQL database that won't lose data.

### Your render.yaml Already Supports This!

Look at your `render.yaml` - it already has:
```yaml
- key: DATABASE_URL
  fromDatabase:
    name: paper-analyzer-db
    property: connectionString
```

This means you have (or should have) a PostgreSQL database service configured!

## 🔧 How to Fix It

### Step 1: Verify PostgreSQL is Set Up on Render
1. Go to your Render Dashboard
2. Check if you have a `paper-analyzer-db` PostgreSQL service
3. If not, create one:
   - Click "New" → "PostgreSQL"
   - Name: `paper-analyzer-db`
   - Plan: Free tier
   - Same region as your web service

### Step 2: Verify DATABASE_URL is Set
1. Go to your web service settings
2. Check Environment variables
3. Verify `DATABASE_URL` is present and points to your PostgreSQL service
4. It should look like: `postgresql://user:pass@hostname:5432/dbname`

### Step 3: Deploy with PostgreSQL
1. Push your latest code to GitHub
2. Render will automatically redeploy
3. On deployment, Django will:
   - Detect the `DATABASE_URL` environment variable
   - Use PostgreSQL instead of SQLite
   - Run migrations automatically (via Procfile release command)

### Step 4: Verify Data Persistence
Run these commands after deployment:

```bash
# Check database type
python manage.py migrate_to_postgresql

# Create a baseline of current data
python manage.py check_data_preservation --check

# Later, verify data is preserved
python manage.py check_data_preservation --compare
```

## 📋 New Management Commands

### `check_data_preservation`
Monitors your database integrity:

```bash
# Show current statistics
python manage.py check_data_preservation

# Save a baseline (run this first)
python manage.py check_data_preservation --check

# Compare with baseline to detect loss
python manage.py check_data_preservation --compare
```

### `migrate_to_postgresql`
Helps verify your database migration:

```bash
# Check current database type
python manage.py migrate_to_postgresql
```

## 🔍 Why This Happens

### SQLite Problems:
- **Ephemeral Storage**: Stored on disk in a container
- **Render Free Tier**: Container is recreated frequently
- **No Persistence**: Files are deleted when container stops

### PostgreSQL Benefits:
- **Persistent Storage**: Data stored on dedicated database server
- **Render Free Tier Support**: Free tier includes a free PostgreSQL database
- **Production Ready**: Suitable for production deployments
- **Scalable**: Can handle more data and concurrent connections

## ✨ Settings Updates

Your `settings.py` has been updated with:

1. **Database Warning**: Alerts if SQLite is used in production
2. **Session Persistence**: 30-day session cookies in database
3. **Connection Health Checks**: Ensures database connection is stable
4. **HTTPS Security**: Proper secure cookie settings

## 🧪 Local Development

Locally, you can still use SQLite for development. It only becomes an issue on Render.

To test with PostgreSQL locally:
```bash
# Set DATABASE_URL to test PostgreSQL connection
export DATABASE_URL="postgresql://user:password@localhost:5432/paper_analyzer_test"
python manage.py runserver
```

## 📊 Data Statistics Commands

After setting up PostgreSQL, you can run:

```bash
# See current database stats
python manage.py check_data_preservation

# Output will show:
# ✓ Database: PostgreSQL (your-host:5432)
# 📊 Current Data Statistics:
#   • Documents: X
#   • Analysis Results: Y
#   • Password Reset OTPs: Z
```

## ⚠️ Migration Notes

1. **No Manual Migration Needed**: Django handles database schema automatically
2. **Existing SQLite Data**: Won't be migrated automatically (new empty database)
3. **Data Re-entry**: You'll need to re-upload documents after switching databases
4. **One-Time Setup**: After PostgreSQL is set up, data will persist permanently

## 🆘 If You Still Lose Data

1. Check Render logs for database connection errors
2. Verify DATABASE_URL is correctly set
3. Run: `python manage.py check_data_preservation --compare`
4. Look for error messages in Render's dashboard

## 📚 Quick Reference

| Issue | Solution |
|-------|----------|
| Data deleted after minutes | Use PostgreSQL (not SQLite) |
| DATABASE_URL not set | Create PostgreSQL service on Render |
| Data loss despite PostgreSQL | Check database connection errors |
| Can't find database | Verify `paper-analyzer-db` exists in Render |

---

**Remember**: SQLite is only for local development. Always use PostgreSQL in production! 🚀
