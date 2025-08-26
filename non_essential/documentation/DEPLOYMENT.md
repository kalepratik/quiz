# 🚀 Deployment Guide - dbt Certification Quiz

## Overview
This guide will help you deploy the dbt Certification Quiz application to production using Render.

## Prerequisites
- GitHub repository with your code
- Render account (free tier available)
- Google OAuth credentials (for authentication)
- Razorpay account (for payments)

## 🎯 Quick Deploy to Render

### Step 1: Prepare Your Repository
1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for production deployment"
   git push origin main
   ```

### Step 2: Deploy on Render
1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service**:
   - **Name**: `dbt-certification-quiz`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`
   - **Plan**: Free

### Step 3: Set Environment Variables
Add these environment variables in Render:

#### Required Variables:
```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-super-secret-production-key-here

# Google OAuth (Required for authentication)
GOOGLE_CLIENT_ID=your-google-client-id-here
GOOGLE_CLIENT_SECRET=your-google-client-secret-here

# Razorpay (Required for payments)
RAZORPAY_KEY_ID=your-razorpay-key-id-here
RAZORPAY_KEY_SECRET=your-razorpay-key-secret-here
```

#### Optional Variables:
```bash
# Python Version
PYTHON_VERSION=3.9

# Custom Domain (if you have one)
RENDER_EXTERNAL_URL=https://your-domain.com
```

## 🔧 Environment Setup

### Google OAuth Setup
1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project or select existing**
3. **Enable Google+ API**
4. **Create OAuth 2.0 credentials**:
   - Application type: Web application
   - Authorized redirect URIs: `https://your-app-name.onrender.com/auth/google/callback`
5. **Copy Client ID and Client Secret**

### Razorpay Setup
1. **Go to [Razorpay Dashboard](https://dashboard.razorpay.com/)**
2. **Create account or login**
3. **Go to Settings → API Keys**
4. **Generate API Keys** (use Live keys for production)
5. **Copy Key ID and Key Secret**

## 🚀 Deployment Steps

### 1. Update Google OAuth Redirect URI
After deployment, update your Google OAuth redirect URI to:
```
https://your-app-name.onrender.com/auth/google/callback
```

### 2. Test the Application
Once deployed, test these features:
- ✅ **Homepage**: `https://your-app-name.onrender.com/`
- ✅ **Quiz Interface**: `https://your-app-name.onrender.com/quiz`
- ✅ **Authentication**: `https://your-app-name.onrender.com/signin`
- ✅ **Payment Flow**: `https://your-app-name.onrender.com/payment`
- ✅ **Health Check**: `https://your-app-name.onrender.com/healthz`

### 3. Monitor Deployment
- **Check Render logs** for any errors
- **Monitor application health** via `/healthz` endpoint
- **Test all features** in production environment

## 🔒 Security Checklist

### Before Going Live:
- [ ] **Strong SECRET_KEY** set in environment variables
- [ ] **Production Razorpay keys** configured
- [ ] **Google OAuth redirect URI** updated for production
- [ ] **Debug mode disabled** (`FLASK_DEBUG=false`)
- [ ] **Environment set to production** (`FLASK_ENV=production`)
- [ ] **All sensitive data** moved to environment variables

### Security Best Practices:
- [ ] **Never commit secrets** to version control
- [ ] **Use HTTPS** (Render provides this automatically)
- [ ] **Regular security updates** for dependencies
- [ ] **Monitor application logs** for suspicious activity

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Build Failures
```bash
# Check if all dependencies are in requirements.txt
pip install -r requirements.txt
```

#### 2. Runtime Errors
- Check Render logs for error messages
- Verify environment variables are set correctly
- Test locally with production settings

#### 3. OAuth Issues
- Verify redirect URI matches exactly
- Check Google OAuth credentials
- Ensure HTTPS is used in production

#### 4. Payment Issues
- Verify Razorpay keys are correct
- Check if using live keys (not test keys)
- Test payment flow in production

### Debug Commands:
```bash
# Test application locally with production settings
FLASK_ENV=production python main.py

# Check environment variables
python -c "import os; print('FLASK_ENV:', os.getenv('FLASK_ENV'))"

# Test imports
python -c "from src.quiz_app import create_app; app = create_app(); print('App created successfully')"
```

## 📊 Monitoring & Maintenance

### Health Monitoring:
- **Health Check**: `/healthz` endpoint
- **Application Logs**: Available in Render dashboard
- **Performance**: Monitor response times and errors

### Regular Maintenance:
- **Update dependencies** regularly
- **Monitor security advisories**
- **Backup important data**
- **Review application logs**

## 🎉 Success!

Once deployed successfully:
- ✅ **Application is live** at your Render URL
- ✅ **Authentication works** with Google OAuth
- ✅ **Payments process** through Razorpay
- ✅ **Quiz functionality** is fully operational
- ✅ **All features** are production-ready

## 📞 Support

If you encounter issues:
1. **Check Render logs** first
2. **Verify environment variables**
3. **Test locally** with production settings
4. **Review this deployment guide**

---

**Happy Deploying! 🚀**
