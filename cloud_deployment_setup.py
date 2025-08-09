"""
UPTRENDR ML PIPELINE DEPLOYMENT SETUP
=====================================

This script helps deploy your sophisticated ML investment pipeline to Google Cloud Functions
with proper scheduling and Firestore collection initialization.

Instructions:
1. Run this to create the deployment configuration
2. Deploy using Firebase CLI
3. Initialize Firestore collections
4. Schedule the ML training and data fetching

Your ML API is deployed at: https://uptrendr-jp-626448778297.asia-northeast1.run.app
"""

import json
from datetime import datetime, timezone

# Cloud Functions deployment configuration
CLOUD_FUNCTIONS_CONFIG = {
    "functions": [
        {
            "name": "train_ml_models_daily",
            "schedule": "0 2 * * *",  # 2:00 AM UTC daily
            "description": "Train sophisticated ML models using historical factors",
            "memory": "2GB",
            "timeout": "540s",
            "trigger": "schedule"
        },
        {
            "name": "fetch_market_data_daily", 
            "schedule": "0 1 * * *",  # 1:00 AM UTC daily
            "description": "Fetch comprehensive market data from multiple sources",
            "memory": "1GB", 
            "timeout": "300s",
            "trigger": "schedule"
        },
        {
            "name": "fetch_sentiment_data_daily",
            "schedule": "15 1 * * *",  # 1:15 AM UTC daily
            "description": "Analyze news sentiment for market prediction",
            "memory": "1GB",
            "timeout": "300s", 
            "trigger": "schedule"
        },
        {
            "name": "fetch_macro_data_daily",
            "schedule": "30 1 * * *",  # 1:30 AM UTC daily
            "description": "Fetch macroeconomic indicators and analysis",
            "memory": "512MB",
            "timeout": "180s",
            "trigger": "schedule"
        },
        {
            "name": "fetch_esg_data_daily",
            "schedule": "45 1 * * *",  # 1:45 AM UTC daily  
            "description": "Fetch ESG scores for sustainable investing",
            "memory": "512MB",
            "timeout": "180s",
            "trigger": "schedule"
        },
        {
            "name": "create_historical_factors_daily",
            "schedule": "30 0 * * *",  # 12:30 AM UTC daily
            "description": "Create consolidated ML training data",
            "memory": "1GB",
            "timeout": "300s",
            "trigger": "schedule"
        },
        {
            "name": "fetch_japanese_data_daily",
            "schedule": "0 7 * * *",  # 7:00 AM UTC daily
            "description": "Fetch Japanese market data and news",
            "memory": "512MB", 
            "timeout": "240s",
            "trigger": "schedule"
        },
        {
            "name": "generate_market_predictions_daily",
            "schedule": "30 2 * * *",  # 2:30 AM UTC daily (after ML training)
            "description": "Generate market predictions using trained models",
            "memory": "1GB",
            "timeout": "300s", 
            "trigger": "schedule"
        }
    ]
}

# Firestore Collections to Initialize
FIRESTORE_COLLECTIONS = {
    "raw_data_collections": [
        "market_data",
        "technical_analysis", 
        "fundamental_analysis",
        "sentiment_analysis",
        "macro_indicators",
        "esg_scores",
        "economic_calendar",
        "japanese_news",
        "japanese_economics"
    ],
    "ml_collections": [
        "historical_factors",
        "model_weights", 
        "market_predictions",
        "ml_training_status",
        "forecast_weights"
    ],
    "app_collections": [
        "calendar",
        "users",
        "config",
        "pipeline_executions",
        "pipeline_monitoring"
    ]
}

# Sample data structure for each collection
SAMPLE_DATA_STRUCTURES = {
    "historical_factors": {
        "symbol": "AAPL",
        "horizon": "1M",
        "fundamental": 0.75,
        "technical": 0.68, 
        "sentiment": 0.72,
        "macro": 0.55,
        "esg": 0.63,
        "actual_return": 0.05,
        "volatility": 25.5,
        "confidence": 0.8,
        "timestamp": datetime.now(timezone.utc)
    },
    "model_weights": {
        "horizon": "1M",
        "fundamental": 0.25,
        "technical": 0.20,
        "sentiment": 0.18,
        "macro": 0.22,
        "esg": 0.15,
        "japanese_adjustment": 1.05,
        "last_updated": datetime.now(timezone.utc),
        "model_performance": {"r2_score": 0.73, "directional_accuracy": 0.68},
        "training_samples": 500
    },
    "market_predictions": {
        "symbol": "^GSPC",
        "predictions": {
            "1W": {"return": 0.02, "confidence": 0.75, "risk_level": "moderate"},
            "1M": {"return": 0.05, "confidence": 0.68, "risk_level": "moderate"}, 
            "6M": {"return": 0.12, "confidence": 0.60, "risk_level": "high"}
        },
        "factors": {
            "fundamental": 0.70,
            "technical": 0.65,
            "sentiment": 0.58,
            "macro": 0.52,
            "esg": 0.60
        },
        "timestamp": datetime.now(timezone.utc)
    }
}

def create_deployment_files():
    """Create deployment configuration files"""
    
    # Create Cloud Scheduler configuration
    scheduler_config = {
        "jobs": []
    }
    
    for func in CLOUD_FUNCTIONS_CONFIG["functions"]:
        job = {
            "name": f"scheduler-{func['name'].replace('_', '-')}",
            "description": func["description"],
            "schedule": func["schedule"],
            "timeZone": "UTC",
            "httpTarget": {
                "uri": f"https://asia-northeast1-{PROJECT_ID}.cloudfunctions.net/{func['name']}",
                "httpMethod": "POST"
            }
        }
        scheduler_config["jobs"].append(job)
    
    # Save configuration files
    with open('cloud_functions_config.json', 'w') as f:
        json.dump(CLOUD_FUNCTIONS_CONFIG, f, indent=2, default=str)
        
    with open('firestore_collections.json', 'w') as f:
        json.dump(FIRESTORE_COLLECTIONS, f, indent=2)
        
    with open('sample_data_structures.json', 'w') as f:
        json.dump(SAMPLE_DATA_STRUCTURES, f, indent=2, default=str)
        
    with open('cloud_scheduler_config.json', 'w') as f:
        json.dump(scheduler_config, f, indent=2)
    
    print("✅ Deployment configuration files created!")
    print("""
📁 Created Files:
  ├── cloud_functions_config.json    # Functions deployment config
  ├── firestore_collections.json     # Firestore collections to create
  ├── sample_data_structures.json    # Data structure examples
  └── cloud_scheduler_config.json    # Scheduling configuration
    
🚀 Next Steps:
  1. Run: firebase deploy --only functions
  2. Initialize Firestore collections
  3. Set up Cloud Scheduler
  4. Test the ML pipeline
    """)

if __name__ == "__main__":
    PROJECT_ID = "uptrendr-api-620356694660"  # Update with your project ID
    create_deployment_files()