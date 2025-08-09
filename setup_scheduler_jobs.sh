#!/bin/bash

# CLOUD SCHEDULER SETUP FOR UPTRENDR ML PIPELINE
# ==============================================

echo "⏰ SETTING UP AUTOMATED ML PIPELINE SCHEDULING"
echo "=============================================="

PROJECT_ID="uptrendr-jp"
LOCATION="asia-northeast1"
API_BASE="https://uptrendr-api-626448778297.asia-northeast1.run.app"

echo "📊 Project: $PROJECT_ID"
echo "🌏 Location: $LOCATION"  
echo "🔗 API Base: $API_BASE"
echo ""

# Set the project and location
gcloud config set project $PROJECT_ID

echo "🗑️ CLEANING UP EXISTING JOBS..."
# Delete existing jobs (ignore errors if they don't exist)
gcloud scheduler jobs delete fetch-market-data --location=$LOCATION --quiet 2>/dev/null || true
gcloud scheduler jobs delete train-ml-models --location=$LOCATION --quiet 2>/dev/null || true
gcloud scheduler jobs delete generate-predictions --location=$LOCATION --quiet 2>/dev/null || true
gcloud scheduler jobs delete create-historical-factors --location=$LOCATION --quiet 2>/dev/null || true

echo ""
echo "⏰ CREATING NEW SCHEDULED JOBS..."
echo ""

# Job 1: Create Historical Factors (12:30 AM UTC)
echo "1️⃣ Creating historical factors job..."
gcloud scheduler jobs create http create-historical-factors \
    --location=$LOCATION \
    --schedule="30 0 * * *" \
    --time-zone="UTC" \
    --uri="$API_BASE/populate-data" \
    --http-method=POST \
    --description="Create historical factors for ML training"

# Job 2: Fetch Market Data (1:00 AM UTC)
echo "2️⃣ Creating market data job..."
gcloud scheduler jobs create http fetch-market-data \
    --location=$LOCATION \
    --schedule="0 1 * * *" \
    --time-zone="UTC" \
    --uri="$API_BASE/market-data" \
    --http-method=GET \
    --description="Fetch real-time market data"

# Job 3: Train ML Models (2:00 AM UTC)  
echo "3️⃣ Creating ML training job..."
gcloud scheduler jobs create http train-ml-models \
    --location=$LOCATION \
    --schedule="0 2 * * *" \
    --time-zone="UTC" \
    --uri="$API_BASE/train-models" \
    --http-method=POST \
    --description="Train ML models with latest data"

# Job 4: Generate Market Predictions (2:30 AM UTC)
echo "4️⃣ Creating predictions job..."
gcloud scheduler jobs create http generate-predictions \
    --location=$LOCATION \
    --schedule="30 2 * * *" \
    --time-zone="UTC" \
    --uri="$API_BASE/generate-predictions" \
    --http-method=POST \
    --description="Generate market predictions"

echo ""
echo "✅ SCHEDULER JOBS CREATED!"
echo ""

# List all jobs to verify
echo "📋 CURRENT SCHEDULED JOBS:"
gcloud scheduler jobs list --location=$LOCATION

echo ""
echo "🎯 PIPELINE SCHEDULE:"
echo "  12:30 AM UTC - Create historical factors → historical_factors"
echo "   1:00 AM UTC - Fetch market data → historical_factors" 
echo "   2:00 AM UTC - Train ML models → model_weights, trained_models, ml_training_status"
echo "   2:30 AM UTC - Generate predictions → market_predictions"
echo ""

echo "🔥 AUTOMATED ML PIPELINE IS NOW LIVE!"
echo "The system will automatically:"
echo "  ✅ Collect fresh market data daily"
echo "  ✅ Train ML models with new data"
echo "  ✅ Generate investment predictions"
echo "  ✅ Update all 5 core Firebase collections"
echo ""

echo "📱 Monitor via Google Cloud Console:"
echo "https://console.cloud.google.com/cloudscheduler?project=$PROJECT_ID"
