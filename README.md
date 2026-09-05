# Project Title :
### Controlled CI/CD Pipeline with PR Governance, Security Validation, and Argo CD-Based Kubernetes Delivery.

# One-Line Summary :
### Implemented a PR-driven, security-gated GitOps CI/CD pipeline where container images are conditionally built, vulnerability-scanned, and promoted to Kubernetes only after approval.

---

> **Note:** This repository is a self-built demonstration of the architecture and 
> approach delivered for this client engagement. It does not contain the client's 
> actual codebase, credentials, or proprietary configuration — the application code, 
> pipeline logic, and infrastructure shown here were independently rebuilt to 
> demonstrate the solution publicly, since the original client environment cannot 
> be shared for confidentiality reasons.

## TL;DR

* PR validation pipeline enforces code review and security checks before merge
* Merge pipeline conditionally builds, scans, and promotes Docker images
* GitOps-based Kubernetes delivery using Argo CD
* Staging deployment is verified using Kubernetes rollout checks and smoke tests
* Production deployment requires manual approval
* Slack notifications provide CI/CD success and failure visibility
* Full traceability from Git commit → image → manifest → deployment

---

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
- Staging deployments are verified using Kubernetes rollout checks and HTTP smoke tests before production promotion.
- Production deployment is protected by a manual approval gate using GitHub Environments.
- Slack notifications provide visibility into successful and failed CI/CD executions.

#### This approach ensures controlled deployments, reduces redundant builds, and keeps the deployment process efficient, traceable, and aligned with GitOps practices.

