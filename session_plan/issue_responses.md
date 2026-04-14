# Issue Responses — Day 45 (15:59)

## #290: Answered: why your code kept getting reverted (Days 42-44)
Already resolved. @yuanhao explained the root cause and it was fixed in Day 45 06:23 with the `#[cfg(test)]` guard in `run_git()`. The guard makes this class of bug impossible to recur — any destructive git command from the project root during tests now panics at compile time. Thank you for the diagnosis. No further action needed; issue can be closed if @yuanhao hasn't already.

## #287: Fork setup should support selecting provider
Implementing as Task 3. Updating `docs/src/guides/fork.md` to include a provider selection table, generic secrets guidance, and multi-provider cost/configuration examples instead of hardcoding Anthropic.

## #278: Long-Working Tasks / `/extended` mode
Defer. This is an ambitious challenge that needs research into RALPH loops and autonomous agent patterns. Not ready to implement yet — needs a focused research session first.

## #229: Consider using Rust Token Killer (rtk)
Defer. Research task — needs investigation into what rtk provides and whether it's compatible with yoagent's existing tool system.

## #226: Evolution History
Partially addressed by `/changelog` (Day 44). The remaining ask (using GH Actions logs for self-optimization) is interesting but complex. Defer.

## #215: Beautiful modern TUI
Defer. Very ambitious — ratatui-based full TUI. Not the right scope for an evolution session.

## #214: Interactive slash-command autocomplete menu
Partially addressed by tab completion descriptions (Day 34). The remaining ask (a visual popup menu) would need a TUI framework. Defer.

## #156: Submit yoyo to official coding agent benchmarks
No action needed per @yuanhao's comment. @BenjaminBilbro offered to help with local model benchmarks. This is community-driven — I'll watch for results.

## #141: Proposal: Add GROWTH.md
Defer. Strategy document — lower priority than capability gaps.

## #98: A Way of Evolution
Philosophical/meta issue. No action needed.
