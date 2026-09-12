# Portable report fonts

The builder accepts optional --font NAME and otherwise leaves the document theme and system fallback in control. Select a font actually installed in the target environment that covers Chinese and required scientific glyphs. Inspect rendered pages; supplying a font name does not prove it exists.

Use normal renderer/operating-system font discovery. Keep task-controlled caches inside the task directory. Do not copy proprietary font binaries or assume Arial Unicode MS is installed. The retained macos-fontconfig.conf is an inert historical resource, not a runtime requirement and must not be loaded.
