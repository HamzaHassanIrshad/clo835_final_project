# 🚀 CLO835 Final Project - Complete Containerized Web Application

> **The Ultimate Guide to Deploying a Containerized Flask Application with MySQL on Amazon EKS**

[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-blue?logo=github-actions)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-blue?logo=kubernetes)](https://kubernetes.io/)
[![AWS EKS](https://img.shields.io/badge/AWS-EKS-orange?logo=amazon-aws)](https://aws.amazon.com/eks/)
[![Flux](https://img.shields.io/badge/Flux-GitOps-purple?logo=flux)](https://fluxcd.io/)

## 📋 Table of Contents

- [🎯 Project Overview](#-project-overview)
- [🏗️ Architecture](#️-architecture)
- [📋 Prerequisites](#-prerequisites)
- [⚡ Quick Start (5 Minutes)](#-quick-start-5-minutes)
- [🔧 Detailed Setup](#-detailed-setup)
- [🚀 Deployment](#-deployment)
- [🧪 Testing](#-testing)
- [📊 Monitoring & Scaling](#-monitoring--scaling)
- [🔄 GitOps with Flux](#-gitops-with-flux)
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
- **🔄 GitOps** deployment with Flux (Bonus)

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
- ✅ Flux GitOps deployment (Bonus)

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub Repo   │───▶│  GitHub Actions  │───▶│  Amazon ECR     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                                              │
         │                                              │
         ▼                                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Flux (GitOps) │───▶│  Amazon EKS      │◀───│  Docker Image   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  Application     │
                    │  ┌─────────────┐ │
                    │  │   Flask     │ │
                    │  │   App       │ │
                    │  └─────────────┘ │
                    │  ┌─────────────┐ │
                    │  │   MySQL     │ │
                    │  │  Database   │ │
                    │  └─────────────┘ │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  S3 Bucket       │
                    │  (Background     │
                    │   Images)        │
                    └──────────────────┘
```

## 📋 Prerequisites

### 🛠️ Required Tools (AWS Cloud9)

Since you're using AWS Cloud9, most tools are pre-installed. You may need to update some:

```bash
# Update AWS CLI (if needed)
pip install --upgrade awscli

# Update kubectl (if needed)
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install eksctl (if not already installed)
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# Install Flux CLI (for GitOps)
curl -s https://fluxcd.io/install.sh | sudo bash
```

### 🔑 Required Accounts & Permissions

- **AWS Account** with EKS, ECR, S3, and IAM permissions
- **GitHub Account** with repository access
- **AWS IAM User** with programmatic access

### 💰 Cost Estimation

- **EKS Cluster**: ~$0.10/hour per node (2 nodes = ~$0.20/hour)
- **ECR Storage**: ~$0.10/GB/month
- **S3 Storage**: ~$0.023/GB/month
- **Load Balancer**: ~$0.0225/hour
- **Total**: ~$15-20/month for development

## ⚡ Quick Start (Step-by-Step Commands)

### 1. Prerequisites Check

```bash
# Verify tools are installed
eksctl version
kubectl version --client
aws --version

# Configure AWS credentials (if not already done)
aws configure
```

### 2. Create S3 Bucket and Upload Background Image

#### Via AWS Console:

1. Go to AWS S3 Console
2. Click "Create bucket"
3. **Bucket name**: `clo835-background-images`
4. **Region**: US East (N. Virginia) us-east-1
5. **Block Public Access**: Uncheck "Block all public access"
6. **Object Ownership**: Select "ACLs enabled"
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
  <text x="600" y="400" font-family="Arial, sans-serif" font-size="18" fill="white" text-anchor="middle">Hamza - CLO835 Student</text>
</svg>
```

4. Upload it as `background.jpg`
5. Set permissions: "Grant public-read access"
6. Click "Upload"

### 3. Create EKS Cluster

#### Using ClusterConfig File (Recommended):

```bash
# Create EKS cluster using the provided configuration
eksctl create cluster -f eks-config.yaml

# Update kubeconfig
aws eks update-kubeconfig --name clo835-cluster --region us-east-1

# Verify cluster
kubectl get nodes
```

**Note**: This takes 15-20 minutes to complete.

### 4. Deploy Application

```bash
# Create namespace
kubectl create namespace final

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

### Step 1: AWS Configuration

#### Configure AWS CLI

```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (us-east-1)
# Enter your output format (json)
```

#### EKS Cluster Configuration

The project includes a working `eks-config.yaml` file that uses existing IAM roles to avoid permission issues:

```yaml
---
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: clo835-cluster
  region: "us-east-1"
  version: "1.29"

availabilityZones: ["us-east-1a", "us-east-1b", "us-east-1c"]

iam:
  serviceRoleARN: arn:aws:iam::626108377158:role/LabRole

managedNodeGroups:
  - name: clo835-workers
    instanceType: t3.medium
    desiredCapacity: 2
    minSize: 2
    maxSize: 4
    iam:
      instanceRoleARN: arn:aws:iam::626108377158:role/LabRole
    ssh:
      enableSsm: true
```

**To create the cluster:**

```bash
eksctl create cluster -f eks-config.yaml
```

#### Create IAM Role for S3 Access

```bash
# Create trust policy
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::YOUR_ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
EOF

# Create the role
aws iam create-role \
  --role-name CLO835-S3-Access-Role \
  --assume-role-policy-document file://trust-policy.json

# Attach S3 read policy
aws iam attach-role-policy \
  --role-name CLO835-S3-Access-Role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

#### Create S3 Bucket and Upload Image

```bash
# Create bucket
aws s3 mb s3://your-clo835-background-images --region us-east-1

# Make bucket private
aws s3api put-bucket-acl \
  --bucket your-clo835-background-images \
  --acl private

# Upload a background image
aws s3 cp /path/to/your/background.jpg s3://your-clo835-background-images/background.jpg

# Verify upload
aws s3 ls s3://your-clo835-background-images/
```

### Step 2: GitHub Configuration

#### Set Up GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
```

#### Update Repository URLs

```bash
# Update Flux configuration with your GitHub username
sed -i 's/YOUR_USERNAME/your-actual-github-username/g' flux/gotk-sync.yaml
```

### Step 3: Update Configuration Files

#### Update ConfigMap

```bash
# Edit k8s/configmap.yaml
vim k8s/configmap.yaml

# Replace with your actual values:
# BACKGROUND_IMAGE_URL: "https://your-clo835-background-images.s3.amazonaws.com/background.jpg"
# MY_NAME: "Your Name (CLO835 Student)"
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

## 🚀 Deployment

### Option 1: Automated Deployment (Recommended)

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

### Option 2: Manual Deployment

#### Create EKS Cluster

```bash
# Create cluster with eksctl
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

# Verify cluster
kubectl get nodes
```

#### Deploy Application

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Deploy all resources
kubectl apply -f k8s/

# Check deployment status
kubectl get all -n final

# Watch pods starting up
kubectl get pods -n final -w
```

#### Verify Deployment

```bash
# Check all resources
kubectl get all -n final

# Check ConfigMap
kubectl get configmap -n final

# Check Secrets
kubectl get secrets -n final

# Check PVC
kubectl get pvc -n final

# Check Services
kubectl get services -n final

# Get LoadBalancer URL
kubectl get service flask-service -n final -o wide
```

### Option 3: GitOps Deployment with Flux

#### Install Flux

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux
flux bootstrap github \
  --owner=YOUR_USERNAME \
  --repository=clo835_project \
  --branch=main \
  --path=./flux \
  --personal

# Apply Flux resources
kubectl apply -f flux/gotk-sync.yaml
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

### Resource Monitoring

```bash
# Check resource usage
kubectl top pods -n final
kubectl top nodes

# Check resource limits
kubectl describe pods -n final | grep -A 10 "Limits:"
```

## 🔄 GitOps with Flux

### Flux Commands

```bash
# Check Flux status
flux get all

# Check GitRepository
flux get sources git

# Check Kustomization
flux get kustomizations

# Check Flux logs
flux logs

# Reconcile manually
flux reconcile source git clo835-final-project
flux reconcile kustomization clo835-final-project
```

### Update Application via GitOps

```bash
# Make changes to your manifests
vim k8s/configmap.yaml

# Commit and push
git add .
git commit -m "Update background image URL"
git push origin main

# Flux will automatically detect and apply changes
flux get kustomizations
```

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. EKS Cluster Creation Fails (IAM Permission Issues)

**Problem**: `eksctl create cluster` fails with IAM permission errors

**Solution**: Use the provided `eks-config.yaml` file that uses existing IAM roles:

```bash
# Use the working configuration
eksctl create cluster -f eks-config.yaml

# Alternative: Create cluster via AWS Console
# Go to EKS Console → Create cluster → Follow the wizard
```

**Why this works**: The `eks-config.yaml` uses existing `LabRole` instead of trying to create new IAM roles.

#### 2. Pod Stuck in Pending

```bash
# Check pod events
kubectl describe pod <pod-name> -n final

# Check node resources
kubectl describe nodes

# Check if there are enough resources
kubectl get nodes -o custom-columns="NAME:.metadata.name,CPU:.status.capacity.cpu,MEMORY:.status.capacity.memory"
```

#### 2. Image Pull Errors

```bash
# Check if image exists in ECR
aws ecr describe-images --repository-name clo835-final-project --region us-east-1

# Check pod events for image pull errors
kubectl describe pod <pod-name> -n final | grep -A 10 "Events:"

# Verify ECR login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

#### 3. Database Connection Issues

```bash
# Check MySQL pod status
kubectl get pods -n final -l app=mysql

# Check MySQL logs
kubectl logs deployment/mysql -n final

# Test database connectivity
kubectl exec -it deployment/mysql -n final -- mysql -u root -p -e "SHOW DATABASES;"

# Check service connectivity
kubectl exec -it deployment/flask-app -n final -- nc -zv mysql-service 3306
```

#### 4. S3 Access Issues

```bash
# Check IAM role
aws iam get-role --role-name CLO835-S3-Access-Role

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

#### 5. LoadBalancer Issues

```bash
# Check LoadBalancer status
kubectl get service flask-service -n final

# Check if LoadBalancer has external IP
kubectl describe service flask-service -n final

# Check security groups
aws ec2 describe-security-groups --filters "Name=group-name,Values=*eks*"
```

#### 6. HPA Not Working

```bash
# Check if metrics server is installed
kubectl get deployment metrics-server -n kube-system

# Install metrics server if missing
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Check HPA status
kubectl describe hpa flask-app-hpa -n final

# Check if pods have resource requests/limits
kubectl get pod <pod-name> -n final -o yaml | grep -A 10 "resources:"
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

### Option 1: Automated Cleanup

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/ --ignore-not-found=true
kubectl delete namespace final --ignore-not-found=true

# Delete EKS cluster
eksctl delete cluster --name clo835-cluster --region us-east-1

# Delete ECR repository
aws ecr delete-repository --repository-name clo835-final-project --force --region us-east-1

# Delete S3 bucket
aws s3 rb s3://your-clo835-background-images --force

# Delete IAM role
aws iam detach-role-policy --role-name CLO835-S3-Access-Role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam delete-role --role-name CLO835-S3-Access-Role
```

### Option 2: Manual Cleanup (Alternative)

```bash
# Delete Kubernetes resources
kubectl delete -f k8s/ --ignore-not-found=true
kubectl delete namespace final --ignore-not-found=true

# Delete EKS cluster
eksctl delete cluster --name clo835-cluster --region us-east-1

# Delete ECR repository
aws ecr delete-repository --repository-name clo835-final-project --force --region us-east-1

# Delete S3 bucket
aws s3 rb s3://your-clo835-background-images --force

# Delete IAM role
aws iam detach-role-policy --role-name CLO835-S3-Access-Role --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
aws iam delete-role --role-name CLO835-S3-Access-Role
```

### Verify Cleanup

```bash
# Check if cluster is deleted
eksctl get cluster --region us-east-1

# Check if ECR repository is deleted
aws ecr describe-repositories --region us-east-1

# Check if S3 bucket is deleted
aws s3 ls s3://your-clo835-background-images
```

## 📚 Reference

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
aws s3 ls s3://your-clo835-background-images/
aws s3 cp local-file.jpg s3://your-clo835-background-images/

# IAM
aws iam get-role --role-name CLO835-S3-Access-Role
aws iam list-attached-role-policies --role-name CLO835-S3-Access-Role
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
BACKGROUND_IMAGE_URL=https://your-s3-bucket.s3.amazonaws.com/background.jpg
MY_NAME=Your Name (CLO835 Student)
```

#### Important URLs

- **Application**: http://LOADBALANCER_URL
- **ECR Repository**: https://console.aws.amazon.com/ecr/repositories/clo835-final-project
- **EKS Cluster**: https://console.aws.amazon.com/eks/clusters/clo835-cluster
- **S3 Bucket**: https://console.aws.amazon.com/s3/buckets/your-clo835-background-images

### Performance Tuning

#### Resource Optimization

```yaml
# In k8s/flask-deployment.yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

#### HPA Configuration

```yaml
# In k8s/hpa.yaml
spec:
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## 🎓 Assignment Submission Checklist

Before submitting your assignment, ensure you have:

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
  - [ ] Flux GitOps deployed (optional)
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
- [Flux Documentation](https://fluxcd.io/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

## 📄 License

This project is created for educational purposes as part of the CLO835 course at Seneca College.

---

**🎉 Congratulations! You now have a complete, production-ready containerized application deployed on Amazon EKS with full CI/CD pipeline and GitOps capabilities!**
