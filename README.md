# Project Title :
### Controlled CI/CD Pipeline with PR Governance, Security Validation, and Argo CD-Based Kubernetes Delivery

# One-Line Summary :
### Implemented a PR-driven, security-gated GitOps CI/CD pipeline where container images are conditionally built, vulnerability-scanned, and promoted to Kubernetes only after approval.

# Business Problem :

# Solution Overview :
- PR-based governance for all code changes
- Separate CI and CD repositories
- Automated Docker image build and registry push
- Mandatory image vulnerability scanning using Trivy
- Controlled manifest updates using yq
- GitOps-based deployment using Argo CD
- Kubernetes as the execution platform

# Architecture Overview :
## 🏗 Architecture Overview

<img width="1000" height="11000" alt="" src="https://github.com/user-attachments/assets/dc31ea68-b008-4c06-be21-fd003a28eec9" />


