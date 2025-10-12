# 🚀 Streamlit Patient Queue Simulator - Deployment Guide

This guide provides multiple options for deploying your Streamlit Patient Queue Simulator application.

## 📋 Project Overview

Your application includes:
- **Main App**: `Simulator.py` - Patient queue simulation with statistical analysis
- **Pages**: 
  - `pages/Gantt_chart.py` - Gantt chart visualization
  - `pages/Queuing Calculator.py` - Queueing theory calculator
- **Dependencies**: Listed in `requirements.txt`
- **Configuration**: `.streamlit/config.toml`

## 🛠️ Prerequisites

Before deploying, ensure you have:
- Python 3.8+ installed
- All dependencies installed (`pip install -r requirements.txt`)
- Your application tested locally

## 🚀 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

**Best for**: Quick deployment, free hosting, easy updates

1. **Prepare your repository**:
   ```bash
   # Initialize git if not already done
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub**:
   - Create a new repository on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

3. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository
   - Set main file path: `Simulator.py`
   - Click "Deploy!"

**Advantages**: Free, automatic updates, custom domain support
**Limitations**: 1GB RAM, 1GB storage

### Option 2: Heroku

**Best for**: More control, custom configurations

1. **Install Heroku CLI**:
   - Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Create Heroku app**:
   ```bash
   heroku create your-app-name
   ```

3. **Create Procfile**:
   ```bash
   echo "web: streamlit run Simulator.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

4. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

**Advantages**: More resources, custom domains, add-ons
**Cost**: Free tier available, paid plans for production

### Option 3: Railway

**Best for**: Modern deployment, easy scaling

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy**:
   ```bash
   railway login
   railway init
   railway up
   ```

**Advantages**: Modern platform, easy scaling, good free tier
**Cost**: Free tier available

### Option 4: Google Cloud Platform (GCP)

**Best for**: Enterprise use, high performance

1. **Set up GCP project**:
   - Create project in [Google Cloud Console](https://console.cloud.google.com)

2. **Deploy using Cloud Run**:
   ```bash
   # Build and deploy
   gcloud run deploy --source . --platform managed --region us-central1
   ```

**Advantages**: Highly scalable, enterprise-grade
**Cost**: Pay-per-use, free tier available

### Option 5: AWS (Amazon Web Services)

**Best for**: Enterprise, high availability

1. **Deploy using AWS App Runner**:
   - Connect your GitHub repository
   - Configure build settings
   - Deploy automatically

**Advantages**: Highly available, scalable
**Cost**: Pay-per-use

### Option 6: DigitalOcean App Platform

**Best for**: Simple deployment, good performance

1. **Create app in DigitalOcean**:
   - Connect GitHub repository
   - Configure build settings
   - Deploy

**Advantages**: Simple, reliable, good performance
**Cost**: Starting at $5/month

## 🔧 Local Testing Before Deployment

1. **Test your application**:
   ```bash
   streamlit run Simulator.py
   ```

2. **Verify all pages work**:
   - Main simulation page
   - Gantt chart page
   - Queueing calculator page

3. **Check dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📝 Environment Variables (if needed)

If your app needs environment variables, create a `.env` file:
```bash
# Example environment variables
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 🐛 Troubleshooting

### Common Issues:

1. **Import errors**: Ensure all dependencies are in `requirements.txt`
2. **Port issues**: Check `.streamlit/config.toml` configuration
3. **File not found**: Ensure all files are in the repository
4. **Memory issues**: Optimize your code or upgrade hosting plan

### Debug Commands:
```bash
# Check Streamlit version
streamlit --version

# Run with debug info
streamlit run Simulator.py --logger.level=debug

# Check dependencies
pip list
```

## 🔄 Updating Your Deployment

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit and push to repository**:
   ```bash
   git add .
   git commit -m "Update description"
   git push origin main
   ```
4. **Most platforms auto-deploy on push**

## 📊 Monitoring and Analytics

- **Streamlit Cloud**: Built-in analytics
- **Heroku**: Use Heroku metrics
- **Other platforms**: Check platform-specific monitoring tools

## 🎯 Recommended Deployment Strategy

1. **Start with Streamlit Community Cloud** (free, easy)
2. **If you need more resources**, consider Railway or Heroku
3. **For production/enterprise**, use GCP or AWS

## 📞 Support

- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Platform-specific documentation
- GitHub Issues for your repository

---

**Happy Deploying! 🚀**
