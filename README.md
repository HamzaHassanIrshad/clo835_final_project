# 🚀 CLO835 Final Project - Complete Containerized Web Application

> **The Ultimate Guide to Deploying a Containerized Flask Application with MySQL on Amazon EKS**

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue?logo=github-actions)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-blue?logo=kubernetes)](https://kubernetes.io/)
[![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazon-aws)](https://aws.amazon.com/eks/)

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🏗️ Architecture](#️-architecture)
- [📋 Prerequisites](#-prerequisites)
- [⚡ Quick Start](#-quick-start)
- [🔧 Detailed Setup](#-detailed-setup)
- [🚀 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📊 Monitoring & Scaling](#-monitoring--scaling)

- [🔍 Troubleshooting](#-troubleshooting)
- [🧹 Cleanup](#-cleanup)
- [📚 Reference](#-reference)

## 🎯 Project Overview

This is a **CLO835 Final Project** that demonstrates a complete modern cloud-native application stack:

### ✨ Features

- **🎨 Dynamic Background Images** from S3 bucket (configurable via ConfigMap)
- **👤 Student Name Display** in application header
- **🗄️ MySQL Database** with persistent storage
- **🔐 Secure Credentials** management with Kubernetes Secrets
- **🚀 Automated CI/CD** with GitHub Actions
- **📦 Container Registry** on Amazon ECR
- **☸️ Kubernetes Orchestration** on Amazon EKS
- **📈 Auto-scaling** with Horizontal Pod Autoscaler (HPA)

### 🏆 Assignment Requirements Met

- ✅ Enhanced web application with background image
- ✅ ConfigMap for background image URL and student name
- ✅ Secrets for MySQL database credentials
- ✅ Port 81 configuration for Flask application
- ✅ GitHub Actions CI/CD pipeline
- ✅ Amazon ECR integration
- ✅ EKS cluster with 2 worker nodes
- ✅ All required Kubernetes manifests
- ✅ Persistent storage (2Gi PVC with gp2 storage class)
- ✅ ServiceAccount with IRSA for S3 access
- ✅ Role/RoleBinding for namespace permissions
- ✅ LoadBalancer service for internet access
- ✅ HPA for auto-scaling (Bonus)

## 🏗️ Architecture

**CI/CD Pipeline:**

- **GitHub Repository** → **GitHub Actions** → **Amazon ECR**
- Code changes trigger automated builds and push Docker images to ECR

**Deployment:**

- **GitHub Actions** builds and pushes Docker images to **ECR**
- **EKS Cluster** pulls Docker images from **ECR** and deploys the application

**Application Stack:**

- **Flask Application** (Frontend/Backend)
- **MySQL Database** (Persistent storage)
- **S3 Bucket** (Background images)

**Data Flow:**

1. Code pushed to GitHub
2. GitHub Actions builds and pushes Docker image to ECR
3. Manual deployment to EKS using kubectl
4. Application runs with MySQL database
5. Application fetches background images from S3

## 🔒 Security Best Practices

### ⚠️ **CRITICAL: Never Commit Credentials!**

**This project contains sensitive AWS credentials. Follow these security practices:**

1. **Never commit credentials to Git**

   - AWS access keys, secret keys, and session tokens
   - Database passwords
   - Private keys or certificates

2. **Use .gitignore properly**

   - The `.gitignore` file is configured to exclude sensitive files
   - Always check what you're committing with `git status`

3. **Use temporary files for secrets**

   - Create secrets dynamically during deployment
   - Delete temporary files immediately after use

4. **Rotate credentials regularly**

   - AWS Academy credentials expire automatically
   - Update your local credentials when they change

5. **Check your commits**
   - Use `git log --oneline` to review recent commits
   - If credentials were accidentally committed, remove them immediately

### 🛡️ **If Credentials Were Committed:**

```bash
# Remove from git history (if credentials were committed)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch k8s/aws-credentials-secret.yaml" \
  --prune-empty --tag-name-filter cat -- --all

# Force push to remove from remote repository
git push origin --force --all
```

## 📋 Prerequisites

### 🛠️ Required Tools (AWS Cloud9)

**Complete Cloud9 Setup:**

```bash
# 1. Install AWS CLI v2 and disable Cloud9 temporary credentials
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update

# Verify AWS CLI version
/usr/local/bin/aws --version

# Disable Cloud9 temporary credentials
/usr/local/bin/aws cloud9 update-environment --environment-id $C9_PID --managed-credentials-action DISABLE

# Remove existing credentials
rm -vf ${HOME}/.aws/credentials

# 2. Install required tools
sudo yum -y install jq gettext bash-completion moreutils

# 3. Install eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv -v /tmp/eksctl /usr/local/bin

# Enable eksctl bash completion
eksctl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion

# 4. Install kubectl (version 1.29.0 as of Winter 2025)
export VERSION=v1.29.0
curl -LO "https://dl.k8s.io/release/$VERSION/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -f ./kubectl

# Optional: kubectl bash completion
kubectl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion

# Optional: Add kubectl alias
echo "alias k=kubectl" >> ~/.bashrc
. ~/.bashrc

# 5. Set LoadBalancer Controller version
echo 'export LBC_VERSION="v2.4.1"' >> ~/.bash_profile
echo 'export LBC_CHART_VERSION="1.4.1"' >> ~/.bash_profile
. ~/.bash_profile


```

**Important Notes:**

- Use AWS CLI v2 (not v1)
- Disable Cloud9 temporary credentials
- Use kubectl version 1.29.0 (matches EKS cluster version)
- Configure permanent AWS credentials from AWS Academy

### 🔑 Required Accounts & Permissions

- **AWS Account** with EKS, ECR, S3, and IAM permissions
- **GitHub Account** with repository access
- **AWS IAM User** with programmatic access

### 🔐 AWS Credentials Setup

**After running the Cloud9 setup commands above:**

1. **Get your AWS Academy credentials** from the AWS Details page
2. **Create credentials file:**

   ```bash
   # Create the credentials file
   mkdir -p ~/.aws
   cat > ~/.aws/credentials << EOF
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY_HERE
   aws_secret_access_key = YOUR_SECRET_KEY_HERE
   aws_session_token = YOUR_SESSION_TOKEN_HERE
   region = us-east-1
   output = json
   EOF
   ```

3. **Replace the placeholders** with your actual AWS Academy credentials (including the session token)
4. **Verify credentials work:**
   ```bash
   aws sts get-caller-identity
   ```

## ⚡ Quick Start

### 1. Prerequisites Check

```bash
# Verify tools are installed
eksctl version
kubectl version --client
aws --version

# Verify AWS credentials
aws sts get-caller-identity
```

### 2. Create S3 Bucket and Upload Background Image

#### Via AWS Console:

1. Go to AWS S3 Console
2. Click "Create bucket"
3. **Bucket name**: `clo835-final-project-bucket-g5`
4. **Region**: US East (N. Virginia) us-east-1
5. **Block Public Access**: Check "Block all public access"
6. **Object Ownership**: Select "ACLs disabled (recommended)"
7. Click "Create bucket"

#### Upload Background Image:

1. Click on your bucket name
2. Click "Upload"
3. Create a file called `background.svg` with this content:

```svg
<svg width="1200" height="800" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#764ba2;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#f093fb;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#grad1)"/>
  <text x="600" y="300" font-family="Arial, sans-serif" font-size="48" fill="white" text-anchor="middle" font-weight="bold">CLO835 Final Project</text>
  <text x="600" y="350" font-family="Arial, sans-serif" font-size="24" fill="white" text-anchor="middle">Container Orchestration with Kubernetes</text>
  <text x="600" y="400" font-family="Arial, sans-serif" font-size="18" fill="white" text-anchor="middle">Hamza, Sanjan Joshua, Rentian Zhang - CLO835 Students</text>
</svg>
```

4. Upload it as `background.svg`
5. Set permissions: "No additional permissions needed" (since bucket blocks public access)
6. Click "Upload"

### 3. Create EKS Cluster

```bash
# Create the cluster using the provided configuration
eksctl create cluster -f eks-config.yaml

# Update your Kube config
aws eks update-kubeconfig --name clo835-final-project --region us-east-1

# Verify cluster
kubectl get nodes
```

**Important Notes:**

- This takes 15-20 minutes to complete
- Monitor CloudFormation console to see resources being created
- The `eks-config.yaml` uses existing IAM roles to avoid permission issues

### 4. Deploy Application

```bash
# Create namespace
kubectl create namespace final

# Deploy all resources (excluding credentials)
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/role.yaml

# Deploy AWS credentials secret (created dynamically)
# Follow the "Update AWS Credentials Secret" section above

kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
kubectl apply -f k8s/hpa.yaml
```

### 5. Verify Deployment

```bash
# Check all resources
kubectl get all -n final

# Check services
kubectl get svc -n final

# Check pods
kubectl get pods -n final

# Watch pods starting up
kubectl get pods -n final -w
```

### 6. Access Your Application

```bash
# Get the LoadBalancer URL
kubectl get svc flask-service -n final

# Look for EXTERNAL-IP or LoadBalancer hostname
# Open the URL in your browser
```

## 🔧 Detailed Setup

### Step 1: Update Configuration Files

#### Update ConfigMap

```bash
# Edit k8s/configmap.yaml
vim k8s/configmap.yaml

# Replace with your actual values:
# BACKGROUND_IMAGE_URL: "https://clo835-final-project-bucket-g5.s3.amazonaws.com/background.svg"
# MY_NAME: "Hamza, Sanjan Joshua, Rentian Zhang (CLO835 Students)"
```

#### Update Flask Deployment

```bash
# Get your AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Update the image URL
sed -i "s/YOUR_ACCOUNT_ID/$AWS_ACCOUNT_ID/g" k8s/flask-deployment.yaml
```

#### Update ServiceAccount

```bash
# Update the IAM role ARN
sed -i "s/YOUR_ACCOUNT_ID/$AWS_ACCOUNT_ID/g" k8s/serviceaccount.yaml
```

#### Update AWS Credentials Secret

**⚠️ IMPORTANT: Never commit credentials to Git!**

```bash
# Get your AWS credentials from ~/.aws/credentials
AWS_ACCESS_KEY=$(grep aws_access_key_id ~/.aws/credentials | cut -d'=' -f2 | tr -d ' ')
AWS_SECRET_KEY=$(grep aws_secret_access_key ~/.aws/credentials | cut -d'=' -f2 | tr -d ' ')
AWS_SESSION_TOKEN=$(grep aws_session_token ~/.aws/credentials | cut -d'=' -f2 | tr -d ' ')

# Base64 encode the credentials
ACCESS_KEY_B64=$(echo -n "$AWS_ACCESS_KEY" | base64)
SECRET_KEY_B64=$(echo -n "$AWS_SECRET_KEY" | base64)
SESSION_TOKEN_B64=$(echo -n "$AWS_SESSION_TOKEN" | base64)

# Create a temporary secret file (DO NOT COMMIT THIS!)
cat > k8s/aws-credentials-secret-temp.yaml << EOF
apiVersion: v1
kind: Secret
metadata:
  name: aws-credentials
  namespace: final
type: Opaque
data:
  access-key-id: $ACCESS_KEY_B64
  secret-access-key: $SECRET_KEY_B64
  session-token: $SESSION_TOKEN_B64
EOF

# Apply the secret and then delete the temp file
kubectl apply -f k8s/aws-credentials-secret-temp.yaml
rm k8s/aws-credentials-secret-temp.yaml
```

### Step 2: GitHub Configuration

#### Set Up GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token
```

```bash
# Note: Repository URLs are already configured correctly
# No updates required for this project
```

**Important**: If using AWS Academy, ensure your session token is included in your AWS credentials.

## 🚀 Deployment

### Option 1: Manual Deployment (Recommended for Beginners)

```bash
# Create EKS cluster
eksctl create cluster -f eks-config.yaml

# Update kubeconfig
aws eks update-kubeconfig --name clo835-final-project --region us-east-1

# Deploy all resources
kubectl apply -f k8s/

# Check deployment status
kubectl get all -n final
```

## 🧪 Testing

### Local Testing

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the test script
python test_app.py

# Build and run Docker container locally
docker build -t clo835-app .
docker run -p 81:81 clo835-app

# Test locally
curl http://localhost:81
```

### Application Testing

```bash
# Get the LoadBalancer URL
LOADBALANCER_URL=$(kubectl get service flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test the application
curl http://$LOADBALANCER_URL

# Test database connectivity
kubectl exec -it deployment/mysql -n final -- mysql -u root -p -e "SHOW DATABASES;"

# Test S3 access
kubectl exec -it deployment/flask-app -n final -- python -c "
import boto3
s3 = boto3.client('s3')
print('S3 access working')
"
```

### Load Testing (for HPA)

```bash
# Install hey (load testing tool)
curl -s https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64 -o hey
chmod +x hey

# Run load test
./hey -n 1000 -c 10 http://$LOADBALANCER_URL

# Check HPA status
kubectl get hpa -n final
kubectl describe hpa flask-app-hpa -n final
```

## 📊 Monitoring & Scaling

### Check Application Status

```bash
# Check all resources
kubectl get all -n final

# Check pod logs
kubectl logs deployment/flask-app -n final
kubectl logs deployment/mysql -n final

# Check pod status
kubectl describe pods -n final

# Check events
kubectl get events -n final --sort-by='.lastTimestamp'
```

### Monitor HPA

```bash
# Check HPA status
kubectl get hpa -n final

# Describe HPA
kubectl describe hpa flask-app-hpa -n final

# Check metrics
kubectl top pods -n final
kubectl top nodes
```

### Scale Manually

```bash
# Scale Flask app manually
kubectl scale deployment flask-app --replicas=3 -n final

# Check scaling
kubectl get pods -n final
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. EKS Cluster Creation Fails

**Problem**: `eksctl create cluster` fails with IAM permission errors

**Solution**: Use the provided `eks-config.yaml` file that uses existing IAM roles:

```bash
# Use the working configuration
eksctl create cluster -f eks-config.yaml
```

#### 2. Pod Stuck in Pending

```bash
# Check pod events
kubectl describe pod <pod-name> -n final

# Check node resources
kubectl describe nodes

# Check if there are enough resources
kubectl get nodes -o custom-columns="NAME:.metadata.name,CPU:.status.capacity.cpu,MEMORY:.status.capacity.memory"
```

#### 3. Image Pull Errors

```bash
# Check if image exists in ECR
aws ecr describe-images --repository-name clo835-final-project --region us-east-1

# Check pod events for image pull errors
kubectl describe pod <pod-name> -n final | grep -A 10 "Events:"
```

#### 4. Database Connection Issues

```bash
# Check MySQL pod status
kubectl get pods -n final -l app=mysql

# Check MySQL logs
kubectl logs deployment/mysql -n final

# Test database connectivity
kubectl exec -it deployment/mysql -n final -- mysql -u root -p -e "SHOW DATABASES;"
```

#### 5. S3 Access Issues

```bash
# Check pod annotations
kubectl get pod <pod-name> -n final -o yaml | grep -A 5 -B 5 "serviceAccountName"

# Test S3 access from pod
kubectl exec -it deployment/flask-app -n final -- python -c "
import boto3
s3 = boto3.client('s3')
try:
    s3.list_buckets()
    print('S3 access working')
except Exception as e:
    print(f'S3 access failed: {e}')
"
```

#### 6. LoadBalancer Issues

```bash
# Check LoadBalancer status
kubectl get service flask-service -n final

# Check if LoadBalancer has external IP
kubectl describe service flask-service -n final
```

### Recent Deployment Issues and Solutions

#### Issue 1: AWS Credentials Secret Not Found

**Problem**: Flask pod fails with `Error: secret "aws-credentials" not found`

**Root Cause**: The deployment was trying to use AWS credentials from a secret that doesn't exist.

**Solution**: Remove AWS credential environment variables from the deployment since we're using IRSA:

```bash
# Delete the problematic deployment
kubectl delete deployment flask-app -n final

# Edit k8s/flask-deployment.yaml to remove AWS credential env vars
# Remove these lines:
# - name: AWS_ACCESS_KEY_ID
#   valueFrom:
#     secretKeyRef:
#       name: aws-credentials
#       key: access-key-id
# - name: AWS_SECRET_ACCESS_KEY
#   valueFrom:
#     secretKeyRef:
#       name: aws-credentials
#       key: secret-access-key
# - name: AWS_SESSION_TOKEN
#   valueFrom:
#     secretKeyRef:
#       name: aws-credentials
#       key: session-token

# Reapply the fixed deployment
kubectl apply -f k8s/flask-deployment.yaml
```

#### Issue 2: PVC Stuck in Pending Status

**Problem**: MySQL pod can't schedule because PVC is not bound

**Root Cause**: EBS CSI driver not installed or not working properly

**Solution**: Install the EBS CSI driver addon:

```bash
# Install EBS CSI driver
eksctl create addon --name aws-ebs-csi-driver --cluster clo835-final-project --region us-east-1 --force

# Check PVC status
kubectl get pvc -n final

# Check EBS CSI driver pods
kubectl get pods -n kube-system | grep ebs
```

#### Issue 3: No Worker Nodes Available

**Problem**: `0/2 nodes are available: no nodes available to schedule pods`

**Root Cause**: EKS cluster created without worker nodes

**Solution**: Ensure the eks-config.yaml includes managedNodeGroups:

```yaml
managedNodeGroups:
  - name: clo835-workers
    instanceType: t3.medium
    desiredCapacity: 2
    minSize: 2
    maxSize: 4
```

### Debug Commands

```bash
# Get detailed information about resources
kubectl describe <resource-type> <resource-name> -n final

# Check logs with timestamps
kubectl logs <pod-name> -n final --timestamps

# Follow logs in real-time
kubectl logs <pod-name> -n final -f

# Execute commands in pods
kubectl exec -it <pod-name> -n final -- /bin/bash

# Port forward for debugging
kubectl port-forward deployment/flask-app 8080:81 -n final
```

## 🧹 Cleanup

### Automated Cleanup

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/ --ignore-not-found=true
kubectl delete namespace final --ignore-not-found=true

# Delete EKS cluster
eksctl delete cluster --name clo835-final-project --region us-east-1

# Delete ECR repository
aws ecr delete-repository --repository-name clo835-final-project --force --region us-east-1

# Delete S3 bucket
aws s3 rb s3://clo835-final-project-bucket-g5 --force
```

### Verify Cleanup

```bash
# Check if cluster is deleted
eksctl get cluster --region us-east-1

# Check if ECR repository is deleted
aws ecr describe-repositories --region us-east-1

# Check if S3 bucket is deleted
aws s3 ls s3://clo835-final-project-bucket-g5
```

## 📚 Reference

### 🚀 Quick Deployment Commands

```bash
# Complete deployment in one go
eksctl create cluster -f eks-config.yaml
aws eks update-kubeconfig --name clo835-final-project --region us-east-1

# Install EBS CSI driver (required for PVC)
eksctl create addon --name aws-ebs-csi-driver --cluster clo835-final-project --region us-east-1 --force

# Deploy all resources
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/serviceaccount.yaml
kubectl apply -f k8s/role.yaml
kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml
kubectl apply -f k8s/flask-deployment.yaml
kubectl apply -f k8s/flask-service.yaml
kubectl apply -f k8s/hpa.yaml

# Check deployment status
kubectl get all -n final
kubectl get pvc -n final
```

### 🔧 Quick Update Commands

```bash
# Update ConfigMap
kubectl patch configmap app-config -n final -p '{"data":{"BACKGROUND_IMAGE_URL":"https://new-image-url"}}'

# Restart deployment to pick up changes
kubectl rollout restart deployment/flask-app -n final

# Check status
kubectl get pods -n final
```

### 🧪 Quick Testing Commands

```bash
# Test application
curl $(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test database
kubectl exec -it deployment/mysql -n final -- mysql -u root -p -e "SHOW DATABASES;"

# Load test for HPA
hey -n 1000 -c 10 http://$(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
```

### Useful Commands Cheat Sheet

#### Kubernetes Commands

```bash
# Get all resources
kubectl get all -n final

# Get specific resources
kubectl get pods,services,deployments -n final

# Describe resources
kubectl describe pod <pod-name> -n final

# Logs
kubectl logs <pod-name> -n final

# Execute commands
kubectl exec -it <pod-name> -n final -- /bin/bash

# Port forward
kubectl port-forward service/flask-service 8080:80 -n final

# Scale deployments
kubectl scale deployment flask-app --replicas=3 -n final

# Rollout restart
kubectl rollout restart deployment/flask-app -n final

# Check rollout status
kubectl rollout status deployment/flask-app -n final
```

#### AWS Commands

```bash
# EKS
eksctl get cluster --region us-east-1
eksctl get nodegroup --cluster clo835-cluster --region us-east-1

# ECR
aws ecr describe-repositories --region us-east-1
aws ecr describe-images --repository-name clo835-final-project --region us-east-1

# S3
aws s3 ls s3://clo835-final-project-bucket-g5/
aws s3 cp local-file.jpg s3://clo835-final-project-bucket-g5/
```

#### Docker Commands

```bash
# Build image
docker build -t clo835-app .

# Run container
docker run -p 81:81 clo835-app

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
docker tag clo835-app:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/clo835-final-project:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/clo835-final-project:latest
```

### Configuration Files Reference

#### Environment Variables

```bash
# Database
DBHOST=mysql-service
DBUSER=root
DBPWD=password
DATABASE=employees
DBPORT=3306

# Application
BACKGROUND_IMAGE_URL=https://clo835-final-project-bucket-g5.s3.amazonaws.com/background.svg
MY_NAME=Hamza Hassan, Sanjan Joshua, Rentian Zhang (CLO835 Students)
```

#### Important URLs

- **Application**: http://LOADBALANCER_URL
- **ECR Repository**: https://console.aws.amazon.com/ecr/repositories/clo835-final-project
- **EKS Cluster**: https://console.aws.amazon.com/eks/clusters/clo835-final-project
- **S3 Bucket**: https://console.aws.amazon.com/s3/buckets/clo835-final-project-bucket-g5

## 📸 Screenshots & Demo

### Application Screenshots

- **Home Page**: Show the application with background image and student name
- **Add Employee**: Demonstrate adding new employee records
- **Get Employee**: Show retrieving employee information
- **Database Persistence**: Show data persistence after pod restart

### Deployment Screenshots

- **EKS Cluster**: Kubernetes dashboard showing running pods
- **LoadBalancer**: Application accessible via internet
- **HPA in Action**: Auto-scaling demonstration
- **GitHub Actions**: CI/CD pipeline success

### Demo Video Requirements

1. **Local Testing**: Docker container running locally
2. **GitHub Actions**: Show automated build and push to ECR
3. **EKS Deployment**: Deploy all manifests to empty namespace
4. **S3 Integration**: Background image loading from private S3 bucket
5. **Data Persistence**: Delete/recreate MySQL pod, data remains
6. **Internet Access**: LoadBalancer URL accessible from browser
7. **ConfigMap Update**: Change background image, see changes
8. **Bonus HPA**: Load testing showing auto-scaling

## 🎓 Assignment Submission Checklist

Before submitting your assignment, ensure you have:

### 🔒 **Security Checklist (CRITICAL!)**

- [ ] **No credentials committed to Git**

  - [ ] AWS access keys not in repository
  - [ ] AWS secret keys not in repository
  - [ ] AWS session tokens not in repository
  - [ ] Database passwords not in repository
  - [ ] All sensitive files in .gitignore

- [ ] **Repository is secure**
  - [ ] Run `git log --oneline` to check recent commits
  - [ ] No sensitive data in commit history
  - [ ] .gitignore properly configured
  - [ ] Credentials handled dynamically during deployment

### 📋 **Project Requirements Checklist**

- ✅ **Application Enhancement**

  - [ ] Background image loads from S3
  - [ ] Student name displays in header
  - [ ] Application runs on port 81
  - [ ] Database logging for background image URL

- ✅ **CI/CD Pipeline**

  - [ ] GitHub Actions workflow configured
  - [ ] Docker image builds successfully
  - [ ] Image pushed to ECR
  - [ ] Tests pass

- ✅ **Kubernetes Deployment**

  - [ ] EKS cluster with 2 worker nodes
  - [ ] All manifests deployed successfully
  - [ ] Application accessible via LoadBalancer
  - [ ] Database connectivity working
  - [ ] S3 access working

- ✅ **Bonus Features**

  - [ ] HPA configured and working

  - [ ] Auto-scaling demonstrated

- ✅ **Documentation**
  - [ ] README updated with your information
  - [ ] Deployment process documented
  - [ ] Screenshots/videos of working application

## 🤝 Support

### Getting Help

1. **Check the troubleshooting section** above
2. **Review the logs** using `kubectl logs`
3. **Check AWS Console** for resource status
4. **Consult course materials** for Kubernetes concepts

### Common Issues

- **Image pull errors**: Check ECR repository and authentication
- **Database connection**: Verify MySQL pod is running and service is accessible
- **S3 access**: Check IAM role and bucket permissions
- **LoadBalancer**: Ensure security groups allow traffic

### Useful Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)

- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📋 Version Information

- **Kubernetes Version**: 1.29.0
- **EKS Version**: 1.29
- **Flask Version**: Latest
- **MySQL Version**: 8.0
- **Docker Base Image**: python:3.9-slim
- **AWS Region**: us-east-1
- **Last Updated**: Winter 2025

## 📄 License

This project is created for educational purposes as part of the CLO835 course at Seneca College.

---

**🎉 Congratulations! You now have a complete, production-ready containerized application deployed on Amazon EKS with full CI/CD pipeline and auto-scaling capabilities!**
