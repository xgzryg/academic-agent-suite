# Bundled engine scope

Selected SVG/DrawingML, template extraction, native fill, notes and text-layout modules are bundled under the accompanying MIT license. The original project website, source template archives, private examples, full icon catalog and restricted Office helpers are not bundled.

The supported entrypoint is `engine.py`. It uses task-local temporary storage, native output without default animation, explicit output paths and existing-file checks. Template fill preserves paragraph formatting and the first text run's style for each replacement paragraph. For exact mixed-emphasis retention, `patch-runs` edits existing runs in place. Arbitrary new paragraphs cannot automatically inherit the intended semantic mapping of previous highlights.

Template asset extraction returns actual media, theme/style metadata and slide/layout relationships. A source-specific asset extraction is not a completed content-free reusable template: the calling agent must still identify fixed chrome versus replaceable content, define appropriate slots and verify a second content set.

The original `config.py` home/repository fallback was scoped to the working directory. Use the supported entrypoint instead of treating the original project-management commands as part of this bundle.

`svg_to_pptx` and related modules remain mostly unchanged, including existing optional SVG image compatibility and media support. The supported default uses only native DrawingML. No SVG icon placeholders are accepted without inlining; no external icon archive is required. Unsupported SVG features fail and must be simplified or explicitly handled as localized raster assets.

Native notes/audio/timing code is included as an optional module. Basic notes editing is verified in the package's build validation; online TTS, full multimedia playback and every PowerPoint transition are not claimed to be verified. The package contains no credentials and performs no automatic dependency installation.

Notes relationships and content-type entries are edited as XML elements so that template-generated namespace prefixes are supported. When a deck has no notes master, a complete native default notes master and a dedicated theme are created through the installed python-pptx library; existing notes masters are preserved. This fixes a desktop PowerPoint rejection observed with the previous minimal notes master. Both SVG-created notes and existing-deck notes were checked in actual PowerPoint, with visible slide XML unchanged for the latter.
