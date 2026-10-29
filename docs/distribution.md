# Distribution maintenance

The public repository contains the clean stock starter and its own new Git history. Users keep their working OS in a separate folder. Never publish the surrounding personal workspace or point a user's personal folder at the public upstream.

## Build a release asset

Run from the untouched stock development folder, using Python 3.10+:

```sh
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
python3 scripts/distribution.py build --output "/path/to/releases/rewired-os-0.6.0-beta.3.zip"
```

Replace the output example with an absolute path outside the source folder, without parent-directory segments or symlinked parents. Use a new output filename for each trial build; assets are never overwritten. The helper only includes the explicit `release-manifest.json` allowlist, adds `.rewired/installed.json`, and writes a `.zip.sha256` sidecar. With identical inputs the ZIP is reproducible. An installed folder, unexpected files, unsafe paths, and symlinks are rejected. Git history and cache directories are not packaged.

The allowlist is not proof that the contents are private-data-free: a template itself could have been personalized. Run the stock checker, review the actual extracted contents, and inspect a new repository's full tracked inventory/history before publication. Keep private test installations and output folders outside the stock starter. Neither build nor install makes network calls or creates a repository.

The receipt schema is `1`, product `rewired-os`, a semantic release version, and a map from stock relative paths to SHA-256 hashes and `managed`/`seed` policies. The updater independently enforces the protected seed paths. Bump the semantic version for changed distribution content; prereleases precede the final version. Same-version and older-version updates are refused. Rollbacks use recorded transactions instead.

## Release asset versus repository source ZIP

The official downloadable asset must be produced by the builder. A GitHub-generated source archive or repository clone does not contain the generated installation receipt. Source checkout is for development; it is not a tracked user installation. The agent must use the named release asset, or build a private package from reviewed source. Never invent a baseline for an existing personalized folder.

The release checksum catches corruption and comparison mistakes. It is not a publisher signature. Use the intended publisher's release channel. The helper validates bytes and paths; it does not certify that supplied Python code or agent instructions are trustworthy. Signed releases can be evaluated later.

## Before a public release

- Preserve the selected MIT license and current authorship record. Include third-party notices whenever the actual shipped material requires them.
- Run [release checks](release.md) and the [distribution pilot](distribution-testing.md); distinguish completed checks from remaining beta limits.
- For an existing product repository, use a reviewed commit and a new version tag; preserve its history. For a new repository, import only reviewed stock files, never personal workspace history.
- Keep the canonical repository and versioned asset links in README and INSTALL accurate. Verify assets before announcing a release.
- Publish a tagged, versioned asset and its checksum with release notes and the accurately tested runtime/provider matrix.
- Keep installation, update, and migration formats compatible, or document and test the transition. Avoid changing helper assumptions merely because a model has improved.

No general-purpose migration engine, background checker, GitHub API client, cloud-write updater, package manager, telemetry, or account system is included. The beta uses the folder, guided installation, and local update workflow.
