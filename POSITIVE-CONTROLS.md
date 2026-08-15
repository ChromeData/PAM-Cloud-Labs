# Positive controls

Seven times while building these labs, a tool reported success while reading
nothing. Not one of them announced itself. Every one produced a confident green.

```
gitleaks         version bump changed its detection; the gate still passed
checkov          nested ARM: descended into nothing, "0 checks", clean exit
checkov          the same template flattened: 5 failures, all false positives
rbac_lint        live kubectl output: "No risky RBAC found" on a cluster
                 holding four cluster-admin-equivalent roles
PSRule           could not find the bicep binary: "Rules processed: 0"
PSRule           an input.pathIgnore entry excluded the only target: 0 again
pytest           a skip guard declared in a helper module, where pytest
                 never looks for one
```

Plus two I wrote into the checks *for* those bugs, which is the part worth
sitting with:

```
canary.sh        "passed" against a file that did not exist, because a
                 missing-file error is also a non-zero exit
gate-selftest    scored a scanner that crashed as a successful detection,
                 for the same reason
```

## The rule

**A green result is not evidence until something has been seen to fail.**

Concretely, every check in these repos has to satisfy two properties:

1. **It counts, it does not merely exit.** `exit != 0` conflates "found the
   problem" with "could not run". Parse the tool's own output and assert a
   non-zero finding count. Report "could not run" as its own failure, never as
   a detection.

2. **It has been observed failing.** Break the thing it watches, watch the
   check go red, put it back. If that has never been done, the check is
   decoration.

## Where each lab implements it

| Lab | Control | What breaks it |
|---|---|---|
| 07 | `scripts/gate-selftest.sh` | Replace a scanner with `exit 1`; it now reports 0 findings and fails |
| 08 | `scripts/canary.sh` | Disable List traversal; the wrapped shape returns nothing and fails |
| 10 | CI rule-count floor | A zero-rule run cannot pass; a working run evaluates 36 |
| 04 | CI skip guard | If the suite skips instead of running, the job fails |
| 02 | `scripts/verify_ground_truth.py` | Both directions, and both were induced deliberately |
| 11 | Pester suite | Sabotaged the UNEXPECTED branch, watched it go red, restored |
| 13 | Chaos target selection | Feed it a `Terminating` instance; it must return None rather than kill something already dead |
| 14 | CI job `Prove the tests can fail` | Three breaks applied in CI, and the build fails if the suite does not catch each one |

## What this does not fix

Offline checks cannot see enforcement. LocalStack builds IAM objects and
evaluates no policy at request time, so "the boundary blocks this request" is
unverifiable locally no matter how many positive controls are added.

That is what `06/scripts/prove-enforcement.sh` is for: one free run, four
checks, and it closes labs 02, 05, 06 and 09 together.

## Lab 14 automated it

Every control above was run by hand once, which means it was true once. Lab 14
moved the idea into CI: a job that applies three deliberate breaks to the module
and **fails the build if the test suite does not catch each one**.

That is the difference between "I verified this" and "this stays verified." A
suite can rot into uselessness on any commit, and nothing about a green badge
would change.

It also caught its own version of the bug. Lab 14's tests reported
`9 passed, 0 failed` on my machine, and in a clean environment reported
`0 passed, 1 failed, 8 skipped`, because the AWS provider validates credentials
at init even for a plan. Eight skips read as fine in a CI summary. That is the
eighth occurrence of the same failure shape in this portfolio, and the first one
found by a rule written after the previous seven.
