# PAM × Cloud Labs

Hands-on lab work at the intersection of privileged access management and cloud
infrastructure. Each lab stands up a real environment, runs real tooling against it,
and documents what actually happened — including the parts that broke.

**Stack:** CyberArk/Idira · Linux (RHEL 9) · AWS · Azure

---

## Labs

| # | Lab | What it proves | Status |
|---|-----|----------------|--------|
| [01](./01-conjur-terraform-aws) | **Conjur secrets injection into a Terraform/AWS pipeline** | Machine identity, dynamic secrets, zero credentials on disk or in state | 🟡 In progress |
| [02](./02-skyark-shadow-admin-audit) | **Shadow-admin discovery across AWS + Azure** | Privilege-escalation path analysis in two clouds | 🟡 In progress |
| [03](./03-rhel9-hardened-lab) | **Self-building hardened RHEL 9 lab** | CIS/STIG remediation as code, measured before and after | 🟡 In progress |
| [04](./04-sentinel-privileged-access) | **Privileged-access detections for Microsoft Sentinel** | Turning PAM domain knowledge into working detection logic | 🟡 In progress |
| [05](./05-secrets-manager-pam) | **AWS Secrets Manager as a PAM control plane** | Rotation, least-privilege resource policies, and an honest CyberArk comparison | 🟡 In progress |
| [06](./06-iam-least-privilege) | **IAM least-privilege & break-glass broker roles** | Minimal roles proven with Access Analyzer + Checkov | 🟡 In progress |
| [07](./07-iac-security-gate) | **IaC security gate (pre-commit + CI)** | Blocking secrets and misconfig before they reach the repo | 🟡 In progress |
| [08](./08-conjur-kubernetes-kubiscan) | **Conjur secrets on Kubernetes + KubiScan RBAC audit** | Runtime secret injection into pods, then a cluster RBAC audit | 🟡 In progress |
| [09](./09-aws-multiaccount-baseline) | **AWS multi-account security baseline** | SRA-aligned org baseline driven to zero with Prowler | 🟡 In progress |
| [10](./10-azure-landing-zone-guardrails) | **Azure landing-zone privileged-access guardrails** | Azure Policy enforcement + Verified Modules | 🟡 In progress |
| [11](./11-pspas-pam-automation) | **CyberArk/Idira PAM automation with psPAS** | Privileged-account lifecycle as idempotent runbooks | 🟡 In progress |

See [REPO-COVERAGE.md](./REPO-COVERAGE.md) for how the shortlisted repos map across these labs, and [PROFILE-README-TEMPLATE.md](./PROFILE-README-TEMPLATE.md) for the profile page.

## Publishing to GitHub

Run **[`PUSH.sh`](./PUSH.sh)** — it detects your GitHub username from the `gh` CLI, creates a repo per lab plus the profile repo, pushes everything, and pins the six strongest. Preview first with `./PUSH.sh --dry-run`. Prereqs: [GitHub CLI](https://cli.github.com) installed and `gh auth login` done.

Update the status column as you go: 🟡 In progress · 🟢 Complete · 🔵 Complete + written up

---

## How these labs are built

Every lab follows the same structure, and the structure is the point:

```
NN-lab-name/
├── README.md        # what it is, how to run it, what I found
├── LAB-NOTES.md     # the running log — errors, dead ends, fixes
├── terraform/       # or ansible/ — the environment, as code
├── scripts/         # bootstrap and teardown
└── findings/        # output, analysis, screenshots
```

**LAB-NOTES.md is the differentiator.** Anyone can push a clean Terraform module.
A dated log of "this failed, here's the error, here's why, here's the fix" is the
thing that reads as real experience — because it is.

---

## Attribution

These labs build on open-source tooling. The environments, test methodology,
analysis and findings are mine. The upstream tools are not, and are credited
in each lab's README:

| Lab | Built on | License |
|-----|----------|---------|
| 01 | [cyberark/conjur](https://github.com/cyberark/conjur), [cyberark/terraform-provider-conjur](https://github.com/cyberark/terraform-provider-conjur) | LGPL-3.0 / Apache-2.0 |
| 02 | [cyberark/SkyArk](https://github.com/cyberark/SkyArk) | MIT |
| 03 | [ComplianceAsCode/content](https://github.com/ComplianceAsCode/content), [dev-sec/ansible-collection-hardening](https://github.com/dev-sec/ansible-collection-hardening) | BSD-3-Clause / Apache-2.0 |
| 04 | [Azure/Azure-Sentinel](https://github.com/Azure/Azure-Sentinel) | MIT |
| 05 | [terraform-aws-modules/terraform-aws-secrets-manager](https://github.com/terraform-aws-modules/terraform-aws-secrets-manager) (Anton Babenko) | Apache-2.0 |
| 06 | [terraform-aws-modules/terraform-aws-iam](https://github.com/terraform-aws-modules/terraform-aws-iam) (Anton Babenko) | Apache-2.0 |
| 07 | [antonbabenko/pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform), [gitleaks](https://github.com/gitleaks/gitleaks), [checkov](https://github.com/bridgecrewio/checkov), [trivy](https://github.com/aquasecurity/trivy) | MIT / Apache-2.0 |
| 08 | [cyberark/conjur](https://github.com/cyberark/conjur), [cyberark/KubiScan](https://github.com/cyberark/KubiScan) | LGPL-3.0 / GPL-3.0 |
| 09 | [prowler-cloud/prowler](https://github.com/prowler-cloud/prowler), [aws-samples/aws-security-reference-architecture-examples](https://github.com/aws-samples/aws-security-reference-architecture-examples) | Apache-2.0 / MIT-0 |
| 10 | [Azure/azure-policy](https://github.com/Azure/azure-policy), [Azure/Azure-Verified-Modules](https://github.com/Azure/Azure-Verified-Modules) | MIT |
| 11 | [pspete/psPAS](https://github.com/pspete/psPAS), [cyberark/epv-api-scripts](https://github.com/cyberark/epv-api-scripts) | MIT / Apache-2.0 |

> **Note on CyberArk → Idira:** Palo Alto Networks completed its acquisition of
> CyberArk and rebranded the platform as Idira. Repos and docs are mid-migration —
> `conjur-cli-go` and `psPAS` already carry the new naming. Labs here use whichever
> name the tooling itself uses at the version pinned.

---

## Cost and safety

- Labs 01, 02 and 04 provision cloud resources. **Every lab has a `make destroy`.** Run it.
- Lab 02 deliberately creates insecure IAM configurations. It is scoped to a
  throwaway account and tagged `Purpose=security-lab`. Do not run it anywhere else.
- No real credentials are committed. `.gitignore` covers `*.tfstate`, `*.tfvars`,
  `.env` and `secrets/`.
