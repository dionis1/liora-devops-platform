# Reviewed integration patch

The original MIT-licensed [DataScientest application](https://github.com/DataScientest/fastapi-traefik-datascientest-project)
remains a Git submodule at its recorded gitlink. Its history and attribution are
preserved. No unpublished replacement submodule commit is required.

Run `bash scripts/prepare-course-app.sh` after initializing the submodule. The
script verifies the pinned revision, checks the patch before applying, is
idempotent, and refuses conflicting local edits. CI runs the same step.

`course-app-platform.patch` explicitly contains the platform integration:

- Python 3.12 dependency locking and security updates, including Sentry 2.
- Compatible public-model typing and PostgreSQL URL construction.
- Correct inactive-user and startup-session assertions in upstream tests.
- A platform-owned ASGI metrics entrypoint around the existing FastAPI app.
- Frontend dependency security updates, Vite 6, and reproducible npm locking.
- A nullable theme-selection guard needed by current Chakra types.
- Targeted transitive overrides (including tar 7) verified by the production frontend build. Client generation and browser end-to-end tests still need separate validation.

The application is not replaced. Review this patch whenever upgrading the
submodule; update the gitlink and regenerate/retest the patch together. A fork
would require separate authorization and publication; this strategy needs no
upstream write access. Applying the patch deliberately makes the submodule
working tree dirty. Commit the patch in this repository, not an inaccessible
submodule commit.
