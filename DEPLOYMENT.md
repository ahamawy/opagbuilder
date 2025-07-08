# Deployment Guide

This guide covers deploying the Operating Agreement Builder to Netlify (frontend) and various backend hosting options.

## Frontend Deployment (Netlify)

### Prerequisites
- GitHub account
- Netlify account
- Backend API deployed and accessible

### Steps

1. **Push to GitHub**
   ```bash
   cd opag-builder
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/opag-builder.git
   git push -u origin main
   ```

2. **Connect to Netlify**
   - Log in to [Netlify](https://app.netlify.com)
   - Click "Add new site" → "Import an existing project"
   - Choose GitHub and authorize access
   - Select your repository

3. **Configure Build Settings**
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`

4. **Environment Variables**
   Add in Netlify dashboard:
   - `REACT_APP_API_URL`: Your backend API URL (e.g., `https://your-api.herokuapp.com`)

5. **Deploy**
   - Click "Deploy site"
   - Wait for build to complete
   - Your site will be live at `https://[your-site-name].netlify.app`

### Custom Domain (Optional)
1. Go to "Domain settings" in Netlify
2. Add your custom domain
3. Update DNS records as instructed

## Backend Deployment Options

### Option 1: Heroku

1. **Create Heroku App**
   ```bash
   cd backend
   heroku create opag-builder-api
   ```

2. **Add Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

3. **Configure Database**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Add Heroku config"
   git push heroku main
   ```

### Option 2: Railway

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

2. **Deploy**
   ```bash
   cd backend
   railway login
   railway init
   railway add
   railway up
   ```

3. **Add Database**
   - In Railway dashboard, add PostgreSQL service
   - Connect to your app

### Option 3: Render

1. **Create Web Service**
   - Go to [Render](https://render.com)
   - New → Web Service
   - Connect GitHub repo

2. **Configure**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add PostgreSQL**
   - New → PostgreSQL
   - Connect to your web service

## Backend Configuration

### Update Production Settings

1. **Database URL**
   Update `app.py` to use production database:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///opag.db')
   ```

2. **CORS Settings**
   Update allowed origins:
   ```python
   CORS(app, origins=['https://your-site.netlify.app'])
   ```

3. **Environment Variables**
   Set on your hosting platform:
   - `DATABASE_URL`: PostgreSQL connection string
   - `SECRET_KEY`: Random secret key
   - `FLASK_ENV`: production

### Database Migration

Run after deployment:
```bash
heroku run python -c "from app import db; db.create_all()"
```

## Template Upload

Since file uploads aren't persistent on most platforms, consider:

1. **Cloud Storage** (Recommended)
   - Use AWS S3 or similar
   - Update `document_generator.py` to fetch from cloud

2. **Include in Repository**
   - Add templates to git
   - Remove from `.gitignore`

3. **Database Storage**
   - Store templates as binary in database
   - Modify code to read from DB

## Monitoring

### Frontend (Netlify)
- Analytics available in Netlify dashboard
- Set up form notifications if needed

### Backend
- Use platform's logging (e.g., `heroku logs --tail`)
- Consider adding Sentry for error tracking

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Verify `REACT_APP_API_URL` is set correctly
   - Check CORS configuration in backend

2. **Database Connection**
   - Ensure `DATABASE_URL` is set
   - Check database credentials

3. **Template Not Found**
   - Verify templates are included in deployment
   - Check file paths in production

4. **Build Failures**
   - Check Node/Python versions
   - Verify all dependencies in requirements.txt/package.json

### Debug Commands

```bash
# Netlify
netlify dev  # Test locally with Netlify CLI

# Heroku
heroku logs --tail
heroku run python app.py

# Railway
railway logs
railway run python app.py
```

## Performance Optimization

1. **Frontend**
   - Enable Netlify's asset optimization
   - Use lazy loading for routes
   - Optimize images

2. **Backend**
   - Add caching headers
   - Use connection pooling
   - Implement pagination

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS (automatic on Netlify/Heroku)
- [ ] Validate all user inputs
- [ ] Implement rate limiting
- [ ] Regular dependency updates
- [ ] Backup database regularly

## Continuous Deployment

### Netlify
- Automatic deploys on push to main branch
- Preview deploys for pull requests

### Backend (GitHub Actions)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy Backend
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "opag-builder-api"
          heroku_email: "your-email@example.com"
          appdir: "backend"
```