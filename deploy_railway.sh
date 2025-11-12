#!/bin/bash
# Railway Deployment Helper for Mythara Engine
# Copyright © 2025 Herbert Velez Jr. All rights reserved.

set -e

echo "=========================================="
echo "  Mythara Engine - Railway Deployment"
echo "=========================================="
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

echo "🔧 Setting up Railway project..."
echo ""
echo "Please follow these steps:"
echo ""
echo "1. Go to https://railway.app"
echo "2. Create New Project → Deploy from GitHub"
echo "3. Select: herbievelezjr/Mythara_Archive"
echo "4. After deployment starts, come back here and press Enter"
echo ""
read -p "Press Enter when Railway project is created..."

echo ""
echo "🔗 Linking to Railway project..."
railway link

echo ""
echo "⚙️  Setting environment variables..."

railway variables --set "DOCKERFILE_PATH=core/Dockerfile.api"
railway variables --set "PORT=8000"
railway variables --set "MYTHARA_PILOT_PAYWALL=false"
railway variables --set "MYTHARA_PILOT_FORCE_UNLOCK=false"
railway variables --set "MYTHARA_PILOT_PRICE_USD=49"
railway variables --set "STRIPE_WEBHOOK_SECRET=whsec_YYgRgpA0oUD9yCoaY2vcKWWraNQmnDH7"
railway variables --set "SENDGRID_API_KEY=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"
railway variables --set "MYTHARA_PILOT_PURCHASE_URL=https://buy.stripe.com/test_dRm28s5XKbpm2Dk41KgjC00"
railway variables --set "STRIPE_LINK_FOUNDATION=https://buy.stripe.com/test_28E9AU85SfFCa5MbucgjC01"
railway variables --set "STRIPE_LINK_PROFESSIONAL=https://buy.stripe.com/test_28E3cw99Wbpm91I2XGgjC02"
railway variables --set "STRIPE_LINK_CORPORATE=https://buy.stripe.com/test_3cI00k3PC3WU91Iaq8gjC03"
railway variables --set "STRIPE_LINK_ENTERPRISE=https://buy.stripe.com/test_6oUbJ2bi4fFC7XE41KgjC04"
railway variables --set "STRIPE_LINK_SOVEREIGN=https://buy.stripe.com/test_00wbJ22Lyali3HofKsgjC05"

echo ""
echo "🚀 Deploying to Railway..."
railway up --detach

echo ""
echo "⏳ Waiting for deployment to complete (45 seconds)..."
sleep 45

echo ""
echo "🔍 Getting deployment URL..."
RAILWAY_URL=$(railway domain 2>/dev/null || echo "")

if [ -z "$RAILWAY_URL" ]; then
    echo "⚠️  Could not auto-detect Railway URL."
    echo "Please get your URL from Railway dashboard and run:"
    echo ""
    echo "  railway variables --set \"MYTHARA_PILOT_DOWNLOAD_URL=https://YOUR-URL/download/pilot\""
    echo ""
else
    echo "✅ Railway URL: https://$RAILWAY_URL"
    railway variables --set "MYTHARA_PILOT_DOWNLOAD_URL=https://$RAILWAY_URL/download/pilot"
    
    echo ""
    echo "🧪 Testing deployment..."
    echo ""
    
    echo "Testing /health endpoint..."
    curl -s "https://$RAILWAY_URL/health" | jq . || echo "⚠️  Health check failed"
    
    echo ""
    echo "Testing /pricing page..."
    curl -I "https://$RAILWAY_URL/pricing" 2>/dev/null | head -1
    
    echo ""
    echo "=========================================="
    echo "  ✅ Deployment Complete!"
    echo "=========================================="
    echo ""
    echo "Your Mythara Engine is now live at:"
    echo ""
    echo "  🌐 Pricing Page: https://$RAILWAY_URL/pricing"
    echo "  📦 API Docs:     https://$RAILWAY_URL/docs"
    echo "  💚 Health:       https://$RAILWAY_URL/health"
    echo ""
    echo "Next steps:"
    echo "  1. Test the pricing page"
    echo "  2. Update Stripe webhook URL to: https://$RAILWAY_URL/api/webhooks/stripe"
    echo "  3. Test a pilot purchase"
    echo ""
fi
