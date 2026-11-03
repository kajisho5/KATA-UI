# Website deployment

Production source is main. Open website PRs against main; merging into a feature branch only updates a preview. The existing Cloudflare Pages Git integration builds this repository (project kata-ui). Build command: python3 build.py. Output directory: dist, also declared in wrangler.toml.

The Build website GitHub workflow runs generator tests and produces an artifact on PRs and pushes to main. It does not upload to Cloudflare: the existing Pages integration owns deployment, so no new credential is needed. Failed component checks are published in mold-results.json; a broken generator fails the build.

After merging, check the Cloudflare Pages deployment for that main commit and open kata-ui.dev. A successful preview check alone does not establish that production changed. Cloudflare project production-branch/build settings are remote settings; if the integration is paused or main is not the production branch, a project administrator must set production branch main, enable automatic production deployments, and use the build/output settings above.
