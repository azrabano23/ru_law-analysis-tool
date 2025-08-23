# Google Custom Search API Setup Guide

## 🎯 **Why Use Google Custom Search API?**

The enhanced faculty media tracker can use Google's Custom Search API to find **comprehensive results** including:
- ✅ Op-eds and opinion pieces
- ✅ Print and online interviews  
- ✅ Television appearances
- ✅ Podcast interviews
- ✅ Social media mentions
- ✅ Academic commentary
- ✅ News articles and analysis

## 💰 **Cost Breakdown**

- **Google Custom Search API**: $5 per 1,000 queries
- **Typical monthly usage**: 2,000-5,000 queries
- **Estimated monthly cost**: $10-25
- **Coverage**: Comprehensive web search (much better than basic search)

## 🔧 **Setup Instructions**

### Step 1: Google Cloud Console Setup

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select an existing one
3. **Enable the Custom Search API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Custom Search API"
   - Click "Enable"

### Step 2: Create API Credentials

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "API Key"**
3. **Copy your API key** (you'll need this later)
4. **Restrict the API key** (recommended):
   - Click on the API key
   - Under "Application restrictions" select "HTTP referrers"
   - Under "API restrictions" select "Custom Search API"

### Step 3: Create Custom Search Engine

1. **Go to Custom Search Engine**: https://cse.google.com/
2. **Click "Add" to create a new search engine**
3. **Configure the search engine**:
   - **Sites to search**: Leave blank (search entire web)
   - **Name**: "CSRR Faculty Media Search"
   - **Language**: English
   - **Region**: United States
4. **Click "Create"**
5. **Copy your Search Engine ID** (you'll need this later)

### Step 4: Set Environment Variables

#### On Mac/Linux:
```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_CSE_ID="your_search_engine_id_here"
```

#### On Windows:
```cmd
set GOOGLE_API_KEY=your_api_key_here
set GOOGLE_CSE_ID=your_search_engine_id_here
```

#### Permanent Setup (Mac/Linux):
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export GOOGLE_API_KEY="your_api_key_here"
export GOOGLE_CSE_ID="your_search_engine_id_here"
```

### Step 5: Test the Setup

```bash
python enhanced_faculty_media_tracker.py --quick-test
```

You should see: "✅ Google Custom Search API configured - Enhanced search enabled"

## 📊 **Enhanced vs Basic Search Comparison**

| Feature | Basic Search | Enhanced Search (Google API) |
|---------|-------------|------------------------------|
| **Coverage** | Limited (Bing only) | Comprehensive (entire web) |
| **Results per faculty** | 3-5 | 10+ |
| **Search types** | Basic queries | Op-eds, interviews, podcasts, videos |
| **Success rate** | ~30% | ~70%+ |
| **Cost** | Free | $10-25/month |
| **Rate limits** | Strict | Generous |

## 🔍 **What Enhanced Search Finds**

### **Op-eds and Opinion Pieces**
- Newspaper op-eds
- Magazine opinion pieces
- Blog commentary
- Academic analysis

### **Interviews**
- Print interviews
- Online interviews
- Radio interviews
- Podcast appearances

### **Media Appearances**
- Television interviews
- YouTube videos
- Social media mentions
- Conference presentations

### **Academic Content**
- Journal articles
- Conference papers
- Academic blogs
- University publications

## 🚀 **Usage with Enhanced Search**

### **Monthly Process (5 minutes)**:

1. **Update date range** in `config.yaml`:
   ```yaml
   search_period:
     start_date: '2025-08-01'
     end_date: '2025-08-31'
   ```

2. **Run enhanced search**:
   ```bash
   python enhanced_faculty_media_tracker.py
   ```

3. **Get comprehensive results** in Downloads folder

### **Expected Results**:
- **Faculty with articles**: 70%+ (vs 30% with basic search)
- **Articles per faculty**: 5-15 (vs 1-3 with basic search)
- **Search time**: 30-60 minutes (vs 2-3 hours manually)
- **Coverage**: Comprehensive (vs limited with basic search)

## ⚠️ **Important Notes**

### **API Limits**:
- **Free tier**: 100 queries/day
- **Paid tier**: $5 per 1,000 queries
- **Rate limits**: 10,000 queries/day

### **Best Practices**:
- **Run searches monthly** (not daily)
- **Use date ranges** to limit results
- **Monitor usage** in Google Cloud Console
- **Set up billing alerts** to avoid surprises

### **Cost Optimization**:
- **Limit search queries** per faculty (5-10 max)
- **Use date restrictions** to focus results
- **Combine with basic search** for cost efficiency

## 🆘 **Troubleshooting**

### **"API not configured" error**:
- Check environment variables are set
- Verify API key is correct
- Ensure Custom Search API is enabled

### **"Quota exceeded" error**:
- Check usage in Google Cloud Console
- Set up billing if needed
- Reduce search queries per faculty

### **"No results found"**:
- Verify search engine ID is correct
- Check date range is valid
- Try broader search terms

## 📞 **Support**

If you need help with API setup:
1. Check Google Cloud Console documentation
2. Verify environment variables are set correctly
3. Test with the quick test option
4. Monitor API usage and costs

---

**Ready to enable comprehensive faculty media tracking!** 🎉
