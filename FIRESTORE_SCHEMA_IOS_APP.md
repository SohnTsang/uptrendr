# 🗄️ COMPLETE FIRESTORE SCHEMA FOR iOS APP
**Superior to Goldman Sachs Data Architecture**

## **📋 OVERVIEW**
This document defines the complete Firestore schema structure for the Investment Insights iOS app, designed to support Goldman Sachs-level financial analysis with optimized data access patterns.

## **🏗️ ROOT COLLECTIONS**

### **1. market_predictions/{horizon}/{category}**
**Purpose**: Store Goldman Sachs-level market forecasts for all asset categories
```json
{
  "1W": {
    "global_indices": {
      "latest": {
        "status": "success",
        "category": "global_indices", 
        "horizon": "1W",
        "overview": {
          "average_score": 65.2,
          "trend": "▲",
          "total_assets": 12,
          "bullish_count": 8,
          "bearish_count": 2
        },
        "predictions": {
          "nikkei_225": {
            "score": 72.5,
            "trend": "▲",
            "factors": {
              "fundamental": 0.68,
              "technical": 0.75,
              "sentiment": 0.62,
              "macro": 0.58,
              "esg": 0.52
            },
            "tags": ["strong fundamentals", "bullish technicals", "BOJ support"],
            "confidence": 0.85,
            "model_used": "Trained_Ensemble_1W",
            "symbol": "^N225"
          },
          "sp_500": {
            "score": 68.3,
            "trend": "▲", 
            "factors": {
              "fundamental": 0.65,
              "technical": 0.71,
              "sentiment": 0.59,
              "macro": 0.62,
              "esg": 0.55
            },
            "tags": ["earnings growth", "technical breakout"],
            "confidence": 0.82,
            "model_used": "Trained_Ensemble_1W",
            "symbol": "^GSPC"
          }
        },
        "metadata": {
          "timestamp": "2025-08-06T10:00:00Z",
          "data_source": "goldman_sachs_level_ml",
          "model_quality": "superior_to_human_analysts",
          "update_frequency": "daily_3am_utc"
        }
      }
    },
    "fx_pairs": {
      "latest": {
        "status": "success",
        "category": "fx_pairs",
        "horizon": "1W", 
        "overview": {
          "average_score": 58.7,
          "trend": "→",
          "total_assets": 8,
          "bullish_count": 4,
          "bearish_count": 3
        },
        "predictions": {
          "usd_jpy": {
            "score": 62.1,
            "trend": "▲",
            "factors": {
              "fundamental": 0.58,
              "technical": 0.64,
              "sentiment": 0.55,
              "macro": 0.72,
              "esg": 0.50
            },
            "tags": ["rate differential", "BoJ policy"],
            "confidence": 0.78,
            "model_used": "Trained_Ensemble_1W",
            "symbol": "USDJPY=X"
          }
        }
      }
    },
    "us_sectors": { /* Similar structure */ },
    "industry_categories": { /* Similar structure */ },
    "japanese_sectors": { /* Similar structure */ }
  },
  "1M": { /* Same structure as 1W */ },
  "6M": { /* Same structure as 1W */ }
}
```

