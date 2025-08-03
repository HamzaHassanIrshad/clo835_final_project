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

## 🎤 **Key Concepts to Highlight**

### **Architecture & Design Decisions:**

- **Microservices Architecture**: Flask app and MySQL are separate containers for scalability
- **Cloud-Native Design**: Using managed AWS services (EKS, ECR, S3, EBS) for reliability
- **Security Best Practices**: Private S3 bucket, IRSA for secure access, Secrets for sensitive data
- **High Availability**: LoadBalancer for external access, HPA for auto-scaling
- **Data Persistence**: EBS volumes ensure data survives pod restarts

### **Technical Concepts:**

- **Container Orchestration**: Kubernetes manages container lifecycle and networking
- **Service Mesh**: Services provide stable endpoints for inter-pod communication
- **Configuration Management**: ConfigMaps separate configuration from code
- **Secret Management**: Kubernetes Secrets encrypt sensitive data
- **Storage Classes**: gp2 StorageClass automatically provisions EBS volumes
- **Horizontal Pod Autoscaler**: Scales based on CPU/memory metrics

### **Business Value:**

- **Scalability**: Application can handle varying loads automatically
- **Reliability**: Self-healing pods and persistent storage
- **Maintainability**: CI/CD pipeline automates deployments
- **Cost Optimization**: Auto-scaling prevents over-provisioning
- **Developer Experience**: GitOps workflow for easy deployments

---

## 🚀 Demo Script - Step by Step

### **Prerequisites Check**

**Duration: 1 minute**

**Demo Flow:**
_"Let me first verify that our environment is properly configured for the demonstration."_

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

**What to Show:**

- ✅ All tools installed and working
- ✅ AWS credentials valid
- ✅ EKS cluster accessible

---

### **1. Application Functionality (Local Docker Testing)**

**Duration: 3 minutes**

**Demo Flow:**
_"We'll start by validating our application in a local Docker environment to ensure everything works before deploying to Kubernetes."_

```bash
# Build the Docker image locally
docker build -t clo835-app .

# Run the container locally
docker run -p 81:81 clo835-app

# Test the application (in another terminal)
curl http://localhost:81

# Test all application endpoints
curl http://localhost:81/addemp
curl http://localhost:81/getemp
curl http://localhost:81/about

# Show application logs
docker logs $(docker ps -q --filter ancestor=clo835-app)
```

**What to Show:**

- ✅ Docker image builds successfully
- ✅ Container runs without errors
- ✅ Application responds to HTTP requests on port 81
- ✅ All endpoints work correctly
- ✅ Background image loads from S3
- ✅ Application logs show S3 download
- ✅ Basic CRUD functionality works locally

**Key Points:**

- Application listens on port 81 as required
- Background image URL comes from environment variable
- MySQL credentials come from environment variables
- Your name appears in the header from ConfigMap

**Technical Notes:**
_This local testing validates our containerization strategy and ensures the application can access external resources like S3 before deployment._

---

### **2. GitHub Actions CI/CD Pipeline**

**Duration: 2 minutes**

**Demo Flow:**
_"Now let's examine our CI/CD pipeline that automates the build and deployment process."_

```bash
# Show the CI/CD workflow
cat .github/workflows/deploy.yml

# Check recent workflow runs
# Navigate to: https://github.com/CLO835FinalTermProject/clo835_project/actions

# Show ECR repository
aws ecr describe-repositories --region us-east-1

# Show recent images in ECR
aws ecr describe-images --repository-name clo835-final-project --region us-east-1
```

**What to Show:**

- ✅ GitHub Actions workflow configuration
- ✅ Recent successful builds
- ✅ Docker images pushed to ECR
- ✅ Automated testing and deployment
- ✅ ECR repository with tagged images

**Technical Notes:**
_Our CI/CD pipeline implements GitOps principles, automatically building and testing code changes before deployment to ensure quality and consistency._

---

### **3. EKS Deployment (Empty Namespace)**

**Duration: 4 minutes**

**Demo Flow:**
_"We'll now deploy our application to Amazon EKS, starting with a completely empty namespace to demonstrate our infrastructure-as-code approach."_

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

# Show all resources created
kubectl get all,pvc,configmap,secret,serviceaccount -n final
```

**What to Show:**

- ✅ EKS cluster with 2 worker nodes
- ✅ Empty namespace before deployment
- ✅ All resources deployed successfully
- ✅ Pods starting up and becoming ready
- ✅ Services and LoadBalancer created
- ✅ PVC bound to EBS volume
- ✅ ConfigMap and Secrets properly configured

**Technical Notes:**
_This deployment demonstrates Kubernetes' declarative approach where we describe the desired state and Kubernetes makes it happen, with proper resource isolation and management._

---

### **4. S3 Background Image Loading**

**Duration: 2 minutes**

**Demo Flow:**
_"Let's verify that our application can access the private S3 bucket to load the background image using our security implementation."_

```bash
# Check S3 bucket contents
aws s3 ls s3://clo835-final-project-bucket-g5/

# Check application logs for S3 download
kubectl logs deployment/flask-app -n final

# Verify ConfigMap has correct S3 URL
kubectl get configmap app-config -n final -o yaml

