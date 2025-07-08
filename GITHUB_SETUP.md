# GitHub Setup Instructions

Follow these steps to push your Operating Agreement Builder to GitHub:

## 1. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the "+" icon in the top right → "New repository"
3. Name it: `opag-builder`
4. Description: "Web app for creating LLC operating agreements with Word export"
5. Keep it public or private as preferred
6. **Don't** initialize with README (we already have one)
7. Click "Create repository"

## 2. Push Local Repository

Copy and run these commands:

```bash
cd "/Users/ahmedelhamawy/OpAgApp Builder/opag-builder"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/opag-builder.git

# Push to GitHub
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

## 3. Deploy to Netlify

### Automatic Deployment (Recommended)

1. Go to [Netlify](https://app.netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Choose "GitHub" and authorize if needed
4. Select your `opag-builder` repository
5. Configure:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/build`
6. Click "Deploy site"

### Manual Deployment (Alternative)

If you prefer to deploy without connecting GitHub:

```bash
# Build the frontend
cd frontend
npm run build

# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --prod --dir=build
```

## 4. Set Up Backend (Choose One)

### Option A: Heroku
```bash
cd backend
heroku create your-app-name-api
git push heroku main
```

### Option B: Railway
```bash
cd backend
railway login
railway init
railway up
```

### Option C: Local Development Only
Keep running locally with `python app.py`

## 5. Configure Frontend API URL

After deploying your backend:

1. Go to Netlify dashboard
2. Site settings → Environment variables
3. Add: `REACT_APP_API_URL` = `https://your-backend-url.com`
4. Redeploy site

## Quick Links

- Your repo will be at: `https://github.com/YOUR_USERNAME/opag-builder`
- Netlify site: `https://YOUR-SITE-NAME.netlify.app`
- Backend API: Depends on your hosting choice

## Next Steps

1. **Set up your Word template**:
   ```bash
   python setup_template.py "/Users/ahmedelhamawy/Downloads/ETFIG_TWO_Operating Agreement_Final_250312.docx"
   ```

2. **Test the application**:
   - Create a new agreement
   - Add members
   - Generate Word document
   - Verify formatting matches your template

3. **Customize** (optional):
   - Update colors in `frontend/src/App.tsx`
   - Add your logo
   - Modify form fields as needed

## Troubleshooting

- **Push rejected**: Make sure you're using the correct repository URL
- **Build failed on Netlify**: Check Node version compatibility
- **API connection issues**: Verify CORS settings and API URL

Need help? Check the main README.md for detailed documentation.