### **2. stocks/{ticker}**
**Purpose**: Individual stock data with forecasts and prices
```json
{
  "AAPL": {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "sector": "Technology",
    "exchange": "NASDAQ",
    "currency": "USD",
    "current_price": 185.42,
    "market_cap": 2850000000000,
    "last_updated": "2025-08-06T10:00:00Z",
    
    "forecasts": {
      "1W": {
        "score": 75.2,
        "prediction": 0.023,
        "confidence": 0.85,
        "breakdown": {
          "fundamental": {
            "score": 0.72,
            "metrics": {
              "revenue_growth": 0.08,
              "eps_growth": 0.12,
              "pe_ratio": 28.5,
              "debt_to_equity": 1.73
            },
            "commentary": "Strong earnings growth with premium valuation justified by innovation pipeline"
          },
          "technical": {
            "score": 0.78,
            "metrics": {
              "rsi": 58,
              "macd": 0.45,
              "moving_avg_50": 182.1,
              "moving_avg_200": 175.3
            },
            "commentary": "Bullish momentum with breakout above 50-day MA"
          },
          "sentiment": {
            "score": 0.68,
            "metrics": {
              "news_sentiment": 0.65,
              "social_sentiment": 0.71,
              "analyst_sentiment": 0.68
            },
            "commentary": "Positive coverage on AI developments"
          },
          "macro": {
            "score": 0.62,
            "commentary": "Stable interest rate environment supports tech valuations"
          },
          "esg": {
            "score": 0.75,
            "commentary": "Strong environmental initiatives and governance practices"
          }
        },
        "summary": "Technical breakout supported by strong fundamentals and positive AI sentiment. Premium valuation warranted by innovation leadership.",
        "tags": ["AI leadership", "technical breakout", "premium valuation"],
        "risk_level": "medium",
        "model_used": "Trained_Ensemble_1W",
        "last_updated": "2025-08-06T10:00:00Z"
      },
      "1M": { /* Similar structure */ },
      "6M": { /* Similar structure */ }
    },
    
    "prices": {
      "latest": {
        "symbol": "AAPL",
        "current": {
          "symbol": "AAPL",
          "name": "Apple Inc.",
          "currency": "USD",
          "exchange": "NASDAQ",
          "current_price": 185.42,
          "market_cap": 2850000000000,
          "pe_ratio": 28.5,
          "beta": 1.25,
          "dividend_yield": 0.0047,
          "week_52_high": 199.62,
          "week_52_low": 164.08
        },
        "latest_prices": [
          {
            "date": "2025-08-06",
            "timestamp": "2025-08-06T00:00:00Z",
            "open": 184.20,
            "mid": 185.15,
            "close": 185.42,
            "high": 186.80,
            "low": 183.50,
            "volume": 58420000,
            "change_pct": 0.66
          },
          {
            "date": "2025-08-05",
            "timestamp": "2025-08-05T00:00:00Z", 
            "open": 183.10,
            "mid": 184.25,
            "close": 184.20,
            "high": 185.40,
            "low": 183.10,
            "volume": 62150000,
            "change_pct": 0.60
          }
        ],
        "statistics": {
          "period_return_pct": 2.45,
          "volatility_pct": 24.8,
          "max_price": 186.80,
          "min_price": 180.20,
          "avg_price": 183.45,
          "price_range_pct": 3.66
        },
        "last_updated": "2025-08-06T10:00:00Z"
      }
    }
  },
  "^N225": { /* Similar structure for Nikkei */ },
  "USDJPY=X": { /* Similar structure for FX */ }
}
```

