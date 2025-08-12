#!/bin/bash
# AWS Frontend Deployment Script

echo "🚀 Building ValuAI Frontend for AWS S3 + CloudFront"

# Build the React app
cd client
npm run build

# Install AWS CLI if not present
if ! command -v aws &> /dev/null; then
    echo "Installing AWS CLI..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
fi

# Create S3 bucket (replace with your bucket name)
BUCKET_NAME="valuai-frontend-$(date +%s)"
aws s3 mb s3://$BUCKET_NAME

# Enable static website hosting
aws s3 website s3://$BUCKET_NAME \
    --index-document index.html \
    --error-document error.html

# Upload build files
aws s3 sync dist/ s3://$BUCKET_NAME --delete

# Set public read policy
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::'$BUCKET_NAME'/*"
        }
    ]
}'

echo "✅ Frontend deployed to: http://$BUCKET_NAME.s3-website-us-east-1.amazonaws.com"
