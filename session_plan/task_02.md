Title: Add GPT-5 and latest model definitions to providers.rs
Files: src/providers.rs
Issue: none

## What to do

Aider already supports GPT-5 family models. We should add them to stay competitive on model breadth. This is a single-file change to `src/providers.rs` with existing test patterns to follow.

### Specific changes:

1. **Add GPT-5 models to the OpenAI known models list** in `known_models_for_provider`:
   - Add `"gpt-5"` and `"gpt-5-mini"` to the openai match arm
   - These follow the naming convention established by `gpt-4o` and `gpt-4o-mini`

2. **Add Grok-4 models to the xAI known models list**:
   - Add `"grok-4"` to the xai match arm (announced and available via xAI API)

3. **Add new tests** following the existing test patterns:
   - `test_openai_known_models_includes_gpt5` — verify `gpt-5` is in the list
   - `test_xai_known_models_includes_grok4` — verify `grok-4` is in the list
   - `test_openai_default_model` — verify the default is still `gpt-4o` (regression guard)

### Important constraints:
- Do NOT change any default models — just add to the known models lists
- Follow the exact pattern of existing model entries (string literals in the slice)
- Keep alphabetical/generational ordering within each provider's list
- This is purely additive — no existing behavior changes
