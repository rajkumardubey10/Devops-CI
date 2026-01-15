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
## PR Validation Pipeline (Pull Request Checks) :

The following screenshot shows the **PR validation pipeline execution** triggered automatically when a pull request is raised.
## Screenshot of PR Request open 
<img width="1351" height="1716" alt="github com_rajkumardubey10_Devops-CI_pull_9" src="https://github.com/user-attachments/assets/cc50ba04-10c3-410f-842f-33bc04ded7b6" />

## Stage view of PR-Validation pipeline 
<img width="1351" height="802" alt="github com_rajkumardubey10_Devops-CI_actions_workflows_ci-pipeline yml" src="https://github.com/user-attachments/assets/83b05f3d-48be-4763-b2bb-6e851dfd5982" />

### What this stage validates

- The pipeline is triggered on **pull request creation or update**.
- It runs **before merge**, ensuring changes are validated early.
- No deployment-related actions are performed at this stage.

The PR validation pipeline includes:

- Source code checkout
- Static checks (syntax / linting)
- Secret scanning
- Dependency or vulnerability checks
- Validation steps required before approval

All checks must pass successfully before the pull request can be approved and merged into the main branch.

This stage ensures that only **verified and reviewed changes** proceed to the merge pipeline, reducing the risk of failures during deployment.

## 🚀 Merge CI Pipeline (Post-Merge Validation) :

<img width="1351" height="1169" alt="github com_rajkumardubey10_Devops-CI_actions_runs_20775615274" src="https://github.com/user-attachments/assets/07bb5b88-6d03-47f7-a2fc-9ede389a51fe" />



This screenshot shows the successful execution of the Merge CI pipeline triggered after the pull request
was merged into the `main` branch. The pipeline runs automatically on every push to the main branch
and performs post-merge validations and build steps required for deployment readiness.

The pipeline includes a **SonarQube quality scan** to enforce **code quality gates**, a **Docker build and push**
step to create the application container image, a **Trivy image vulnerability scan** to ensure container security, and a step to securely access the CD repository for deployment-related updates.

All stages completed successfully, confirming that the merged code meets quality standards, the
container image is built and scanned without critical vulnerabilities, and the application is
ready for the continuous delivery process.

## 🖼️ Deploy Key for CD Repository Access :
<img width="1351" height="879" alt="github com_rajkumardubey10_CD-repo-for-Gitops_blob_main_K8_deployment yml (1)" src="https://github.com/user-attachments/assets/f5b5b330-0ccb-407c-9afb-7b02e0911882" />

This screenshot shows a **Deploy Key configured in the CD (GitOps) repository**.

### What this does:
- A deploy key is added to the **CD repository** with **read/write access**
- It allows the **CI pipeline** to securely access the CD repository
- The CI pipeline uses this access to **update `deployment.yml` files** (for example, updating Docker image tags)
- This enables **automated GitOps-style deployments** without using personal credentials

### Why deploy keys are used:
- Limited to a **single repository**
- More secure than using personal access tokens
- Ideal for **CI → CD repository communication**
- Commonly used in production GitOps workflows

---
## 🖼️ SSH Key for GitHub Authentication (Push & Pull Access)

<img width="1351" height="1229" alt="github com_rajkumardubey10_CD-repo-for-Gitops_blob_main_K8_deployment yml (2)" src="https://github.com/user-attachments/assets/c33e4434-2a88-4c61-b1c3-76e029dddc78" />


This screenshot shows an **SSH key added to the GitHub user account**.

### What this does:
- Enables **passwordless authentication** with GitHub
- Allows seamless **git pull** and **git push** operations
- Eliminates repeated username and password prompts required by HTTPS authentication

### Why SSH is preferred over HTTPS:
- HTTPS requires entering username and password (or token) repeatedly
- SSH provides **secure, persistent authentication**
- Essential for automation and CI/CD pipelines
- Industry-standard approach in professional DevOps environments

---

## 🔄 How CI and CD Repositories Work Together

1. Code is merged into the `main` branch
2. The **Merge CI pipeline** builds and scans the Docker image
3. CI pipeline uses the **deploy key** to access the CD repository
4. The pipeline updates Kubernetes `deployment.yml` with the new image tag
5. GitOps tools (e.g., Argo CD) detect the change and deploy automatically

---

## 🎯 Key Takeaway

By separating **CI and CD repositories** and using **SSH keys and deploy keys**, this setup:
- Improves security
- Avoids credential leakage
- Enables clean GitOps workflows
- Matches real-world enterprise DevOps practices


