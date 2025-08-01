# 🚀 CLO835 Final Project - Cloud9 Setup Guide

## Quick Setup for AWS Cloud9

### 1. Verify Pre-installed Tools

```bash
# Check AWS CLI
aws --version

# Check kubectl
kubectl version --client

# Check eksctl
eksctl version

# Check Docker
docker --version
```

### 2. Configure AWS Credentials

```bash
# Configure AWS CLI (if not already done)
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (us-east-1)
# Enter your output format (json)
```

### 3. Update Tools (if needed)

```bash
# Update kubectl to latest version
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install eksctl (if not present)
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin
```

### 4. Create AWS Resources

```bash
# Get your AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Your AWS Account ID: $AWS_ACCOUNT_ID"

# Create ECR repository
aws ecr create-repository --repository-name clo835-final-project --region us-east-1

# Create S3 bucket (replace with your bucket name)
aws s3 mb s3://your-clo835-background-images --region us-east-1

# Upload a background image
aws s3 cp /path/to/your/background.jpg s3://your-clo835-background-images/background.jpg
```

### 5. Update Configuration Files

```bash
# Update ConfigMap with your S3 bucket URL
sed -i "s|https://your-s3-bucket.s3.amazonaws.com/background.jpg|https://your-clo835-background-images.s3.amazonaws.com/background.jpg|g" k8s/configmap.yaml

# Update Flask deployment with your ECR repository
sed -i "s|YOUR_ACCOUNT_ID|$AWS_ACCOUNT_ID|g" k8s/flask-deployment.yaml

# Update ServiceAccount with your IAM role
sed -i "s|YOUR_ACCOUNT_ID|$AWS_ACCOUNT_ID|g" k8s/serviceaccount.yaml
```

### 6. Deploy to EKS

```bash
# Create EKS cluster
eksctl create cluster \
  --name clo835-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed \
  --with-oidc

# Update kubeconfig
aws eks update-kubeconfig --name clo835-cluster --region us-east-1

# Deploy all resources
kubectl apply -f k8s/

# Check deployment status
kubectl get all -n final
```

### 7. Access Your Application

```bash
# Get the LoadBalancer URL
kubectl get service flask-service -n final

# The URL will be displayed in the EXTERNAL-IP column
```

### 8. Test Your Application

```bash
# Test locally first
python test_app.py

# Build and test Docker image
docker build -t clo835-app .
docker run -p 81:81 clo835-app

# Test the deployed application
curl http://LOADBALANCER_URL
```

### 9. Monitor and Scale

```bash
# Check application status
kubectl get all -n final

# Check HPA status
kubectl get hpa -n final

# Check logs
kubectl logs deployment/flask-app -n final
kubectl logs deployment/mysql -n final
```

### 10. Cleanup (when done)

```bash
# Delete all resources
kubectl delete -f k8s/ --ignore-not-found=true
kubectl delete namespace final --ignore-not-found=true
eksctl delete cluster --name clo835-cluster --region us-east-1

# Delete AWS resources
aws ecr delete-repository --repository-name clo835-final-project --force --region us-east-1
aws s3 rb s3://your-clo835-background-images --force
```

## 🎯 Key Benefits of Cloud9

- **Pre-installed tools**: AWS CLI, kubectl, Docker, and more
- **Integrated terminal**: No need for local setup
- **IAM integration**: Automatic credential management
- **Cost-effective**: No need for local development environment
- **Collaborative**: Share environment with team members

## 📝 Notes

- All commands run in the Cloud9 terminal
- No need to install tools locally
- Use the integrated file editor for configuration changes
- Take advantage of Cloud9's built-in Git integration
- Use the preview feature to test your application

## 🚨 Important

- Remember to update the S3 bucket name and image path
- Update the ECR repository URL with your AWS Account ID
- Set up GitHub secrets for CI/CD pipeline
- Monitor costs in AWS Console