# Architecture Overview :
![Devops CI/CD Project Architecture ](https://github.com/user-attachments/assets/f6de2043-0987-4bf7-8dbb-520cabc6d41c)<?xml version="1.0" encoding="UTF-8"?>


--- 

## Challenges & Design Trade-offs

- Conditional Docker builds increased pipeline logic complexity but significantly reduced unnecessary image builds and registry usage.
- Deploy keys limited access scope and improved security but required explicit rotation and access management.
- SonarQube quality gates increased CI execution time but prevented low-quality code from progressing to deployment.
- Staging verification added an additional validation step after GitOps deployment, ensuring the application is actually running and responding before production promotion.
- Manual production approval adds a controlled human checkpoint, preventing automatic promotion of every successful staging deployment.


# Tech Stack :

| Category | Technology |
|--------|------------|
| Version Control | GitHub |
| CI Automation | GitHub Actions |
| Containerization | Docker |
| Container Registry | Docker Hub |
| Code Quality | SonarQube |
| Security Scanning (Secrets) | Gitleaks |
| Security Scanning (Images) | Trivy |
| Configuration Management | yq |
| GitOps Deployment | Argo CD |
| Container Orchestration | Kubernetes |
| Deployment Verification | Kubernetes Rollout + HTTP Smoke Test |
| Deployment Governance | GitHub Environments |
| Notifications | Slack |

# CI/CD & GitOps Workflow :
```
Developer raises Pull Request
→ PR validation pipeline runs
→ PR reviewed and approved
→ PR merged into assessment branch
→ Merge pipeline triggered
→ SonarQube quality gate
→ Evaluate file changes (source code / Dockerfile)
→ If relevant changes detected:
    → Docker image built
    → Image pushed to Docker Hub
    → Trivy image vulnerability scan
    → Image tag updated in CD repository using yq
    → Commit pushed to CD repository
→ If no relevant changes detected:
    → Skip image build, scan, and promotion
→ Argo CD detects manifest change
→ Argo CD syncs desired state
→ Kubernetes deploys application
→ Staging rollout verification
→ Staging smoke test
→ Manual production approval
→ Production deployment
→ Slack notification
```
# Project File-Structure :
```
.
├── .github/
│   └── workflows/
│       ├── pr-validation.yml
│       └── merge-pipeline.yml
├── src/
│   ├── Dockerfile
│   └── app.py
├── tests/
│   ├── unit/
│   └── integration/
├── screenshots/
│   ├── architecture.png
│   ├── PR-validation.png
│   ├── PR-validation-stage-view.png
│   ├── SonarQube-quality-gate.png
│   ├── Docker-build.png
│   ├── Merge-pipeline.png
│   ├── Staging-smoke-test.png
│   ├── Production-approval.png
│   └── Slack-notification.png
├── requirements.txt
├── .gitignore
└── README.md
```
## PR Validation Pipeline (Pull Request Checks) :

The following screenshot shows the **PR validation pipeline execution** triggered automatically when a pull request is raised.
## Screenshot of PR Request open 
<img width="1366" height="768" alt="octa_pr_validation" src="https://github.com/user-attachments/assets/c21220e9-d5a2-4a18-b4e6-9d9d5cd23671" />

## Stage view of PR-Validation pipeline 
<img width="1366" height="768" alt="octa_pipline" src="https://github.com/user-attachments/assets/2d7ec159-908c-4caf-9cc5-57f61e0184f0" />

### What this stage validates

- The pipeline is triggered on **pull request creation or update**.
- It runs **before merge**, ensuring changes are validated early.
- No deployment-related actions are performed at this stage.

The PR validation pipeline includes:

- Source code checkout
- Static checks (syntax / linting)
- Secret scanning
- Security and vulnerability checks
- Validation steps required before approval

All checks must pass successfully before the pull request can be approved and merged into the assessment branch.

This stage ensures that only **verified and reviewed changes** proceed to the merge pipeline, reducing the risk of failures during deployment.

## 🚀 Merge CI Pipeline (Post-Merge Validation) :

<img width="1366" height="768" alt="merge_pipeline" src="https://github.com/user-attachments/assets/8a1f7771-d7b6-4d1c-8ba8-410bb6247118" />

This screenshot shows the successful execution of the Merge CI pipeline triggered after the pull request was merged into the `assessment` branch.

The pipeline performs SonarQube quality validation, Docker image build and push, Trivy image vulnerability scanning, GitOps manifest update, staging deployment verification, staging smoke testing, manual production approval, production deployment, and Slack notification.

All required stages completed successfully, confirming that the application passed CI validation and was successfully promoted through the staging and production deployment flow.

<img width="1366" height="768" alt="docker_build_artifact_and_approval" src="https://github.com/user-attachments/assets/c94fe636-3a72-4bea-957f-08bfe69ecf6d" />


---

## 🔴 SonarQube Quality Gate — FAILED

<img width="1366" height="768" alt="sonarqube-qualitygate-failed" src="https://github.com/user-attachments/assets/4ce38f3d-03d7-4ba7-9c21-a4729f4b8ff1" />

**Description**  
- This GitHub Actions workflow failed during the **SonarQube Quality Gate check**.  
- Although the SonarQube analysis step completed successfully, the Quality Gate evaluation returned a **FAILED status**, causing the pipeline to exit with a non-zero code.

The pipeline is intentionally configured to **fail fast** when code quality, security, or coverage thresholds are not met, ensuring that non-compliant code is blocked before reaching build or deployment stages.

---

## 🟢 SonarQube Quality Gate — PASSED

<img width="1366" height="768" alt="sonarqube-qualitygate-pass" src="https://github.com/user-attachments/assets/c3045823-c727-468d-bc4d-de841a38a5dd" />

**Description**  
- This GitHub Actions workflow successfully passed the **SonarQube Quality Gate**.  
- The analysis met all configured quality, security, and coverage conditions, allowing the pipeline to continue without interruption.
  
A successful Quality Gate validation confirms that the codebase complies with defined standards and is eligible to proceed to subsequent stages such as Docker image build and deployment.

---

## 🔴 Trivy Vulnerability Scan — FAILED

<img width="1366" height="768" alt="trivy-scan-failed" src="https://github.com/user-attachments/assets/87a851c3-2d19-4630-9041-e2fa994d606f" />

**Description**  
- This CI pipeline execution failed during the **Trivy vulnerability scanning stage**, which is configured to run in **fail-safe mode**.  
- The scan detected vulnerabilities that caused the configured security threshold to fail.

As part of secure CI/CD enforcement, the pipeline was automatically stopped to prevent the build and deployment of artifacts containing known security risks.  
This demonstrates proactive **container and dependency security scanning** aligned with DevSecOps best practices.

---

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

1. Code is merged into the `assessment` branch.
2. The Merge CI pipeline builds and scans the Docker image.
3. CI uses the deploy key to securely access the CD repository.
4. The pipeline updates Kubernetes `deployment.yml` with the new image tag.
5. The change is committed and pushed to the CD repository.
6. Argo CD detects the Git change and synchronizes the Kubernetes deployment.
7. The staging deployment is verified using Kubernetes rollout checks and a smoke test.
8. Production deployment requires manual approval.
9. Slack receives the final CI/CD pipeline status.

---

## 🎯 Key Takeaway

By separating CI and CD repositories and using SSH keys and deploy keys, this setup:

* Improves security
* Avoids credential leakage
* Enables clean GitOps workflows
* Validates staging deployments before production promotion
* Provides controlled manual approval for production
* Provides Slack-based deployment visibility
* Matches real-world enterprise DevOps practices

## 🔁 GitOps Image Tag Update & Docker Registry Verification

This section demonstrates the **GitOps workflow** where the CI pipeline updates the application image tag in the
CD repository and the same image is available in the Docker registry, ensuring **consistency between CI, CD, and runtime deployments**.

---

## 🖼️ Kubernetes Deployment Image Tag Update (CD Repository)

<img width="1366" height="768" alt="manifest_image_tag" src="https://github.com/user-attachments/assets/973f9e7f-4945-49a8-a1d8-fa9f140e6f36" />

---
## Docker Registry Tag Verification
<img width="1366" height="768" alt="docker_verfiy_tag" src="https://github.com/user-attachments/assets/19b992bb-b83f-4155-94b2-c00d978ffa04" />


This screenshot shows the `deployment.yml` file in the **CD (GitOps) repository** where the Docker image tag has been
automatically updated by the CI pipeline after a successful merge.

### What this proves:
- The CI pipeline commits a new image tag into the CD repository
- The image tag corresponds to the latest Docker image built during the merge pipeline
- No manual changes are required to update Kubernetes manifests
- Git becomes the **single source of truth** for deployment state

Example:
```yaml
image: rajkumardockerhub/fastapi-app-multistage:c15cd1ba9f733261f0c226ef81f7ef37a52ac10f
```
For CD Part Checkout this Repo Link : https://github.com/rajkumardubey10/CD-repo-for-Gitops.git

---

## 🧪 Staging Deployment & Smoke Test

After the CI pipeline updates the image tag in the CD repository, Argo CD detects the change and synchronizes the application to the staging Kubernetes environment.

The pipeline then verifies the staging deployment before production promotion.

### Staging Verification includes:

* Kubernetes deployment rollout verification
* Verification that the expected image is deployed
* HTTP smoke test against the application
* Health endpoint validation

The smoke test validates:

<img width="1366" height="768" alt="smoke_test_ss" src="https://github.com/user-attachments/assets/8e186a38-bc5d-479b-a324-b3a41c5fe2bd" />


```text
GET /health
Expected response: {"status":"ok"}
```
---

## 🔐 Manual Production Deployment Approval

<img width="1366" height="768" alt="manual_approval" src="https://github.com/user-attachments/assets/1c99d8fe-57cd-4cd8-9fce-10dd4f8e761b" />

Production deployment is protected using a GitHub Environment with manual approval.

After the staging deployment and smoke test succeed, the pipeline pauses and waits for an authorized reviewer to approve the production deployment.

### Production deployment flow

<img width="1366" height="768" alt="approving _deployment " src="https://github.com/user-attachments/assets/c05480b2-a274-4123-84e3-631130dd06e6" />

```text
Staging Deployment
        ↓
Staging Verification
        ↓
Manual Production Approval
        ↓
Production Deployment
```

---

## 📢 Slack CI/CD Notifications

Slack notifications are integrated into the CI/CD pipeline to provide visibility into pipeline execution.

The pipeline sends notifications for both successful and failed executions.

### Notifications provide:

* Pipeline status
* Success or failure indication
* Failed stage information when applicable

Example failure notification:
<img width="1366" height="768" alt="failed_slack_notificaiton" src="https://github.com/user-attachments/assets/ea4d4690-536c-4c23-8ad2-9fb621cf91ac" />

```text
CI/CD Pipeline Failed
Stage: Staging Verification
Status: FAILED
```

Example success notification:
<img width="1366" height="768" alt="successful_run_slack_notification " src="https://github.com/user-attachments/assets/6b6d5524-1834-4efb-adba-6e0b8ab429a2" />

```text
CI/CD Pipeline Success
Stage: None
Status: SUCCESSFUL
```
