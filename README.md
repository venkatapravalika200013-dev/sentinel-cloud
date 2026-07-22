# Project Sentinel-Cloud 🛡️
> **Automated FinOps Governance & Infrastructure Cleanup Engine**

Sentinel-Cloud is an automated cloud governance and cost-optimization system. Built with Terraform, Docker, LocalStack, and Python, it simulates a real-world enterprise environment to detect "Shadow IT" and eliminate unallocated cloud waste. The engine scans local AWS resources, identifies non-compliant infrastructure lacking mandatory corporate tags, and automatically terminates them.

---

## 🏗️ Architecture & Tech Stack

- **Infrastructure Emulation**: [LocalStack](https://localstack.cloud/) running in [Docker](https://www.docker.com/)
- **Infrastructure-as-Code (IaC)**: [Terraform](https://www.terraform.io/) (HCL)
- **Automation & FinOps Brain**: [Python 3](https://www.python.org/) with the [Boto3 AWS SDK](https://aws.amazon.com/sdk-for-python/)
- **Cloud CLI**: AWS CLI / `awslocal`

┌────────────────────────────────────────────────────────────────────────┐
│                          LOCAL PC ENVIRONMENT                          │
│                                                                        │
│   ┌────────────────────┐                   ┌───────────────────────┐   │
│   │   Terraform IaC    │───(Provision)────►│ LocalStack Container  │   │
│   └────────────────────┘                   │  (Emulated AWS APIs) │   │
│                                            └───────────┬───────────┘   │
│                                                        │               │
│   ┌────────────────────┐                               │               │
│   │ Python Sentinel    │───(Scan & Remediate)──────────┘               │
│   │   (boto3 Engine)   │                                               │
│   └────────────────────┘                                               │
└────────────────────────────────────────────────────────────────────────┘


---

## 📋 Project Governance Policy

To enforce financial accountability and tracking across cloud infrastructure, **Sentinel-Cloud** enforces a mandatory tagging rule:

- **Compliant Resource**: Must include a tag with `Key="Project"` and `Value="Sentinel-Cloud"`.
- **Non-Compliant Resource**: Missing the `Project` tag or having no tags at all. Flagged as cloud waste and queued for immediate termination.

---

## 📁 Repository Structure

.
├── docker-compose.yml       # LocalStack container orchestration
├── provider.tf              # Terraform AWS provider configuration (Path-style enabled)
├── variables.tf             # Configurable input parameters
├── main.tf                  # Infrastructure provisioning (Compliant & Non-Compliant buckets)
├── outputs.tf               # Exported resource ARNs and endpoints
├── scripts/
│   └── sentinel_brain.py    # Python FinOps engine with Dry-Run & Live execution modes
└── README.md                # Project documentation


---

## 🚀 Quick Start (1-2-3 Execution Workflow)

Follow these steps to spin up the emulated cloud, deploy infrastructure, and execute the automated governance engine.

### Step 1: Spin Up the Local Cloud Environment
Launch LocalStack inside Docker to emulate AWS services locally without incurring actual costs:

```bash
docker-compose up -d
Step 2: Deploy Infrastructure via Terraform
Initialize Terraform and provision both compliant (tagged) and non-compliant (untagged) test resources:

Bash
terraform init
terraform apply -auto-approve
Step 3: Run the Sentinel Governance Engine
A. Run in Safe Mode (Dry-Run)
Scan the environment and view non-compliant resources without making any destructive changes:

Bash
python scripts/sentinel_brain.py
B. Run in Execution Mode (Live Cleanup)
Enforce governance policies and automatically terminate non-compliant infrastructure:

Windows PowerShell:

PowerShell
$env:DRY_RUN="False"; python scripts/sentinel_brain.py
Linux / macOS / Bash:

Bash
export DRY_RUN=False && python scripts/sentinel_brain.py
🛡️ Key Features & Reliability Patterns
Dry-Run Safety Switch: Defaults to DRY_RUN=True to prevent accidental deletion of critical infrastructure during audit scans.

Path-Style Addressing: Configured s3_use_path_style = true to ensure smooth DNS resolution within local Docker network topologies.

100% Verification Handshake: Uses head_bucket post-deletion checks to confirm resources are fully removed from the cloud provider's state before closing execution loops.

Zero-Trust Metadata Inspection: Handles missing tag sets (NoSuchTagSet) gracefully without crashing the scanning process.

🧹 Tear Down
To destroy all local resources and stop the LocalStack environment, run:

Bash
terraform destroy -auto-approve
docker-compose down -v
