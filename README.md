# Project Title :
### Controlled CI/CD Pipeline with PR Governance, Security Validation, and Argo CD-Based Kubernetes Delivery

# One-Line Summary :
### Implemented a PR-driven, security-gated GitOps CI/CD pipeline where container images are conditionally built, vulnerability-scanned, and promoted to Kubernetes only after approval.

# Project Requirements :
#### The client required an automated deployment pipeline for a containerized application running on Kubernetes. The objective was to standardize the deployment process and reduce manual intervention while maintaining control and traceability.
### The requirements provided for the project were:
- Build an automated CI/CD pipeline to handle application build and deployment.
- Ensure application changes are deployed only after code review and approval.
- Integrate the existing GitHub workflow with CI/CD automation.
- Deploy and manage the application in a Kubernetes environment.
- Maintain a consistent and repeatable deployment process across releases.
- Ensure each deployment can be traced back to a specific Git commit and approval.
- Include security validation as part of the deployment process.
- Provide a clear rollback mechanism in case of failed or unstable deployments.
- Follow standard CI/CD practices so the setup can be maintained by the internal team.
- Design the solution in a way that supports future enhancements without major restructuring.

#### The client expected a practical, production-oriented solution that could be operated and maintained by the internal team.

# Solution Overview :
#### To meet the project requirements, a controlled CI/CD pipeline was implemented using a pull-request–driven workflow combined with GitOps-based deployment.
#### The solution separates validation, build, and deployment responsibilities to ensure that only reviewed and approved changes reach the Kubernetes environment.
### Key aspects of the implementation include:
- A PR validation pipeline that runs on pull request creation to validate changes without triggering builds or deployments.
- A merge pipeline that runs only after PR approval and merge, responsible for build, security checks, and promotion.
- Sequential pipeline stages with strict dependency, ensuring the pipeline stops immediately if any stage fails.
- A conditional Docker build strategy, where the pipeline evaluates changes in application source files and the Dockerfile before building an image.
- If no relevant changes are detected, the pipeline continues without building or pushing a Docker image, avoiding unnecessary resource usage.
- When a build is required, the container image is built and pushed to the registry as part of the merge pipeline.
- Image security validation is performed as part of the merge pipeline before promotion.
- Kubernetes manifests are maintained in a separate repository to follow GitOps principles.
- Application deployment is handled by Argo CD based on changes committed to the manifest repository.
- Rollbacks are handled by reverting manifest changes in Git, without manual access to the Kubernetes cluster.

#### This approach ensures controlled deployments, reduces redundant builds, and keeps the deployment process efficient, traceable, and aligned with GitOps practices.

# Architecture Overview :
![Devops CI/CD Project Architecture ](https://github.com/user-attachments/assets/f6de2043-0987-4bf7-8dbb-520cabc6d41c)<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" id="mermaid-svg-2" width="100%" class="flowchart" style="max-width: 100%;" viewBox="-31.160028076171876 -31.160026168823016 685.5206176757813 3613.3029663085936" height="100%">

# Tech Stack :

| Category | Technology |
|--------|------------|
| Version Control | GitHub |
| CI Automation | GitHub Actions |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Security Scanning | Trivy |
| Configuration Management | yq |
| GitOps Deployment | Argo CD |
| Container Orchestration | Kubernetes |

# CI/CD & GitOps Workflow :
```
Developer raises Pull Request  
→ PR validation pipeline runs  
→ PR reviewed and approved  
→ PR merged into main branch  
→ Merge pipeline triggered  
→ Evaluate file changes (source code / Dockerfile)  
→ If relevant changes detected:  
  → Docker image built  
  → Image pushed to Docker Hub  
  → Trivy image vulnerability scan  
  → Security gate evaluation  
  → Image tag updated in CD repository using yq  
  → Commit pushed to CD repository  
→ If no relevant changes detected:  
  → Skip image build, scan, and promotion  
→ Argo CD detects manifest change (if any)  
→ Argo CD syncs desired state  
→ Kubernetes deploys application
```
# Project File-Structure :
```
.
├── .github/workflows/
│   ├── pr-validation.yml
│   └── merge-pipeline.yml
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── docs/
│   ├── security-design.md
│   ├── ci-cd-pipeline.md
│   └── deployment-flow.md
├── screenshots/
│   ├── architecture.png
│   ├── merge-pipeline-success.png
│   ├── trivy-pass.png
│   └── argocd-synced.png
├── Dockerfile
└── README.md
```