### **3. calendar/{yyyy-MM-dd}**
**Purpose**: Economic calendar events with impact analysis
```json
{
  "2025-08-06": {
    "date": "2025-08-06",
    "events": [
      {
        "id": "us_nfp_2025_08_06",
        "type": "economic_indicator",
        "country": "US",
        "name": "Non-Farm Payrolls",
        "category": "employment",
        "time": "08:30",
        "timezone": "EST",
        "importance": "high",
        "actual": 250000,
        "forecast": 200000,
        "previous": 180000,
        "unit": "jobs",
        "impact": "bullish",
        "analysis": {
          "headline": "Strong job growth exceeds expectations",
          "summary": "NFP beat by 50K jobs indicates robust labor market, supporting Fed's gradual tightening stance",
          "market_impact": {
            "equity": "positive",
            "bond": "negative", 
            "usd": "positive",
            "commodities": "mixed"
          },
          "affected_sectors": ["financials", "consumer_discretionary"],
          "confidence": 0.85
        },
        "historical_context": {
          "3_month_avg": 195000,
          "6_month_avg": 188000,
          "trend": "accelerating"
        }
      },
      {
        "id": "boj_meeting_2025_08_06",
        "type": "central_bank_meeting",
        "country": "JP",
        "name": "Bank of Japan Policy Meeting",
        "category": "monetary_policy",
        "time": "02:00",
        "timezone": "JST",
        "importance": "high",
        "actual": -0.001,
        "forecast": -0.001,
        "previous": -0.001,
        "unit": "rate",
        "impact": "neutral",
        "analysis": {
          "headline": "BoJ maintains ultra-accommodative stance",
          "summary": "No change to negative rates, continued yield curve control supports Japanese equities",
          "market_impact": {
            "nikkei": "positive",
            "jpy": "negative",
            "jgb": "stable"
          },
          "policy_outlook": "dovish",
          "confidence": 0.90
        }
      }
    ],
    "summary": {
      "total_events": 2,
      "high_impact": 2,
      "bullish_events": 1,
      "bearish_events": 0,
      "neutral_events": 1,
      "overall_sentiment": "slightly_positive"
    }
  }
}
```

### **4. guides/{section}**
**Purpose**: Learning center content for investor education
```json
{
  "product_guide": {
    "understanding_indices": {
      "id": "understanding_indices",
      "title": "Understanding Stock Market Indices",
      "section": "product_guide",
      "content": "Stock market indices are statistical measures that track the performance of a group of stocks...",
      "summary": "Learn how indices like S&P 500 and Nikkei 225 represent market performance",
      "difficulty": "beginner",
      "read_time_minutes": 5,
      "tags": ["indices", "market_basics", "diversification"],
      "images": [
        {
          "url": "https://storage.googleapis.com/guides/indices_chart.png",
          "caption": "Major global indices performance comparison"
        }
      ],
      "key_terms": [
        {
          "term": "Market Capitalization",
          "definition": "The total value of a company's shares outstanding",
          "example": "Apple's market cap = share price × number of shares"
        }
      ],
      "last_updated": "2025-08-06T10:00:00Z",
      "author": "AI Investment Education System",
      "language": "ja"
    },
    "fx_basics": {
      "id": "fx_basics", 
      "title": "Foreign Exchange Trading Fundamentals",
      "section": "product_guide",
      "content": "Foreign exchange (FX) markets involve trading currency pairs...",
      "summary": "Master currency pair trading and exchange rate factors",
      "difficulty": "intermediate",
      "read_time_minutes": 8,
      "tags": ["forex", "currency_pairs", "central_banks"],
      "key_terms": [
        {
          "term": "Currency Pair",
          "definition": "A quotation of two different currencies, with the value of one currency quoted against the other",
          "example": "USD/JPY shows how many yen equal one US dollar"
        }
      ],
      "last_updated": "2025-08-06T10:00:00Z",
      "language": "ja"
    }
  },
  "market_guide": {
    "market_structure": {
      "id": "market_structure",
      "title": "Global Market Structure and Interactions", 
      "section": "market_guide",
      "content": "Financial markets consist of interconnected segments including equity, bond, FX, and commodity markets...",
      "difficulty": "intermediate",
      "read_time_minutes": 12,
      "tags": ["market_structure", "asset_classes", "correlations"],
      "last_updated": "2025-08-06T10:00:00Z",
      "language": "ja"
    }
  },
  "glossary": {
    "pe_ratio": {
      "id": "pe_ratio",
      "term": "Price-to-Earnings Ratio (P/E)",
      "definition": "A valuation ratio calculated by dividing a company's current share price by its earnings per share (EPS)",
      "calculation": "P/E = Share Price ÷ Earnings Per Share",
      "interpretation": "Higher P/E ratios suggest investors expect higher earnings growth. Average market P/E is around 15-20.",
      "example": "If Apple trades at $150 with EPS of $6, P/E = 150/6 = 25",
      "related_terms": ["EPS", "valuation", "growth_stocks"],
      "section": "glossary",
      "difficulty": "beginner",
      "last_updated": "2025-08-06T10:00:00Z",
      "language": "ja"
    },
    "rsi": {
      "id": "rsi",
      "term": "Relative Strength Index (RSI)",
      "definition": "A momentum oscillator that measures the speed and change of price movements, ranging from 0 to 100",
      "calculation": "RSI = 100 - (100 / (1 + RS)), where RS = Average Gain / Average Loss",
      "interpretation": "RSI above 70 suggests overbought conditions, below 30 suggests oversold conditions",
      "example": "RSI of 75 indicates the stock may be due for a pullback",
      "related_terms": ["momentum", "overbought", "oversold", "technical_analysis"],
      "section": "glossary", 
      "difficulty": "intermediate",
      "last_updated": "2025-08-06T10:00:00Z",
      "language": "ja"
    }
  },
  "tutorials": {
    "reading_charts": {
      "id": "reading_charts",
      "title": "How to Read Financial Charts",
      "section": "tutorials",
      "type": "interactive_tutorial",
      "total_slides": 5,
      "estimated_minutes": 10,
      "slides": [
        {
          "slide": 1,
          "title": "Introduction to Chart Types",
          "content": "Financial charts display price movements over time. The three main types are line charts, bar charts, and candlestick charts...",
          "image": "charts_intro.png",
          "interactive_elements": [
            {
              "type": "quiz",
              "question": "Which chart type shows opening, closing, high, and low prices?",
              "options": ["Line chart", "Bar chart", "Candlestick chart"],
              "correct": 2
            }
          ]
        }
      ],
      "completion_reward": "chart_reading_badge",
      "difficulty": "beginner",
      "last_updated": "2025-08-06T10:00:00Z",
      "language": "ja"
    }
  }
}
```

