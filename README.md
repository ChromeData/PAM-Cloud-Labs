# PAM × Cloud Labs

Hands-on lab work at the intersection of privileged access management and cloud
infrastructure. Each lab stands up a real environment, runs real tooling against it,
and documents what actually happened — including the parts that broke.

**Stack:** CyberArk/Idira · Linux (RHEL 9) · AWS · Azure

---

## Labs

Every lab is built, code-complete, and verified — Terraform `validate`, Pester,
or pytest, most with CI. **Built** means the code works and is tested; the last
step, a live run producing `findings/`, is per-lab and marked below.

| # | Lab | What it proves | Verification |
|---|-----|----------------|--------------|
| [01](https://github.com/ChromeData/Conjur-Terraform-AWS) | **Conjur secrets injection into a Terraform/AWS pipeline** | Zero credentials on disk or in state — Summon vs. the data-source leak, measured | 🟢 `terraform validate` |
| [02](https://github.com/ChromeData/SkyArk-Shadow-Admin-Audit) | **Shadow-admin discovery across AWS + Azure** | Privilege-escalation path analysis, scored against ground truth | 🟢 9 tests · 2 TF roots |
| [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | **Self-building hardened RHEL 9 lab** | CIS/STIG remediation as code, measured before and after | 🟢 8 tests · CI |
| [04](https://github.com/ChromeData/Sentinel-Privileged-Access) | **Privileged-access detections for Microsoft Sentinel** | PAM domain knowledge as working detection logic | 🟢 13 tests · CI |
| [05](https://github.com/ChromeData/Secrets-Manager-PAM) | **AWS Secrets Manager as a PAM control plane** | Rotation, three-layer access model, honest CyberArk comparison | 🟢 `terraform validate` |
| [06](https://github.com/ChromeData/IAM-Least-Privilege) | **IAM least-privilege & break-glass broker roles** | Minimal roles proven with Access Analyzer + Checkov | 🟢 validate · Checkov CI |
| [07](https://github.com/ChromeData/IaC-Security-Gate) | **IaC security gate (pre-commit + CI)** | Blocks secrets + misconfig — self-test proves bad fails, good passes | 🟢 self-test passing |
| [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan) | **Conjur secrets on Kubernetes + KubiScan RBAC audit** | Runtime injection + an offline RBAC linter cross-checking KubiScan | 🟢 11 tests · CI |
| [09](https://github.com/ChromeData/AWS-Multi-Account-Baseline) | **AWS multi-account security baseline** | SRA-aligned baseline that passes its own audit, driven to zero with Prowler | 🟢 9 tests · validate |
| [10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails) | **Azure landing-zone privileged-access guardrails** | Azure Policy enforcement, GUID-verified | 🟢 15 tests · Bicep CI |
| [11](https://github.com/ChromeData/psPAS-PAM-Automation) | **CyberArk/Idira PAM automation with psPAS** | Privileged-account lifecycle + drift reconciliation as idempotent runbooks | 🟢 20 tests · CI |

See [REPO-COVERAGE.md](./REPO-COVERAGE.md) for how the shortlisted repos map across these labs, and [PROFILE-README-TEMPLATE.md](./PROFILE-README-TEMPLATE.md) for the profile page.

**On status:** every lab's code is tested and green. What's not yet in each repo
is a `findings/` folder — the output of running the lab against live cloud
infrastructure. That's the deliberate last step (it costs real money and real
credentials), and each repo's `LAB-NOTES.md` lists the exact questions that run
will answer.

---

## How these labs are built

Every lab follows the same structure, and the structure is the point:

```
lab-name/
├── README.md        # what it is, how to run it, what it proves
├── LAB-NOTES.md     # the running log — errors, dead ends, fixes
├── tests/           # offline tests for the analytical core (most labs)
├── terraform/       # or ansible/ bicep/ policy/ — the environment, as code
├── scripts/         # bootstrap, teardown, and the scoring/analysis logic
└── findings/        # output, analysis, screenshots (from the live run)
```

**Two things make these more than a folder of Terraform:**

**The tested core.** Wherever a lab has analytical logic — a SkyArk scorer, a
SCAP delta, an RBAC linter, a drift reconciler, a policy validator — that logic
is unit-tested offline and runs in CI. If the number a lab reports is wrong, a
test goes red. That's the difference between "I ran a tool" and "I built the
thing that checks the tool."

**LAB-NOTES.md.** A dated log of "this failed, here's the error, here's why,
here's the fix" reads as real experience because it is. Several of these labs
found genuine bugs during the build — a Terraform dependency cycle, a policy
that would have protected nothing, a security gate that failed its own scan —
and the notes record them.

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
