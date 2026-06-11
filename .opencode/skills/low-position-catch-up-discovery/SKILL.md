---
name: low-position-catch-up-discovery
description: Use when the user says "找低位补涨的", "低位补涨", "未启动个股", "预期差", "补涨龙", or asks to find laggard/catch-up stocks after a theme leader has already moved.
---

# Low-Position Catch-Up Discovery

Use this skill to find research-only A-share or HK candidates that may benefit from theme diffusion, low-position catch-up, or expectation gaps after a market leader has already validated a theme.

This is not a buying system. A candidate can be worth tracking because it has a credible setup, but it is not actionable unless the repository's deterministic investment gates, liquidity gates, risk review, and the user's manual decision all agree.

## When To Use

Use this skill when the user asks things like:

- `找低位补涨的`
- `找还没启动的`
- `找预期差`
- `找补涨龙`
- `这个题材还有没有低位票`
- `龙头涨太多了，看看后排`
- `按补涨逻辑找候选`
- `这个主线还能扩散到谁`

If the user asks for ordinary industry-chain mapping without catch-up/laggard logic, use `industry-chain-stock-discovery` instead. If the user asks for high-volatility monster-stock traits, combine this with `ah-monster-stock-discovery`.

## Core Principle

Low-position catch-up is not simply buying anything that has not risen. The target is:

`leader-confirmed theme -> credible same-chain exposure -> lower consensus/price position -> beginning volume confirmation -> explicit invalidation`

The best research window is usually after the leader has proven the theme, but before the market has fully agreed on the next-tier beneficiary.

## Define The Theme First

Before naming stocks, explain why the original theme can keep running.

Check whether the theme has at least three of these persistence drivers:

- Real price anchor: product price, commodity price, freight rate, drug approval, order data, policy date, or benchmark index can be tracked.
- Supply constraint: export control, quota, accident, shutdown, certification bottleneck, capacity shortage, or long qualification cycle.
- Demand pull: AI capex, HBM/3D NAND, EV/robotics, healthcare demand, RWA/stablecoin policy, consumer trend, or restocking.
- Scarce listed exposure: only a few public companies have direct enough exposure.
- Profit-pool shift: upstream/downstream margins are moving from old players to new domestic suppliers.
- Multiple catalysts over time: the thesis has staged events instead of one headline.
- Market confirmation: leader keeps relative strength and same-theme breadth improves.

If the theme has only one news catalyst and no follow-up evidence, do not search aggressively for catch-up names; label the request as `theme too thin`.

## Candidate Layers

Always separate candidates by causal distance from the leader.

| Layer | Meaning | Typical catch-up quality |
| --- | --- | --- |
| Core catch-up | Same product or same bottleneck, lower price consensus than leader | Best if evidence is filing-backed |
| Expectation gap | Trial production, certification, upcoming capacity, pending license/order | High elasticity, high verification risk |
| Upstream bottleneck | Raw material, equipment, consumable, component, qualification service | Better when pricing power improves |
| Downstream pull | Direct demand beneficiary with backlog/order acceleration | Better for swing research than pure emotion |
| Second-order beneficiary | Infrastructure, logistics, power/cooling, testing, packaging, brokers/payments | Watch only unless volume confirms |
| Concept proxy | Same label but weak business link | Usually ignore or diagnostic only |

## What Counts As "Not Started"

Do not require a stock to be flat. Use stricter labels:

- `dormant`: low attention, no abnormal volume, near base or moving-average cluster.
- `pre-ignition`: mild volume expansion, close above key moving average, no market-wide recognition yet.
- `early catch-up`: first strong day or first board, theme leader still active, market has not fully labeled it.
- `confirmed catch-up`: first divergence absorbed, volume expands, close remains strong, peer breadth supports.
- `late catch-up`: multiple boards/large candles after media consensus; monitor risk, not fresh discovery.
- `avoid`: no credible exposure, hard risk, illiquid/unexitable, severe regulatory/announcement risk, or pure rumor.

Fresh research should prefer `pre-ignition`, `early catch-up`, or `confirmed catch-up`. Treat `late catch-up` as risk monitoring.

## Discovery Workflow

1. Identify the leader and the exact causal theme.

- Do not stop at a broad sector label like `半导体` or `电子特气`.
- Narrow it to the real driver, such as `六氟化钨涨价`, `稀土出口许可`, `稳定币牌照`, `AI制药临床进展`, `车企账期缩短`, or `PCB上游材料涨价`.

2. Explain why the theme has lasted or may last.

- List persistence drivers and staged catalysts.
- If the current leader is already in extreme acceleration, state that the goal is lower-risk research discovery, not chasing the leader.

3. Map the diffusion path.

Use this sequence:

`leader -> same product -> same bottleneck -> upstream raw material/equipment -> downstream demand -> adjacent infrastructure -> pure concept`

4. Find candidates.

- First check local files: `config/trade_universe.toml`, `config/market_radar.toml`, `config/watchlist.toml`, and `config/external_signal_candidates.toml`.
- Then use current public sources for fresh market breadth,涨停复盘, company announcements, exchange filings, investor relations, and credible financial media.
- For HK names, also look for southbound flow, CCASS concentration/participant changes, public float, placement/rights issue risk, and order-book liquidity.

5. Filter out weak names.

Reject or downgrade candidates when:

