# Documents releases

Tag format: `documents-YYYY-MM-DD` (the date is the publication/release date)

Each `documents-*` release archives one document (typically a single PDF) to:

- formalize authorship and licensing under the repository's license for artifacts ([CC-BY-4.0](https://raw.githubusercontent.com/Health-RI/semantic-interoperability/refs/heads/main/LICENSE-ARTIFACTS.md)), and
- trigger Zenodo DOI minting and long-term archiving.

This is **not** a version series: later `documents-*` tags **do not** supersede earlier ones unless the release notes explicitly say so.

## Citation

Cite the **version-specific Zenodo DOI** for the relevant release. Do not cite the Zenodo concept DOI (project's DOI) when you need to reference this exact document.

## Edge cases

- Multiple documents on the same date: `documents-YYYY-MM-DDa`, `documents-YYYY-MM-DDb`, and so on.
- New version of the same document: publish a new `documents-*` release and state in the release notes that it supersedes the previous version.
