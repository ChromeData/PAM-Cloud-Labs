# Upstream Tools and Where They Are Used

Every lab in this set builds on existing open source tooling. This page records
which tool each lab depends on, what it is used for, and under what license, so
the boundary between upstream work and mine is explicit.

Nothing upstream is vendored into these repos. Everything is referenced as a
module, a package, or a documented dependency.

## By tool

| Tool | License | Used in | For what |
|------|---------|---------|----------|
| [cyberark/conjur](https://github.com/cyberark/conjur) | LGPL-3.0 | [01](https://github.com/ChromeData/Conjur-Terraform-AWS), [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan) | the secrets engine and its policy model |
| [cyberark/summon](https://github.com/cyberark/summon) | MIT | [01](https://github.com/ChromeData/Conjur-Terraform-AWS) | injecting secrets into a process environment |
| [terraform-provider-conjur](https://github.com/cyberark/terraform-provider-conjur) | Apache-2.0 | [01](https://github.com/ChromeData/Conjur-Terraform-AWS) | the data source path, kept as a demonstration of its state behaviour |
| [cyberark/SkyArk](https://github.com/cyberark/SkyArk) | MIT | [02](https://github.com/ChromeData/SkyArk-Shadow-Admin-Audit) | shadow admin discovery in AWS and Azure |
| [cyberark/KubiScan](https://github.com/cyberark/KubiScan) | GPL-3.0 | [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan) | live cluster RBAC risk audit |
| [pspete/psPAS](https://github.com/pspete/psPAS) | MIT | [11](https://github.com/ChromeData/psPAS-PAM-Automation) | every CyberArk REST call |
| [cyberark/epv-api-scripts](https://github.com/cyberark/epv-api-scripts) | Apache-2.0 | [11](https://github.com/ChromeData/psPAS-PAM-Automation) | reference for vault automation patterns |
| [ComplianceAsCode/content](https://github.com/ComplianceAsCode/content) | BSD-3-Clause | [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | the STIG and CIS scan content |
| [dev-sec/ansible-collection-hardening](https://github.com/dev-sec/ansible-collection-hardening) | Apache-2.0 | [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | the remediation roles |
| [Azure/Azure-Sentinel](https://github.com/Azure/Azure-Sentinel) | MIT | [04](https://github.com/ChromeData/Sentinel-Privileged-Access) | detection schema and validation conventions |
| [Azure/azure-policy](https://github.com/Azure/azure-policy) | MIT | [10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails) | policy definition structure |
| [Azure Verified Modules](https://github.com/Azure/Azure-Verified-Modules) | MIT | [10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails) | the compliant Key Vault deployment |
| [terraform-aws-modules/secrets-manager](https://github.com/terraform-aws-modules/terraform-aws-secrets-manager) | Apache-2.0 | [05](https://github.com/ChromeData/Secrets-Manager-PAM) | the secret resource |
| [terraform-aws-modules/iam](https://github.com/terraform-aws-modules/terraform-aws-iam) | Apache-2.0 | [06](https://github.com/ChromeData/IAM-Least-Privilege) | assumable role construction |
| [pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform) | MIT | [07](https://github.com/ChromeData/IaC-Security-Gate) | the hook collection the gate is built on |
| [checkov](https://github.com/bridgecrewio/checkov) | Apache-2.0 | [06](https://github.com/ChromeData/IAM-Least-Privilege), [07](https://github.com/ChromeData/IaC-Security-Gate) | IaC misconfiguration scanning |
| [trivy](https://github.com/aquasecurity/trivy) | Apache-2.0 | [07](https://github.com/ChromeData/IaC-Security-Gate) | additional IaC scanning |
| [gitleaks](https://github.com/gitleaks/gitleaks) | MIT | [07](https://github.com/ChromeData/IaC-Security-Gate) | secrets scanning, the gap the gate fills |
| [prowler](https://github.com/prowler-cloud/prowler) | Apache-2.0 | [09](https://github.com/ChromeData/AWS-Multi-Account-Baseline) | auditing the account baseline |
| [AWS SRA examples](https://github.com/aws-samples/aws-security-reference-architecture-examples) | MIT-0 | [09](https://github.com/ChromeData/AWS-Multi-Account-Baseline) | the reference layout the baseline follows |
| [OpenSCAP](https://github.com/OpenSCAP/openscap) | LGPL-2.1 | [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | running the compliance scans |

## What is mine

The upstream tools do the scanning, the vaulting, and the provisioning. What
these repos add is the part in between:

- The environments, including the deliberately vulnerable ones built to be found
  ([02](https://github.com/ChromeData/SkyArk-Shadow-Admin-Audit),
  [07](https://github.com/ChromeData/IaC-Security-Gate),
  [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan)).
- The analysis logic: the SkyArk scorer, the SCAP delta, the RBAC linter, the
  drift reconciler, the policy validator, the Prowler triage roller, the rotation
  handler.
- The tests around that logic, so the numbers these labs report can be trusted
  before any cloud spend.
- The findings, the failures, and the reasoning, recorded in each lab's
  `LAB-NOTES.md`.

## A note on overlap

Several tools appear in more than one lab, and one lab often needs several tools.
The mapping is deliberately many to many rather than one lab per tool, because
the interesting problems sit where two tools meet: secrets injection next to RBAC
audit, an IAM boundary next to the scanner that verifies it, a vault next to the
cloud service that claims to replace it.
