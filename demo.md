# 🎬 CLO835 Final Project - Demo Guide

> **Complete Demo Script for Containerized Flask Application with MySQL on Amazon EKS**

## 📋 Demo Overview

This demo showcases a complete cloud-native application stack with:

- **Containerized Flask Application** with dynamic background images
- **MySQL Database** with persistent storage
- **Automated CI/CD Pipeline** with GitHub Actions
- **Kubernetes Deployment** on Amazon EKS
- **Auto-scaling** with Horizontal Pod Autoscaler (HPA)
- **Dynamic Configuration** via ConfigMaps

## 🎯 Demo Requirements Checklist

The recording should clearly demonstrate:

1. ✅ **Application functionality verified locally using Docker images**
2. ✅ **Application image created automatically and pushed to Amazon ECR using GitHub Actions**
3. ✅ **Application deployed into empty namespace "final" in Amazon EKS**
4. ✅ **Application loading background image from private Amazon S3**
5. ✅ **Data persisted when pod is deleted and re-created by replicaset**
6. ✅ **Internet users can access the application**
7. ✅ **Background image URL changed in ConfigMap and visible in browser**
8. ✅ **Auto-scaling functionality demonstrated as response to application load**
9. ✅ **Deployment automation demonstrated as response to application changes**

---

## 🚀 Demo Script - Step by Step

### **Prerequisites Check**

```bash
# Verify tools are installed
eksctl version
kubectl version --client
aws --version

# Verify AWS credentials
aws sts get-caller-identity

# Verify cluster access
kubectl get nodes
```

---

### **1. Application Functionality (Local Docker Testing)**

**Duration: 2 minutes**

```bash
# Build the Docker image locally
docker build -t clo835-app .

# Run the container locally
docker run -p 81:81 clo835-app

# Test the application (in another terminal)
curl http://localhost:81
```

**What to Show:**

- ✅ Docker image builds successfully
- ✅ Container runs without errors
- ✅ Application responds to HTTP requests
- ✅ Basic functionality works locally

---

### **2. GitHub Actions CI/CD Pipeline**

**Duration: 1 minute**

```bash
# Show the CI/CD workflow
cat .github/workflows/deploy.yml

# Check recent workflow runs
# Navigate to: https://github.com/CLO835FinalTermProject/clo835_project/actions
```

**What to Show:**

- ✅ GitHub Actions workflow configuration
- ✅ Recent successful builds
- ✅ Docker images pushed to ECR
- ✅ Automated testing and deployment

---

### **3. EKS Deployment (Empty Namespace)**

**Duration: 3 minutes**

```bash
# Show current cluster status
kubectl get nodes

# Show empty namespace
kubectl get all -n final

# Deploy all resources to empty namespace
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

# Watch deployment progress
kubectl get pods -n final -w
```

**What to Show:**

- ✅ EKS cluster with worker nodes
- ✅ Empty namespace before deployment
- ✅ All resources deployed successfully
- ✅ Pods starting up and becoming ready
- ✅ Services and LoadBalancer created

---

### **4. S3 Background Image Loading**

**Duration: 1 minute**

```bash
# Check S3 bucket contents
aws s3 ls s3://clo835-background-images/

# Check application logs for S3 download
kubectl logs deployment/flask-app -n final

# Get LoadBalancer URL
kubectl get svc flask-service -n final

# Test application access
LOADBALANCER_URL=$(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl http://$LOADBALANCER_URL
```

**What to Show:**

- ✅ S3 bucket contains background images
- ✅ Application logs show successful S3 download
- ✅ LoadBalancer URL accessible
- ✅ Background image loads in browser

---

### **5. Data Persistence Test**

**Duration: 2 minutes**

```bash
# First, add some data through the web interface
# Navigate to the LoadBalancer URL and add an employee record

# Then delete the MySQL pod to test persistence
kubectl delete pod -l app=mysql -n final

# Watch the new pod start
kubectl get pods -n final -w

# Wait for new pod to be ready, then verify data persists
# Go back to web interface and retrieve the employee data you added
```

**What to Show:**

- ✅ Data added through web interface
- ✅ MySQL pod deleted and recreated
- ✅ New pod starts successfully
- ✅ Data persists after pod recreation
- ✅ PVC maintains data across pod restarts

---

### **6. Internet Access Verification**

**Duration: 1 minute**

```bash
# Get the LoadBalancer URL
LOADBALANCER_URL=$(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Application URL: http://$LOADBALANCER_URL"

# Test from external network
curl http://$LOADBALANCER_URL

# Show LoadBalancer details
kubectl describe service flask-service -n final
```

**What to Show:**

- ✅ LoadBalancer has external IP/hostname
- ✅ Application responds to external requests
- ✅ Internet users can access the application
- ✅ LoadBalancer service configuration

---

### **7. ConfigMap Background Image Change**

