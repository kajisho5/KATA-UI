# Owner-only publication and migration plan

No npm publish, deprecate, ownership or access changes have been performed by this PR.

## Publish @kajisho5/kataui 1.1.0

1. Merge the consolidated CLI PR after CI passes. Use an account with publication rights and verify the working tree.
2. From cli/: run `npm test`, `npm pack --dry-run` and inspect the four packaged files (script, README, CHANGELOG, package.json). No runtime dependencies or test fixtures are packaged.
3. Check `npm whoami` and `npm view @kajisho5/kataui@1.1.0 version`. If that version already exists, bump package.json, the standalone CLI VERSION and the changelog together; do not overwrite a published version.
4. The owner runs `npm publish --access public`. Follow npm authentication/2FA requirements.
5. Verify `npm view @kajisho5/kataui version` and `npx @kajisho5/kataui@1.1.0 --version`; smoke-test add against a disposable project with both legacy and v2 tokens. Confirm legacy warns, tokens stay byte-for-byte unchanged and the new package installs dependencies.

## Future name migration

Read-only lookup on 2026-11-05 found kata-ui@1.0.0 already published. @kata-ui/cli returned E404; that does not verify scope ownership, reservation or publication permission. These authorization details remain unverified.

1. Establish ownership/publication rights for the kata-ui scope before choosing @kata-ui/cli. If kata-ui is desired instead, establish ownership or an agreed transfer with its current owner; do not assume an occupied name is available.
2. Make a separate reviewed package-name migration, retaining the kataui bin command so scripts remain usable. Update site/README/Skill/llms/MCP installation instructions together. Do not change moldVersion for a package-name change.
3. Publish and test the replacement package first. Verify fresh installs, npx, --version, registry/dependency resolution and the mold warning on the supported Node versions.
4. Only after the replacement works, the owner may run `npm deprecate '@kajisho5/kataui@*' 'Moved to @kata-ui/cli. Use npx @kata-ui/cli; review https://kata-ui.dev/docs/update-mold/ before updating your mold.'` (adjust the name if a different one is chosen).
5. Keep old versions available; do not unpublish them. Document global-bin conflicts and the opt-in uninstall/install sequence for users who switch packages. Existing project files are never migrated or overwritten automatically.

## Verification scope

The integration tests ran on Linux with Node 24.19.0. The package still declares Node >=18; the APIs used are built-in. Windows/macOS and every Node release were not exercised here. No npm account ownership or publication operation was verified. The name lookups above are public metadata checks only.
