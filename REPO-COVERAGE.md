# How the ten repos map to these labs

The earlier shortlist was ten repos worth having on your profile. They don't map
one-to-one to ten labs — some are contribution targets, some are references, and
several combine into a single stronger lab. Here's where each one lands, so the
whole list is accounted for.

| # | Repo (from the shortlist) | Where it lives in the labs | How you engage it |
|---|---------------------------|----------------------------|-------------------|
| 1 | **prowler** | Referenced in Lab 02 (cross-check SkyArk findings) & Lab 04 | Star + contribute a check |
| 2 | **cyberark/SkyArk** | **Lab 02** — the core tool | Fork, run, score |
| 3 | **pspete/psPAS** | Natural extension of Lab 02 / a future Lab | Fork, contribute a cmdlet |
| 4 | **ComplianceAsCode/content** | **Lab 03** — the STIG/CIS content source | Use + contribute upstream |
| 5 | **cyberark/conjur** | **Lab 01** — the secrets engine | Deploy, model policy |
| 6 | **cyberark/epv-api-scripts** | Extension of Lab 01 (EPV automation) | Fork, adapt |
| 7 | **Azure/Azure-Verified-Modules** | Substrate for Lab 04's Azure resources | Contribute a module |
| 8 | **Azure/Azure-Sentinel** | **Lab 04** — the detection platform | Use + submit a detection |
| 9 | **dev-sec/ansible-collection-hardening** | **Lab 03** — the remediation roles | Use + contribute |
| 10 | **terraform-aws-modules (eks/vpc/iam)** | **Labs 05 & 06** (secrets-manager, iam) | Fork, configure, verify |

Plus the antonbabenko-derived additions from his profile:

| Repo | Lab | Why |
|------|-----|-----|
| terraform-aws-secrets-manager | **Lab 05** | Your signature CyberArk-vs-cloud comparison |
| terraform-aws-iam | **Lab 06** | Least-privilege broker roles |
| pre-commit-terraform | **Lab 07** | Policy-as-code gate (+ the gitleaks gap you fill) |
| terraform-best-practices | Audit method across all labs | Score your own repos against it |

## The eleven labs

1. **Conjur → Terraform secrets injection** (AWS, no creds in state)
2. **SkyArk shadow-admin audit** (AWS + Azure escalation scoring)
3. **RHEL 9 hardening** (OpenSCAP before/after delta)
4. **Sentinel privileged-access detections** (KQL, ATT&CK-mapped)
5. **Secrets Manager as a PAM control plane** (rotation + CyberArk comparison)
6. **IAM least-privilege broker roles** (Access Analyzer + Checkov verified)
7. **IaC security gate** (pre-commit + CI, secrets + misconfig)
8. **Conjur on Kubernetes + KubiScan** (runtime injection + RBAC audit)
9. **AWS multi-account baseline** (SRA + Prowler to zero)
10. **Azure landing-zone guardrails** (Azure Policy + AVM)
11. **CyberArk/Idira PAM automation** (psPAS runbooks)

Labs 1–4 are the deepest; 5–7 are faster wins; 8–11 broaden the stack into
Kubernetes, multi-account AWS, Azure governance, and pure PAM. Every one is honest
work you can defend line by line — built on named upstream tools, with your
environment, your findings, and your analysis on top.

Which six to pin: `PUSH.sh` pins the umbrella repo plus labs 1, 2, 5, 8, and 11 —
a spread that shows CyberArk, AWS, Azure, Kubernetes, and PAM in the first glance at
your profile. Change the `PINS` array in `PUSH.sh` if you'd rather lead with others.