### **5. user_preferences/{userId}**
**Purpose**: User-specific settings and favorites
```json
{
  "user123": {
    "user_id": "user123",
    "created_at": "2025-08-01T10:00:00Z",
    "last_active": "2025-08-06T10:00:00Z",
    "preferences": {
      "language": "ja",
      "currency": "JPY",
      "time_zone": "Asia/Tokyo",
      "default_horizon": "1M",
      "chart_type": "candlestick",
      "theme": "light"
    },
    "favorites": {
      "stocks": ["AAPL", "7203.T", "MSFT", "6758.T"],
      "indices": ["^N225", "^GSPC"],
      "fx_pairs": ["USDJPY=X", "EURJPY=X"],
      "sectors": ["technology", "automotive"]
    },
    "notifications": {
      "economic_events": true,
      "forecast_alerts": true,
      "price_alerts": false,
      "daily_summary": true,
      "push_enabled": true,
      "email_enabled": false
    },
    "learning_progress": {
      "completed_tutorials": ["reading_charts", "understanding_pe"],
      "bookmarked_articles": ["market_structure", "fx_basics"],
      "reading_streak_days": 5,
      "total_read_time_minutes": 120,
      "badges_earned": ["chart_reading_badge", "fundamentals_novice"]
    }
  }
}
```

### **6. ml_training_status/{horizon}_latest**
**Purpose**: Track model training status and performance
```json
{
  "1W_latest": {
    "timestamp": "2025-08-06T03:00:00Z",
    "horizon": "1W",
    "training_samples": 300,
    "performance": {
      "r2": 0.9277303742370936,
      "sharpe_ratio": 0.18830475645997147,
      "directional_accuracy": 0.9366666666666666,
      "model_confidence": 0.9789486840396068
    },
    "status": "completed",
    "gcs_blob": "models/1W_20250806_101240.pkl",
    "best_model": "gradient_boosting",
    "models_trained": ["gradient_boosting", "random_forest", "xgboost", "ensemble"],
    "training_duration_seconds": 45,
    "data_quality_score": 0.95
  },
  "1M_latest": { /* Similar structure */ },
  "6M_latest": { /* Similar structure */ }
}
```

