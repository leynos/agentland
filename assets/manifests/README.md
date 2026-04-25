# Asset manifests

Every accepted project-bound generated image needs a JSON manifest under this
directory. Manifests are provenance records, validation records, and runtime
promotion controls.

## Required workflow

1. Write the structured prompt under `prompts/generated/<family>/`.
2. Generate with Codex built-in `image_gen`.
3. Inspect the output.
4. Copy the accepted source into `assets/source/gpt-images-2/<family>/`.
5. Create a manifest under `assets/manifests/<family>/`.
6. Run any post-processing.
7. Update the manifest with processed paths, settings, and validation notes.

Do not reference generated images from code while they exist only under
`$CODEX_HOME`.

## Required fields

Each manifest records:

- asset `id`, `family`, and `status`;
- tool mode, model family, and fallback state;
- prompt path, final prompt text, and input image roles;
- Codex generated path when known;
- workspace source path;
- processed and atlas paths when present;
- source dimensions and format;
- post-processing settings;
- validation notes;
- runtime use.

See [`docs/asset-spec.md`](../../docs/asset-spec.md) for the canonical schema.
