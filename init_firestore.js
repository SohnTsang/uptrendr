const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccountKey.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

const collections = [
  'market_data', 'technical_analysis', 'fundamental_analysis',
  'sentiment_analysis', 'macro_indicators', 'esg_scores',
  'historical_factors', 'model_weights', 'market_predictions',
  'ml_training_status', 'calendar', 'config'
];

async function initializeCollections() {
  for (const collection of collections) {
    try {
      await db.collection(collection).doc('_init').set({
        initialized: true,
        created_at: admin.firestore.FieldValue.serverTimestamp()
      });
      console.log(`✅ Initialized collection: ${collection}`);
    } catch (error) {
      console.log(`❌ Error initializing ${collection}:`, error.message);
    }
  }
  
  console.log('\n🎉 Firestore collections initialized!');
  process.exit(0);
}

initializeCollections();