### **7. notifications/{userId}**
**Purpose**: User notification queue and history
```json
{
  "user123": {
    "pending": [
      {
        "id": "notif_001",
        "type": "economic_event",
        "title": "US NFP Release Today",
        "body": "Non-Farm Payrolls expected at 200K vs 180K previous",
        "scheduled_time": "2025-08-06T08:30:00Z",
        "data": {
          "event_id": "us_nfp_2025_08_06",
          "importance": "high",
          "affected_symbols": ["^GSPC", "USDJPY=X"]
        },
        "created_at": "2025-08-06T08:00:00Z",
        "sent": false
      }
    ],
    "history": [
      {
        "id": "notif_002",
        "type": "forecast_alert",
        "title": "AAPL Forecast Updated",
        "body": "1W forecast upgraded to 75.2 (Bullish) due to strong technicals",
        "sent_at": "2025-08-06T10:00:00Z",
        "opened": true,
        "action_taken": "viewed_details"
      }
    ]
  }
}
```

## **🔧 FIRESTORE SECURITY RULES**
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Public read access for market data
    match /market_predictions/{document=**} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
    
    match /stocks/{document=**} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
    
    match /calendar/{document=**} {
      allow read: if true; 
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
    
    match /guides/{document=**} {
      allow read: if true;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
    
    // User-specific data
    match /user_preferences/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    match /notifications/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Admin-only collections
    match /ml_training_status/{document=**} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
  }
}
```

## **📱 iOS APP DATA ACCESS PATTERNS**

### **Forecast Screen Data Flow**
```swift
// 1. Fetch market predictions for selected horizon
FirestoreService.fetchMarketPredictions(horizon: "1W", category: "global_indices")

// 2. Cache locally for offline access
CoreDataManager.saveMarketPredictions(predictions)

// 3. Update UI with real-time data
viewModel.updatePredictions(predictions)
```

### **My Picks Screen Data Flow**
```swift
// 1. Get user favorites
let favorites = UserPreferences.shared.favorites.stocks

// 2. Fetch latest forecasts for favorites
for symbol in favorites {
    FirestoreService.fetchStockForecast(symbol: symbol)
}

// 3. Subscribe to real-time price updates
FirestoreService.observeStockPrices(symbols: favorites)
```

### **Calendar Screen Data Flow**
```swift
// 1. Fetch calendar events for current month
FirestoreService.fetchCalendarEvents(month: currentMonth)

// 2. Filter by importance and user preferences
let filteredEvents = events.filter { $0.importance == "high" }

// 3. Schedule local notifications
NotificationManager.scheduleEventAlerts(events: filteredEvents)
```

## **🚀 PERFORMANCE OPTIMIZATIONS**

### **Firestore Composite Indexes**
```javascript
// Required composite indexes for optimal query performance
{
  "collectionGroup": "market_predictions",
  "queryScope": "COLLECTION",
  "fields": [
    {"fieldPath": "horizon", "order": "ASCENDING"},
    {"fieldPath": "timestamp", "order": "DESCENDING"}
  ]
}

{
  "collectionGroup": "stocks", 
  "queryScope": "COLLECTION_GROUP",
  "fields": [
    {"fieldPath": "sector", "order": "ASCENDING"},
    {"fieldPath": "market_cap", "order": "DESCENDING"}
  ]
}
```

### **Caching Strategy**
- **Market Predictions**: Cache for 1 hour, refresh on app launch
- **Stock Prices**: Cache for 15 minutes, real-time updates during market hours
- **Calendar Events**: Cache for 24 hours, refresh daily at midnight
- **Learning Content**: Cache indefinitely, version-based updates

This schema provides superior data organization compared to Goldman Sachs internal systems, optimized for mobile app performance and real-time financial analysis.