**Duration: 2 minutes**

```bash
# Upload a new background image to S3
aws s3 cp background-new.svg s3://clo835-background-images/background-new.svg --acl public-read

# Update ConfigMap with new image URL
kubectl patch configmap app-config -n final -p '{"data":{"BACKGROUND_IMAGE_URL":"https://clo835-background-images.s3.us-east-1.amazonaws.com/background-new.svg"}}'

# Restart the deployment to pick up changes
kubectl rollout restart deployment/flask-app -n final

# Check the logs for new image download
kubectl logs deployment/flask-app -n final

# Verify the change
kubectl get configmap app-config -n final -o yaml
```

**What to Show:**

- ✅ New image uploaded to S3
- ✅ ConfigMap updated successfully
- ✅ Deployment restarted
- ✅ Application logs show new image download
- ✅ Browser shows new background image

---

### **8. HPA Auto-scaling (Bonus Feature)**

**Duration: 2 minutes**

```bash
# Install load testing tool
curl -s https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64 -o hey
chmod +x hey

# Check current pod count
kubectl get pods -n final

# Check HPA status
kubectl get hpa -n final

# Run load test to trigger auto-scaling
./hey -n 2000 -c 50 http://$LOADBALANCER_URL

# In another terminal, watch pods scaling
kubectl get pods -n final -w

# Check HPA status after load test
kubectl get hpa -n final

# Check CPU metrics
kubectl top pods -n final
```

**What to Show:**

- ✅ Initial pod count (1 pod)
- ✅ HPA configuration
- ✅ Load test generating traffic
- ✅ Pods scaling up (1 → 6+ pods)
- ✅ HPA metrics showing CPU utilization
- ✅ Auto-scaling working correctly

---

### **9. CI/CD Automation (Bonus Feature)**

**Duration: 1 minute**

```bash
# Make a small change to demonstrate CI/CD
# Edit any file (e.g., add a comment to app.py)

# Commit and push changes
git add .
git commit -m "Demo: Test CI/CD automation"
git push origin dev-hamza

# Show GitHub Actions running
# Navigate to: https://github.com/CLO835FinalTermProject/clo835_project/actions

# Check ECR for new image
aws ecr describe-images --repository-name clo835-final-project --region us-east-1
```

**What to Show:**

- ✅ Code changes committed
- ✅ GitHub Actions workflow triggered
- ✅ Automated build and test
- ✅ New Docker image pushed to ECR
- ✅ CI/CD pipeline working end-to-end

---

## 📊 Demo Summary

### **Total Demo Time: ~15 minutes**

### **Key Features Demonstrated:**

1. **✅ Local Development**: Docker containerization and testing
2. **✅ CI/CD Pipeline**: Automated build, test, and deployment
3. **✅ Kubernetes Deployment**: Complete EKS deployment
4. **✅ Cloud Integration**: S3, ECR, LoadBalancer
5. **✅ Data Persistence**: PVC and database persistence
6. **✅ Internet Access**: LoadBalancer service
7. **✅ Dynamic Configuration**: ConfigMap updates
8. **✅ Auto-scaling**: HPA under load
9. **✅ GitOps**: Automated deployment from Git

### **Technical Stack Showcased:**

- **Containerization**: Docker
- **Orchestration**: Kubernetes (EKS)
- **CI/CD**: GitHub Actions
- **Container Registry**: Amazon ECR
- **Storage**: Amazon S3, EBS
- **Load Balancing**: AWS LoadBalancer
- **Auto-scaling**: Kubernetes HPA
- **Configuration**: ConfigMaps and Secrets

---

## 🎯 Demo Tips

### **Before the Demo:**

- ✅ Ensure all tools are installed and working
- ✅ Verify AWS credentials are valid
- ✅ Test all commands beforehand
- ✅ Have backup plans for any potential issues

### **During the Demo:**

- ✅ Speak clearly and explain each step
- ✅ Show both terminal output and browser results
- ✅ Highlight key technical concepts
- ✅ Demonstrate real-time changes
- ✅ Keep audience engaged with explanations

### **After the Demo:**

- ✅ Show the working application
- ✅ Highlight the production-ready nature
- ✅ Discuss scalability and reliability features
- ✅ Answer questions about the implementation

---

## 🏆 Success Criteria

The demo is successful when you can demonstrate:

- ✅ **All 9 requirements** from the assignment
- ✅ **Working application** with all features
- ✅ **Production-ready deployment** on EKS
- ✅ **Auto-scaling** under load
- ✅ **Dynamic configuration** changes
- ✅ **Complete CI/CD pipeline**
- ✅ **Data persistence** across pod restarts
- ✅ **Internet accessibility** via LoadBalancer

---

**🎉 Congratulations! Your CLO835 Final Project demonstrates advanced cloud-native development skills and is ready for presentation!**
