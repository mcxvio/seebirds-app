# Patch handoff

For this workflow, Codex prepares the scoped change and validates it locally. The
handoff includes a patch generated from the committed Git objects, together with
the base and result commit IDs, file hashes, and validation evidence.

ChatGPT applies that exact patch to the stated base, confirms that its contents
and scope match the handoff, and publishes the branch and pull request. This
separates implementation evidence from publication evidence without requiring
the change to be rewritten between tools.

Marcus retains the final review and merge decision. A successful handoff proves
this small text-patch route only; it does not by itself validate larger or binary
transfers.
