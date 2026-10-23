# Mandatory evidence capture for remaining validation

Capture is part of every remaining test/remediation phase, before temporary resources are stopped or deleted. Keep tests sequential on this laptop. A useful existing capture takes precedence over restarting an expensive stack only for a new picture.

1. Identify the exact official requirement number/title from [requirements.json](../presentation-evidence/requirements.json) and the narrow assertion being checked.
2. Record the real command or workflow URL, actual software/image versions, environment, source revision and observation time. Keep complete sanitized text output even when a screenshot is possible.
3. As soon as the result is visible, capture the actual UI or terminal **before cleanup**. For lost historical terminal sessions, a clearly labeled screenshot of real archived output is acceptable; never call it the original terminal or a current running system.
4. Record PASSED, FAILED, PARTIALLY VALIDATED or NOT YET TESTED accurately. A passing configuration render is not a working deployment. A healthy Argo server is not a synced Application. A green historical release does not supersede a failing newer gate.
5. Never include passwords, bearer tokens, login forms containing credentials, private keys, kubeconfigs, Secret values, full environment dumps or database archive contents. Select non-secret inspect fields. Test-only public record IDs/titles are safe; database dumps stay outside Git.
6. Save a readable `.jpg` browser screenshot under its numbered official requirement folder. Browser screenshots are JPEG, so do not rename them to PNG. Keep surrounding context and dates; do not edit failure into success. Verify the saved file visually.
7. Add screenshot metadata: what it demonstrates, supported requirement(s), capture date, original observation date, software versions, environment, result, command/workflow link, source artifact path/SHA-256 and screenshot SHA-256. State limitations and whether it is actual UI, archived output, configuration or design.
8. If capture is unavailable, preserve the genuine text artifact and explain the blocker in [missing-evidence.md](../presentation-evidence/missing-evidence.md). Do not create a fake successful screenshot for that gap.
9. Update the evidence index, [checklist](../requirements-validation-checklist.md), [final compliance report](../final-compliance-report.md) and [presentation plan](../presentation-evidence.md). For the current fixed catalog, `python3 scripts/build-presentation-evidence.py` regenerates the archived-output HTML views and index; it does not run tests or capture screenshots.
10. Run `python3 scripts/check-presentation-evidence.py`. Only after the evidence is safely stored, clean up that phase's resources and verify unrelated applications remain untouched.

The primary folders and all report headings follow the user's exact ten official requirement titles. The optional [technical-category navigation](categories/README.md) cross-links the original eight requested categories without duplicating or inflating screenshot counts.