# Get LoadBalancer URL
kubectl get svc flask-service -n final

# Test application access
LOADBALANCER_URL=$(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl http://$LOADBALANCER_URL

# Show application logs with S3 download
kubectl logs deployment/flask-app -n final | grep -i s3
```

**What to Show:**

- ✅ S3 bucket contains background images
- ✅ Application logs show successful S3 download
- ✅ ConfigMap contains correct S3 URL
- ✅ LoadBalancer URL accessible
- ✅ Background image loads in browser
- ✅ Private S3 bucket access working

**Technical Notes:**
_The S3 integration uses IRSA for secure access without hardcoded credentials, providing temporary, scoped permissions that automatically rotate._

---

### **5. Data Persistence Test (EBS Volume Verification)**

**Duration: 3 minutes**

**Demo Flow:**
_"Now we'll demonstrate data persistence by adding data through our web interface, then simulating a pod failure to show that our data survives."_

```bash
# First, add some data through the web interface
# Navigate to the LoadBalancer URL and add an employee record

# Show current PVC and PV status
kubectl get pvc -n final
kubectl get pv

# Show EBS volume details
kubectl describe pvc mysql-pvc -n final

# Then delete the MySQL pod to test persistence
kubectl delete pod -l app=mysql -n final

# Watch the new pod start
kubectl get pods -n final -w

# Show PVC still bound after pod deletion
kubectl get pvc -n final

# Wait for new pod to be ready, then verify data persists
# Go back to web interface and retrieve the employee data you added

# Show EBS volume remains attached
kubectl describe pvc mysql-pvc -n final
```

**What to Show:**

- ✅ Data added through web interface
- ✅ PVC bound to EBS volume
- ✅ MySQL pod deleted and recreated
- ✅ New pod starts successfully
- ✅ Data persists after pod recreation
- ✅ PVC maintains data across pod restarts
- ✅ EBS volume dynamically created and attached

**Key Points:**

- EBS volume created automatically by gp2 StorageClass
- PVC size: 2Gi as specified
- AccessMode: ReadWriteOnce as required
- Data persists across pod restarts

**Technical Notes:**
_This persistence test validates our storage architecture where the gp2 StorageClass automatically provisions EBS volumes that survive pod restarts._

---

### **6. Internet Access Verification**

**Duration: 2 minutes**

**Demo Flow:**
_"Let's verify that our application is accessible from the internet through our LoadBalancer configuration."_

```bash
# Get the LoadBalancer URL
LOADBALANCER_URL=$(kubectl get svc flask-service -n final -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
echo "Application URL: http://$LOADBALANCER_URL"

# Test from external network
curl http://$LOADBALANCER_URL

# Show LoadBalancer details
kubectl describe service flask-service -n final

# Test all endpoints from external access
curl http://$LOADBALANCER_URL/addemp
curl http://$LOADBALANCER_URL/getemp
curl http://$LOADBALANCER_URL/about
```

**What to Show:**

- ✅ LoadBalancer has external IP/hostname
- ✅ Application responds to external requests
- ✅ Internet users can access the application
- ✅ LoadBalancer service configuration
- ✅ All endpoints accessible from internet

**Technical Notes:**
_The LoadBalancer service type creates an AWS Application Load Balancer that provides a stable external endpoint with automatic traffic distribution and health checking._

---

### **7. ConfigMap Background Image Change**

**Duration: 3 minutes**

**Demo Flow:**
_"We'll now demonstrate dynamic configuration management by updating our background image through ConfigMap changes."_

```bash
# Upload a new background image to S3
aws s3 cp background-new.svg s3://clo835-final-project-bucket-g5/background-new.svg

# Update ConfigMap with new image URL
kubectl apply -f k8s/configmap.yaml

# Restart the deployment to pick up changes
kubectl rollout restart deployment/flask-app -n final

# Check the logs for new image download
kubectl logs deployment/flask-app -n final

# Verify the change
kubectl get configmap app-config -n final -o yaml

# Show new background image in browser
# Navigate to LoadBalancer URL and refresh
```

**What to Show:**

- ✅ New image uploaded to S3
- ✅ ConfigMap updated successfully
- ✅ Deployment restarted
- ✅ Application logs show new image download
- ✅ Browser shows new background image
- ✅ Dynamic configuration change working

**Technical Notes:**
_This demonstrates Kubernetes ConfigMaps' ability to change application behavior without rebuilding containers, enabling rapid updates and configuration management._

---

### **8. HPA Auto-scaling (Bonus Feature)**

**Duration: 3 minutes**

**Demo Flow:**
_"Let's demonstrate auto-scaling by generating load on our application and watching Kubernetes automatically scale up additional pods."_

```bash
# Install load testing tool
curl -s https://hey-release.s3.us-east-2.amazonaws.com/hey_linux_amd64 -o hey
chmod +x hey

# Check current pod count
kubectl get pods -n final

# Check HPA status
kubectl get hpa -n final
kubectl describe hpa flask-app-hpa -n final

# Run load test to trigger auto-scaling
./hey -n 2000 -c 50 http://$LOADBALANCER_URL

# In another terminal, watch pods scaling
kubectl get pods -n final -w

# Check HPA status after load test
kubectl get hpa -n final

# Check CPU metrics
kubectl top pods -n final

# Show HPA events
kubectl describe hpa flask-app-hpa -n final
```

**What to Show:**

- ✅ Initial pod count (1 pod)
- ✅ HPA configuration and thresholds
- ✅ Load test generating traffic
- ✅ Pods scaling up (1 → 6+ pods)
- ✅ HPA metrics showing CPU utilization
- ✅ Auto-scaling working correctly
- ✅ Metrics server providing data

**Technical Notes:**
_The Horizontal Pod Autoscaler automatically manages application capacity based on CPU usage, providing both performance optimization and cost efficiency._

---

### **9. CI/CD Automation (Bonus Feature)**

**Duration: 2 minutes**

**Demo Flow:**
_"Finally, let's demonstrate our complete CI/CD automation by making a code change and watching the pipeline automatically deploy it."_

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

# Show the new image being deployed
kubectl get pods -n final
```

**What to Show:**

- ✅ Code changes committed
- ✅ GitHub Actions workflow triggered
- ✅ Automated build and test
- ✅ New Docker image pushed to ECR
- ✅ CI/CD pipeline working end-to-end
- ✅ Application automatically updated

**Technical Notes:**
_This demonstrates complete automation from code commit to production deployment, reducing deployment time and eliminating manual errors._

---

## 🔧 Enhanced Troubleshooting Section

### **Common Issues and Solutions**

```bash
# If pods are stuck in Pending
kubectl describe pod <pod-name> -n final
kubectl get events -n final --sort-by='.lastTimestamp'

# If S3 access fails
kubectl logs deployment/flask-app -n final | grep -i s3
kubectl describe serviceaccount clo835 -n final

# If database connection fails
kubectl logs deployment/flask-app -n final | grep -i mysql
kubectl get secret mysql-secret -n final -o yaml

# If LoadBalancer is not ready
kubectl describe service flask-service -n final
kubectl get events -n final | grep LoadBalancer

# If HPA is not working
kubectl get hpa -n final
kubectl describe hpa flask-app-hpa -n final
kubectl top pods -n final
```

---

## 📊 Demo Summary

### **Total Demo Time: ~20 minutes**

### **Key Features Demonstrated:**

1. **✅ Local Development**: Docker containerization and testing on port 81
2. **✅ CI/CD Pipeline**: Automated build, test, and deployment
3. **✅ Kubernetes Deployment**: Complete EKS deployment in "final" namespace
4. **✅ Cloud Integration**: Private S3 bucket, ECR, LoadBalancer
5. **✅ Data Persistence**: PVC (2Gi, ReadWriteOnce) and EBS volume persistence
6. **✅ Internet Access**: LoadBalancer service with stable endpoint
7. **✅ Dynamic Configuration**: ConfigMap updates with background image changes
8. **✅ Auto-scaling**: HPA under load with metrics server
9. **✅ GitOps**: Automated deployment from Git changes

### **Technical Stack Showcased:**

- **Containerization**: Docker
- **Orchestration**: Kubernetes (EKS with 2 worker nodes)
- **CI/CD**: GitHub Actions
- **Container Registry**: Amazon ECR
- **Storage**: Amazon S3 (private), EBS (gp2 StorageClass)
- **Load Balancing**: AWS LoadBalancer
- **Auto-scaling**: Kubernetes HPA with metrics server
- **Configuration**: ConfigMaps and Secrets
- **Service Accounts**: IRSA for S3 access

---

## 🎯 Demo Tips

### **Before the Demo:**

- ✅ Ensure all tools are installed and working
- ✅ Verify AWS credentials are valid
- ✅ Test all commands beforehand
- ✅ Have backup plans for any potential issues
- ✅ Prepare the background-new.svg file for S3 upload

### **During the Demo:**

- ✅ Speak clearly and explain each step
- ✅ Show both terminal output and browser results
- ✅ Highlight key technical concepts
- ✅ Demonstrate real-time changes
- ✅ Keep audience engaged with explanations
- ✅ Show the "final" namespace creation
- ✅ Demonstrate port 81 configuration

### **After the Demo:**

- ✅ Show the working application
- ✅ Highlight the production-ready nature
- ✅ Discuss scalability and reliability features
- ✅ Answer questions about the implementation

---

## 🏆 Success Criteria

The demo is successful when you can demonstrate:

- ✅ **All 9 requirements** from the assignment
- ✅ **Working application** with all features on port 81
- ✅ **Production-ready deployment** on EKS with 2 worker nodes
- ✅ **Auto-scaling** under load with HPA
- ✅ **Dynamic configuration** changes via ConfigMap
- ✅ **Complete CI/CD pipeline** with GitHub Actions
- ✅ **Data persistence** across pod restarts with EBS
- ✅ **Internet accessibility** via LoadBalancer
- ✅ **Private S3 bucket** access with background images
- ✅ **IRSA** for secure S3 access

---

**🎉 Congratulations! Your CLO835 Final Project demonstrates advanced cloud-native development skills and is ready for presentation!**
