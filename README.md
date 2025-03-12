# PAM x Cloud Labs

Hands on lab work at the meeting point of privileged access management and cloud infrastructure. Each lab stands up a real environment, runs real tooling against it, and documents what actually happened, including the parts that broke.

**Stack:** CyberArk/Idira, Linux (RHEL 9), AWS, Azure

## What running them actually caught

Building infrastructure is the easy half. These are the defects that only appeared once the environments were stood up and the deployed objects were read back from the API rather than trusted from the config.

**A machine role that no machine could ever assume.** The `terraform-aws-modules/iam` module defaults `role_requires_mfa` to `true`. The DB broker is assumed by a service, and a service cannot present MFA, so the role deployed looking perfect, passed `terraform validate`, passed Checkov, and would have failed the first time anything tried to use it. Visible only by reading the deployed trust policy. — [lab 06](https://github.com/ChromeData/IAM-Least-Privilege)

**A CloudTrail bucket policy that trusted every AWS account.** Neither statement carried `aws:SourceArn`. The principal is the CloudTrail *service*, which is not scoped to an account, so the policy trusted CloudTrail globally rather than this account's trail — the cross-account confused-deputy pattern AWS has documented since 2022. Encryption and public access were both fine; the trust boundary was the thing nobody was checking. — [lab 09](https://github.com/ChromeData/AWS-Multi-Account-Baseline)

**A Key Vault hardened against access that recorded nobody who accessed it.** Soft delete, purge protection, network ACLs, RBAC — all correct. No diagnostic setting, so no `AuditEvent`. A vault nobody can reach is half a control; the other half is knowing who reached it. — [lab 10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails)

**An RBAC linter that reported a clean cluster.** Run against a live kind cluster holding four deliberately cluster-admin-equivalent roles, it printed `No risky RBAC found` and exited 0. `kubectl -o json` wraps everything in a single `kind: List` document, and the top-level kind check returned nothing. Every unit test passed the entire time, because every unit test fed it a hand-written manifest — the one shape it never meets in production. — [lab 08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan)

**Three credentials in plaintext in `terraform.tfstate`.** Minimal config, no AWS provider, nothing referencing the values. They landed in state anyway, including the full 40-character secret key. The lab's central claim, measured rather than asserted. — [lab 01](https://github.com/ChromeData/Conjur-Terraform-AWS)

Each one is written up in that lab's `LAB-NOTES.md` with the error output, the cause, and the fix.

## Labs

Every lab has been **run**, not just built. Each one has a `findings/` folder recording what actually happened, and the Verification column below says what was executed and against what.

Most ran without any cloud account: Docker for Conjur and Kubernetes, LocalStack for AWS IAM and S3, a Rocky container for OpenSCAP, Microsoft's Kusto container for KQL, and a stub tenant for psPAS. Where a claim genuinely needs a real subscription, that is stated in the lab rather than glossed.

| # | Lab | What it proves | Verification |
|---|-----|----------------|--------------|
| [01](https://github.com/ChromeData/Conjur-Terraform-AWS) | **Conjur secrets into a Terraform/AWS pipeline** | No credentials on disk or in state. Summon vs the data source leak, measured | Docker run, 4 bugs fixed, credential leak measured |
| [02](https://github.com/ChromeData/SkyArk-Shadow-Admin-Audit) | **Shadow admin discovery across AWS and Azure** | Escalation path analysis, scored against ground truth | 9 tests; paths planted on LocalStack, ground truth verified |
| [03](https://github.com/ChromeData/RHEL9-Hardened-Lab) | **Self building hardened RHEL 9 lab** | STIG remediation as code, measured before and after | 8 tests; real OpenSCAP scan, remediate, rescan |
| [04](https://github.com/ChromeData/Sentinel-Privileged-Access) | **Privileged access detections for Microsoft Sentinel** | PAM knowledge as working detection logic | 24 tests; all 4 detections executed against Kusto |
| [05](https://github.com/ChromeData/Secrets-Manager-PAM) | **AWS Secrets Manager as a PAM control plane** | Rotation, three layer access, honest CyberArk comparison | Applied on LocalStack, CMK and retrieval verified |
| [06](https://github.com/ChromeData/IAM-Least-Privilege) | **IAM least privilege and break glass roles** | Minimal roles proven with Access Analyzer and Checkov | Applied on LocalStack, controls read back from IAM |
| [07](https://github.com/ChromeData/IaC-Security-Gate) | **IaC security gate** | Blocks secrets and misconfig. Self test proves bad fails, good passes | 3 scanners run for real, bad fails, good passes |
| [08](https://github.com/ChromeData/Conjur-Kubernetes-KubiScan) | **Conjur secrets on Kubernetes plus KubiScan** | An offline RBAC linter, run against a real cluster. KubiScan cross-check still pending | 15 tests; real kind cluster, 15 RBAC findings |
| [09](https://github.com/ChromeData/AWS-Multi-Account-Baseline) | **AWS multi account security baseline** | A baseline that passes its own audit. Prowler scoring needs a real account | 14 tests; trail bucket applied and audited |
| [10](https://github.com/ChromeData/Azure-Landing-Zone-Guardrails) | **Azure landing zone guardrails** | Guardrail definitions unit tested, Bicep verified offline. Deny path needs Azure | 15 tests; Bicep verified with PSRule, 36 rules |
| [11](https://github.com/ChromeData/psPAS-PAM-Automation) | **CyberArk/Idira PAM automation with psPAS** | Account lifecycle plus drift reconciliation as idempotent runbooks | 29 tests; reconciler run against a stub tenant |
| [12](https://github.com/ChromeData/Network-Isolation-Access-Control) | **Network isolation as an access control** | The layer under IAM: can this host even reach the endpoint | 15 tests; verified on real AWS, negative control run live |

### Positive controls

Seven times while building these labs, a tool reported success while reading nothing: gitleaks after a version bump, checkov twice on nested ARM, the RBAC linter on live `kubectl` output, PSRule twice, and a pytest skip guard declared where pytest never looks. None announced itself.

Two more of the same shape appeared in the checks written *for* those bugs, which is the part worth sitting with.

So every check here has to count findings rather than trust an exit code, and has to have been **observed failing** before it counts as evidence. [POSITIVE-CONTROLS.md](./POSITIVE-CONTROLS.md) lists each one and exactly what breaks it.

See [REPO-COVERAGE.md](./REPO-COVERAGE.md) for which upstream tool each lab depends on and under what license.

**On status:** every lab has run and every lab has `findings/`. CI is green across all 11.

What each lab still cannot prove is stated in its own README and notes rather than averaged away here. The largest remaining gap is shared rather than per-lab: LocalStack creates IAM objects faithfully and **evaluates no policy at request time**, so every "this control actually blocks the request" claim across labs 02, 05, 06 and 09 is configured-and-verified, not observed-blocking. One free-tier AWS account closes all four. Labs 05, 09 and 10 additionally need a real subscription for CloudTrail data events, GuardDuty and Azure Policy deny.

The running the labs did produce found real bugs, including several in the labs' own tooling: an RBAC linter that reported a clean cluster while four cluster-admin-equivalent roles sat in it, a Key Vault hardened against access but keeping no record of who accessed it, a CloudTrail bucket policy trusting the CloudTrail service globally rather than its own trail, and a module default that silently required MFA on a machine role that can never present it.

## Linux depth

Lab 03 is the Linux one and it is not a Docker exercise. OpenSCAP against the DISA STIG profile for RHEL 9, scan then `oscap --remediate` then rescan, with the delta computed by a scorer in `scripts/`.

```
Baseline :  62 / 71 passed (87.3%)
Hardened :  68 / 71 passed (95.8%)
Delta    : +6 controls (+8.5 pp)
```

The interesting part is the denominator. Of the profile's 1532 rules, 412 came back `notapplicable` because that run was in a container: no kernel of its own, no bootloader, no GRUB, no auditd, no physical console. So the honest reading is +8.5 points on the 71-rule userspace subset, **not** a STIG compliance figure — which is exactly why the scorer excludes skips from the denominator. Counting them would have reported roughly 4% and looked catastrophic instead of narrow.

Also confirmed a distro trap the playbook had wrong: the datastream on Rocky is `ssg-rl9-ds.xml`, not `ssg-almalinux9-ds.xml`. Wrong path means zero rules evaluated, which presents as a clean pass.

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
