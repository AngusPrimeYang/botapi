"""外商面試英文搭配庫。用日期種子抽樣，不必另存「用過哪些」狀態。"""

from __future__ import annotations

import datetime
import random
from dataclasses import dataclass

START_DATE = datetime.date(2026, 1, 1)
SHUFFLE_SEED = 2026
PICKS_PER_DAY = 2

SCENARIOS = (
    "STAR / 專案介紹：說明你如何主導或推進一個專案",
    "System design：討論架構取捨與技術決策",
    "跨團隊衝突：溝通、對齊、化解分歧",
    "線上事故 / 除錯：事發、止血、復盤",
    "交付與排期：scope、deadline、品質取捨",
    "談薪與職級：compensation、scope、expectation",
    "Leadership / mentoring：帶人、授權、課責",
)

# 核心字 -> 面試常用搭配。同一字在詞庫輪完一圈後，才換下一條搭配。
COLLOCATIONS: dict[str, tuple[str, ...]] = {
    "own": (
        "own the outcome",
        "take ownership of the incident",
        "own the technical decision",
        "own the follow-up",
    ),
    "align": (
        "align with stakeholders",
        "get alignment before we commit",
        "align on the trade-off",
        "drive alignment across teams",
    ),
    "trade-off": (
        "make an explicit trade-off",
        "trade-off between latency and cost",
        "document the trade-off",
        "accept the trade-off for now",
    ),
    "escalate": (
        "escalate early",
        "escalate with options",
        "know when to escalate",
        "escalate the risk, not the blame",
    ),
    "delegate": (
        "delegate the implementation",
        "delegate with clear ownership",
        "delegate but stay accountable",
        "decide what not to delegate",
    ),
    "bottleneck": (
        "identify the bottleneck",
        "remove the bottleneck",
        "the database was the bottleneck",
        "avoid becoming the bottleneck",
    ),
    "latency": (
        "reduce p99 latency",
        "latency versus throughput",
        "hide latency from the user",
        "latency budget",
    ),
    "throughput": (
        "increase throughput",
        "throughput dropped under load",
        "optimize for throughput",
        "throughput versus cost",
    ),
    "scope": (
        "cut scope to hit the date",
        "scope creep",
        "negotiate the scope",
        "keep the scope explicit",
    ),
    "stakeholder": (
        "keep stakeholders informed",
        "conflicting stakeholder priorities",
        "bring stakeholders along",
        "manage stakeholder expectations",
    ),
    "mitigate": (
        "mitigate the risk",
        "mitigate the blast radius",
        "mitigate impact on users",
        "we couldn't eliminate it, but we mitigated it",
    ),
    "triage": (
        "triage incoming issues",
        "triage by user impact",
        "during triage we paused deploys",
        "triage first, then deep-dive",
    ),
    "rollback": (
        "rollback as the default",
        "a one-click rollback",
        "we rolled back within minutes",
        "feature flags made rollback cheap",
    ),
    "regression": (
        "caught the regression in staging",
        "avoid shipping a regression",
        "a performance regression",
        "regression tests around the incident",
    ),
    "impact": (
        "quantify the impact",
        "high-impact, low-effort",
        "business impact, not just technical elegance",
        "my impact on the team's delivery",
    ),
    "leverage": (
        "leverage existing infrastructure",
        "leverage the incident as a learning opportunity",
        "where I can leverage my strengths",
        "leverage the platform instead of rebuilding",
    ),
    "bandwidth": (
        "I don't have the bandwidth this quarter",
        "protect the team's bandwidth",
        "bandwidth for exploratory work",
        "that's outside my current bandwidth",
    ),
    "accountability": (
        "clear accountability",
        "accountability without blame",
        "I held myself accountable",
        "shared accountability across teams",
    ),
    "buy-in": (
        "get buy-in from leadership",
        "earn buy-in, don't demand it",
        "we didn't have buy-in yet",
        "technical buy-in from the team",
    ),
    "clarify": (
        "clarify the requirements",
        "clarify who owns the decision",
        "clarify the success metric",
        "I asked clarifying questions",
    ),
    "prioritize": (
        "prioritize by user impact",
        "re-prioritize when the data changed",
        "help the team prioritize",
        "prioritize ruthlessly",
    ),
    "compromise": (
        "a pragmatic compromise",
        "compromise on the timeline, not on safety",
        "we reached a compromise",
        "compromise that we could revisit",
    ),
    "push back": (
        "push back on unrealistic dates",
        "push back with data",
        "I pushed back, then offered options",
        "know how to push back professionally",
    ),
    "consensus": (
        "we don't need full consensus",
        "consensus was slowing us down",
        "seek consensus on the problem, not the solution",
        "disagree and commit after consensus failed",
    ),
    "iterate": (
        "iterate with users",
        "ship a thin slice and iterate",
        "iterate on the API design",
        "I'd iterate rather than big-bang rewrite",
    ),
    "ship": (
        "ship behind a flag",
        "ship a vertical slice",
        "bias toward shipping",
        "what blocked us from shipping",
    ),
    "estimate": (
        "give a range, not a false-precise estimate",
        "estimate with unknowns called out",
        "my estimate was wrong, here's what I learned",
        "re-estimate after the spike",
    ),
    "decouple": (
        "decouple the services",
        "decouple deploy from release",
        "decouple teams with a stable API",
        "we decoupled the billing path",
    ),
    "resilient": (
        "make the system more resilient",
        "resilient to downstream timeouts",
        "resilient retries with backoff",
        "resilient, not just redundant",
    ),
    "degrade": (
        "fail gracefully / degrade gracefully",
        "degrade non-critical features first",
        "the search degraded to a simpler ranking",
        "degrade rather than go fully down",
    ),
    "incident": (
        "during the incident",
        "incident commander",
        "declare an incident early",
        "incident communication to stakeholders",
    ),
    "root cause": (
        "the root cause was a bad config",
        "don't stop at the first root cause",
        "root-cause analysis",
        "we fixed the symptom before the root cause",
    ),
    "postmortem": (
        "a blameless postmortem",
        "action items from the postmortem",
        "the postmortem changed how we deploy",
        "write the postmortem while it's fresh",
    ),
    "hotfix": (
        "ship a hotfix",
        "hotfix versus a proper fix",
        "the hotfix bought us time",
        "hotfix behind extra monitoring",
    ),
    "compensation": (
        "total compensation",
        "compensation aligned with scope",
        "how compensation is structured",
        "I'm looking for compensation that reflects",
    ),
    "expectation": (
        "set expectations early",
        "misaligned expectations",
        "reset expectations with data",
        "expectations for this level",
    ),
    "influence": (
        "influence without authority",
        "influence the technical direction",
        "I influenced the decision by",
        "influence through working demos",
    ),
    "mentor": (
        "mentor junior engineers",
        "I was mentored on",
        "mentoring through code review",
        "scale myself by mentoring",
    ),
    "facilitate": (
        "facilitate the design review",
        "facilitate a difficult discussion",
        "facilitate, not dominate",
        "I facilitated alignment between",
    ),
    "articulate": (
        "articulate the trade-off",
        "articulate the customer problem",
        "articulate why this is urgent",
        "I struggled to articulate, so I used a diagram",
    ),
    "quantify": (
        "quantify the risk",
        "quantify the performance win",
        "if I can't quantify it, I say so",
        "quantify in user terms",
    ),
    "socialize": (
        "socialize the proposal",
        "socialize the design before the meeting",
        "I socialized it with the on-call team",
        "socialize early to avoid surprises",
    ),
    "handoff": (
        "clean handoff to the next owner",
        "handoff notes for on-call",
        "the handoff was the actual bug",
        "reduce handoff cost between teams",
    ),
    "constraint": (
        "work within the constraint",
        "the real constraint was people, not CPUs",
        "make the constraint explicit",
        "design for the constraint we have",
    ),
    "capacity": (
        "capacity planning",
        "we ran out of capacity",
        "leave spare capacity for incidents",
        "team capacity versus roadmap ambition",
    ),
    "idempotent": (
        "make the API idempotent",
        "retries only work if it's idempotent",
        "idempotent payments",
        "the job wasn't idempotent, so it double-charged",
    ),
    "reproduce": (
        "reproduce it locally",
        "couldn't reproduce in staging",
        "a reliable way to reproduce",
        "reproduce with production-like load",
    ),
    "over-communicate": (
        "over-communicate during an incident",
        "I'd rather over-communicate than go dark",
        "over-communicate status to stakeholders",
        "over-communicate the risk, not the panic",
    ),
}