- The exposure is only a media label and not in filings, annual reports, announcements, or credible company communication.
- The company has denied or materially weakened the core exposure.
- The stock already had several accelerated boards and no fresh divergence confirmation.
- Liquidity is too thin to exit.
- The rise depends mainly on rumor, stock-forum claims, or unverified screenshots.
- There is imminent dilution, major unlock, formal investigation, ST/*ST, suspension, audit uncertainty, or delisting risk.

6. Rank the remaining names.

Use the scoring model below.

## 100-Point Catch-Up Score

High score means `research priority`, not buy.

| Module | Weight | What to score |
| --- | ---: | --- |
| Theme persistence | 20 | Multi-day/month catalyst, price anchor, supply/demand proof, policy calendar |
| Exposure credibility | 20 | Direct product, capacity, customer validation, segment revenue, filing-backed evidence |
| Position advantage | 15 | Still lower consensus, not already extreme consensus, constructive base or first breakout |
| Volume/price confirmation | 15 | Volume expansion, relative strength, first board/strong close, divergence absorption |
| Diffusion fit | 10 | Clear place in leader -> same product -> upstream/downstream chain |
| Float/liquidity suitability | 10 | Moveable float but not unexitable; avoid HK empty-book traps |
| Risk cleanliness | 10 | No hard announcement/regulatory/liquidity/dilution red flags |

Score interpretation:

| Score | Label | Meaning |
| ---: | --- | --- |
| 0-49 | ignore | Weak or too speculative |
| 50-64 | watch | Track only |
| 65-74 | candidate | Daily follow-up |
| 75-84 | high attention | Strong research candidate; wait for confirmation |
| 85-100 | strong | Rare setup; still not a trade instruction |

## Risk Gate

Apply the risk gate after scoring.

| Gate | Trigger | Effect |
| --- | --- | --- |
| `pass` | No material red flag beyond volatility | Keep score label |
| `caution` | One non-fatal risk, weak evidence, mild overheat, stale data, or moderate liquidity issue | Keep label but disclose |
| `restricted` | Multiple independent risks, pure expectation without evidence, repeated clarifying denials, late acceleration, major unlock/reduction/dilution risk | Cap final label at `candidate` |
| `avoid` | Fraud/delisting/audit/suspension risk, ST/*ST, formal investigation, unexitable liquidity, severe weakening after regulatory warning, destructive financing risk | Force `avoid` |

## Confirmation Triggers

Use conditions instead of trade commands.

Good confirmation examples:

- Theme leader stays strong while the candidate starts volume expansion.
- Candidate breaks a base and closes near high with volume above the 20-day average.
- First board opens, absorbs supply, and reseals decisively.
- First major divergence closes above VWAP or a key level.
- Same-chain peers broaden from one leader to several names.
- Company filing or credible announcement improves exposure evidence.
- HK candidate shows real two-sided turnover and no hard placement/rights issue risk.

## Invalidation Triggers

Always write invalidation before upside imagination.

- Leader breaks down and same-theme breadth collapses.
- Candidate fails after first volume expansion and closes weak.
- Company denies the key exposure or says no revenue/order/qualification progress.
- Good news stops lifting the stock.
- Huge volume long upper shadow after a large rise.
- Regulatory inquiry, abnormal-move warning, reduction/unlock/dilution, suspension, audit, or delisting risk appears.
- HK CCASS concentration disperses after a large rise, or liquidity becomes one-sided.

## Output Format

Use this compact structure unless the user asks for a full report:

```markdown
**主线判断**
<theme and why it can/cannot keep running>

**扩散路径**
`leader -> same product -> same bottleneck -> upstream/downstream -> second-order -> concept proxy`

**候选池**
| 优先级 | 代码 | 名称 | 层级 | 状态 | 补涨分 | 风险门槛 | 关键依据 |
| --- | --- | --- | --- | --- | ---: | --- | --- |

**重点候选拆解**
- <symbol/name>: <why it is lower-position catch-up, what must confirm, what invalidates it>

**不要碰/降级**
- <symbol/name>: <reason>

**验证清单**
- <price/volume/theme/filing/liquidity checks>

**系统建议**
- 已在交易池: <symbols>
- 仅雷达/观察: <symbols>
- 池外候选: <symbols; add to external candidates or radar first>
```

## Example: Six Tungsten Hexafluoride Chain

Do not say `电子特气都该涨`. The real chain is:

`AI/HBM/3D NAND demand -> tungsten deposition process -> high-purity WF6 -> certification-gated domestic suppliers -> upstream tungsten/fluorine inputs -> industrial gas sentiment proxies`

The leader can keep moving when price, supply shock, scarce certified capacity, and staged policy/news catalysts remain active. Catch-up candidates should be separated as:

- Same product with capacity/revenue: stronger if already certified and selling.
- Trial production/verification: high expectation gap but high risk.
- Upstream tungsten/fluorine: only strong if pricing power or supply control improves.
- General industrial gas: mostly sentiment diffusion unless business exposure is proven.

## Local Investment System Integration

- If the candidate is in `config/trade_universe.toml`, it can be ranked by the normal investment workflow but remains subject to deterministic gates.
- If it is only in `config/market_radar.toml`, use it as theme confirmation, not an actionable recommendation.
- If it is outside all configs, propose adding it to `config/external_signal_candidates.toml` for research-only tracking before promotion.
- Do not modify configs unless the user explicitly asks to update the system.
- Existing cost, liquidity, action eligibility, risk-review, symbol-risk, and recommendation-only rules dominate this skill.
