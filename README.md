# PAM x Cloud Labs

Hands on lab work at the meeting point of privileged access management and cloud infrastructure. Each lab stands up a real environment, runs real tooling against it, and documents what actually happened, including the parts that broke.

**Stack:** CyberArk/Idira, Linux (RHEL 9), AWS, Azure

## Labs

Every lab is built, code complete, and verified with `terraform validate`, Pester, or pytest, most with CI. Built means the code works and is tested. The last step, a live run that produces `findings/`, is per lab and noted below.

| # | Lab | What it proves | Verification |
|---|-----|----------------|--------------|
| [01](https://github.com/ChromeData/Conjur-Terraform-AWS) | **Conjur secrets into a Terraform/AWS pipeline** | No credentials on disk or in state. Summon vs the data source leak, measured | `terraform validate` |
| [02](https://github.com/ChromeData/SkyArk-Shadow-Admin-Audit) | **Shadow admin discovery across AWS and Azure** | Escalation path analysis, scored against ground truth | 9 tests, 2 TF roots |
| [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | **Self building hardened RHEL 9 lab** | STIG remediation as code, measured before and after | 8 tests, CI |
| [04](https://github.com/ChromeData/Sentinel-Privileged-Access) | **Privileged access detections for Microsoft Sentinel** | PAM knowledge as working detection logic | 13 tests, CI |
| [05](https://github.com/ChromeData/Secrets-Manager-PAM) | **AWS Secrets Manager as a PAM control plane** | Rotation, three layer access, honest CyberArk comparison | `terraform validate` |
| [06](https://github.com/ChromeData/IAM-Least-Privilege) | **IAM least privilege and break glass roles** | Minimal roles proven with Access Analyzer and Checkov | validate, Checkov CI |
| [07](https://github.com/ChromeData/IaC-Security-Gate) | **IaC security gate** | Blocks secrets and misconfig. Self test proves bad fails, good passes | self test passing |
| [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan) | **Conjur secrets on Kubernetes plus KubiScan** | Runtime injection plus an offline RBAC linter cross checking KubiScan | 11 tests, CI |
| [09](https://github.com/ChromeData/AWS-Multi-Account-Baseline) | **AWS multi account security baseline** | A baseline that passes its own audit, driven to zero with Prowler | 9 tests, validate |
| [10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails) | **Azure landing zone guardrails** | Azure Policy enforcement, role ID verified | 15 tests, Bicep CI |
| [11](https://github.com/ChromeData/psPAS-PAM-Automation) | **CyberArk/Idira PAM automation with psPAS** | Account lifecycle plus drift reconciliation as idempotent runbooks | 20 tests, CI |

See [REPO-COVERAGE.md](./REPO-COVERAGE.md) for which upstream tool each lab depends on and under what license.

**On status:** every lab's code is tested and green. What is not yet in each repo is a `findings/` folder, the output of running the lab against live cloud infrastructure. That is the deliberate last step (it costs real money and real credentials), and each repo's `LAB-NOTES.md` lists the exact questions that run will answer.

## How these labs are built

Every lab follows the same shape, and the shape is the point:

```
lab-name/
  README.md        what it is, how to run it, what it proves
  LAB-NOTES.md     the running log: errors, dead ends, fixes
  tests/           offline tests for the core logic (most labs)
  terraform/       or ansible, bicep, policy: the environment as code
  scripts/         bootstrap, teardown, and the scoring logic
  findings/        output, analysis, screenshots (from the live run)
```

**Two things make these more than a folder of Terraform.**

The tested core. Wherever a lab has real logic (a SkyArk scorer, a SCAP delta, an RBAC linter, a drift reconciler, a policy validator), that logic is unit tested offline and runs in CI. If the number a lab reports is wrong, a test goes red. That is the difference between "I ran a tool" and "I built the thing that checks the tool."

The lab notes. A dated log of "this failed, here is the error, here is why, here is the fix" reads as real experience because it is. Several of these labs found genuine bugs during the build (a Terraform dependency cycle, a policy that would have protected nothing, a security gate that failed its own scan), and the notes record them.

## Attribution

These labs build on open source tooling. The environments, test methods, analysis, and findings are mine. The upstream tools are not, and each lab's README credits them. Nothing upstream is copied into these repos.

> **On the name:** Palo Alto Networks acquired CyberArk and rebranded the platform Idira. Repos and docs are mid migration. Labs here use whichever name the tooling itself uses at the pinned version.