@dataclass(frozen=True)
class CollocationPick:
    word: str
    collocation: str


@dataclass(frozen=True)
class DailyTarget:
    scenario: str
    picks: tuple[CollocationPick, ...]

    def prompt_block(self) -> str:
        lines = [
            f"今天面試情境：{self.scenario}",
            "今天指定關鍵單字與搭配（必須使用，不可自行替換成其他常見說法）：",
        ]
        for i, pick in enumerate(self.picks, 1):
            lines.append(f"{i}. 單字：{pick.word}；指定搭配：{pick.collocation}")
        lines.append(
            "【關鍵單字】必須剛好是上述這些字，並解釋指定搭配、常見搭配對象與使用時機，"
            "不要只給字典定義。"
        )
        lines.append(
            "金句必須自然嵌入這些搭配；允許時態與人稱變化，但不可改寫成其他同義片語。"
        )
        return "\n".join(lines)


def _shuffled_words() -> list[str]:
    words = list(COLLOCATIONS.keys())
    rng = random.Random(SHUFFLE_SEED)
    rng.shuffle(words)
    return words


def pick_daily_target(
    today: datetime.date | None = None,
    n: int = PICKS_PER_DAY,
) -> DailyTarget:
    """依日期取出當天的情境、單字與搭配。同一天重跑結果相同。"""
    if n < 1:
        raise ValueError("n must be >= 1")

    today = today or datetime.date.today()
    words = _shuffled_words()
    day_index = (today - START_DATE).days
    if day_index < 0:
        day_index = 0

    start = (day_index * n) % len(words)
    selected = [words[(start + i) % len(words)] for i in range(n)]
    cycle = (day_index * n) // len(words)

    picks = tuple(
        CollocationPick(word=word, collocation=COLLOCATIONS[word][cycle % len(COLLOCATIONS[word])])
        for word in selected
    )
    scenario = SCENARIOS[day_index % len(SCENARIOS)]
    return DailyTarget(scenario=scenario, picks=picks)
