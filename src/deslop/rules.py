"""Rule packs for deslop.

Every rule is a regex plus a human explanation and, where it is safe, a
replacement. Rules are grouped by language and weighted by how strongly the
phrase signals machine-written prose.

Severity:
    3  strong tell   - the phrase almost never shows up in careful human writing
    2  medium tell   - common in generated copy, rare in plain speech
    1  mild tell     - fine once, suspicious when it repeats
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    """One detectable pattern."""

    id: str
    pattern: str
    severity: int
    message: str
    suggestion: str
    fix: str | None = None
    flags: int = re.IGNORECASE | re.MULTILINE
    lang: str = "en"

    def compile(self) -> re.Pattern[str]:
        return re.compile(self.pattern, self.flags)


def _r(rule_id, pattern, severity, message, suggestion, fix=None, flags=None, lang="en"):
    return Rule(
        id=rule_id,
        pattern=pattern,
        severity=severity,
        message=message,
        suggestion=suggestion,
        fix=fix,
        flags=re.IGNORECASE | re.MULTILINE if flags is None else flags,
        lang=lang,
    )


# ---------------------------------------------------------------------------
# English
# ---------------------------------------------------------------------------

ENGLISH_RULES = [
    # opener clichés
    _r("en.fast-paced", r"in today'?s (?:fast-paced|ever-changing|digital|modern) (?:world|era|age|landscape)",
       3, "opening cliché", "start with the actual subject", "Today"),
    _r("en.evolving-landscape", r"(?:ever[- ]evolving|rapidly evolving|constantly evolving) (?:landscape|world|field|space)",
       3, "generic evolution phrase", "say what changed and when", None),
    _r("en.in-the-realm", r"\bin the realm of\b", 3, "ornate filler", "say 'in' or drop the phrase", "in"),
    _r("en.in-a-world", r"\bin a world where\b", 3, "cinematic opener", "state the situation directly", None),
    _r("en.at-the-intersection", r"\bat the intersection of\b", 2, "conference-speak", "name the two things and their relation", None),
    _r("en.navigate-complexity", r"\bnavigat(?:e|ing) the (?:complexit|challeng|landscap)\w*", 2,
       "abstract difficulty talk", "describe the concrete problem", None),

    # verbs
    _r("en.delve", r"\bdelv(?:e|es|ed|ing)\s+(?:into|deeper)\b", 3, "'delve' is a strong tell",
       "write 'look at', 'read', 'dig into' or just start", "look into"),
    _r("en.dive-in", r"\blet'?s (?:dive in|dive into|unpack|break it down|explore)\b", 3,
       "stage-direction opener", "delete it and start with the content", None),
    _r("en.dive-deep", r"\bdive (?:deep|deeper) into\b", 2, "stock phrase", "use 'look at' or 'cover'", "look at"),
    _r("en.unlock", r"\bunlock(?:ing|s|ed)? (?:the )?(?:power|potential|value|insights?|secrets?)\b", 3,
       "marketing verb", "say what becomes possible", None),
    _r("en.unleash", r"\bunleash(?:ing|es|ed)?\b", 3, "marketing verb", "say what it does", None),
    _r("en.harness", r"\bharness(?:ing|es|ed)? the power of\b", 3, "marketing verb", "say what you use it for", None),
    _r("en.supercharge", r"\b(?:supercharge|skyrocket|turbocharge)\w*\b", 3, "hype verb", "give a number or drop it", None),
    _r("en.elevate", r"\belevat(?:e|ing|es) your\b", 3, "hype verb", "say what improves", None),
    _r("en.master-art", r"\bmaster(?:ing)? the art of\b", 3, "course-sales phrase", "say 'get good at'", None),
    _r("en.embark", r"\bembark(?:ing)? on (?:a|the|your) (?:journey|adventure|quest)\b", 3,
       "narrative filler", "say what you started", None),
    _r("en.pave-way", r"\bpav(?:e|es|ed|ing) the way\b", 2, "stock transition", "say what enabled what", None),
    _r("en.shed-light", r"\bshed(?:s|ding)? (?:light|new light) on\b", 2, "stock transition", "say 'shows' or 'explains'", None),
    _r("en.underscore", r"\bunderscore(?:s|d|ing)?\b", 2, "formal filler", "say 'shows' or 'stresses'", None),
    _r("en.catalyze", r"\bcataly[sz](?:e|es|ed|ing)\b", 2, "formal filler", "say 'caused'", None),

    # adjectives
    _r("en.cutting-edge", r"\b(?:cutting[- ]edge|state[- ]of[- ]the[- ]art|next[- ]generation|world[- ]class)\b", 2,
       "unsupported superlative", "say what is new about it", "recent"),
    _r("en.seamless", r"\bseamless\b", 2, "vague quality claim", "say what does not break", "smooth"),
    _r("en.seamlessly", r"\bseamlessly\b", 2, "vague quality claim", "say what does not break", "smoothly"),
    _r("en.robust", r"\brobust\b", 1, "vague quality claim", "say what it survives", None),
    _r("en.effortless", r"\beffortless(?:ly)?\b", 2, "vague quality claim", "say how long it takes", None),
    _r("en.pivotal", r"\b(?:pivotal|crucial|paramount|instrumental)\b", 1, "importance filler", "show why it matters", None),
    _r("en.meticulous", r"\bmeticulous(?:ly)?\b", 2, "decorative adverb", "describe the actual care", None),
    _r("en.multifaceted", r"\bmulti[- ]fac(?:eted|et)\b", 2, "abstract adjective", "list the facets", None),
    _r("en.holistic", r"\bholistic\b", 2, "consultant word", "say what it covers", None),
    _r("en.nuanced", r"\bnuanced\b", 1, "vague quality claim", "name the distinction", None),
    _r("en.vibrant", r"\bvibrant\b", 2, "travel-brochure word", "say what is happening", None),
    _r("en.bustling", r"\bbustling\b", 2, "travel-brochure word", "say what is happening", None),
    _r("en.nestled", r"\bnestled\b", 2, "travel-brochure word", "say where it is", None),
    _r("en.profound", r"\bprofound(?:ly)?\b", 1, "importance filler", "say what actually changed", None),
    _r("en.unwavering", r"\bunwavering\b", 2, "empty loyalty word", "give evidence", None),
    _r("en.unparalleled", r"\bunparalleled\b", 2, "unsupported superlative", "compare with something", None),

    # nouns
    _r("en.tapestry", r"\btapestry\b", 3, "'tapestry' is a meme", "say 'mix' or name the parts", None),
    _r("en.testament", r"\b(?:a )?testament to\b", 3, "essay-cliché", "say what proves it", None),
    _r("en.beacon", r"\bbeacon of\b", 3, "essay-cliché", "say what it does", None),
    _r("en.labyrinth", r"\blabyrinth(?:ine)?\b", 2, "ornate metaphor", "say 'complicated'", None),
    _r("en.plethora", r"\b(?:a )?(?:myriad|plethora|multitude) of\b", 2, "inflated quantity", "say 'many'", "many"),
    _r("en.game-changer", r"\bgame[- ]chang(?:er|ing)\b", 3, "hype phrase", "say what changes", None),
    _r("en.revolutionize", r"\brevolutioni[sz](?:e|es|ed|ing)\b", 3, "hype verb", "say what improves", None),
    _r("en.transformative", r"\btransformative\b", 2, "hype adjective", "say what changes", None),
    _r("en.paradigm", r"\bparadigm shift\b", 3, "consultant phrase", "say what changed", None),
    _r("en.synergy", r"\bsynerg(?:y|ies|istic)\b", 3, "consultant phrase", "say what combines well", None),
    _r("en.ecosystem", r"\b(?:rich|vibrant|thriving) (?:ecosystem|community)\b", 2, "generic praise", "name who is involved", None),
    _r("en.landscape-of", r"\bthe (?:landscape|world) of \w+", 2, "vague framing", "name the field directly", None),

    # connectors and structure
    _r("en.moreover", r"(?:^|[.!?]\s+)(?:Moreover|Furthermore|Additionally|Consequently),", 2,
       "essay connector at sentence start", "drop it or use a plain 'and'/'so'", None, flags=re.MULTILINE),
    _r("en.not-only", r"\bnot only\b[^.]{0,80}?\bbut also\b", 2, "balanced construction", "split into two sentences", None),
    _r("en.not-just", r"\b(?:it|this|that)(?:'s| is) not (?:just|only) (?:a |an |the )?[^.]{2,70}?[,;]\s*(?:it|this|that)(?:'s| is)\b",
       3, "'not just X, it's Y' pattern", "state the claim once", None),
    _r("en.heres-thing", r"\bhere'?s (?:the thing|the kicker|the deal|why)\b", 3, "blog-voice filler", "get to the point", None),
    _r("en.imagine", r"\bimagine (?:a |an |the )?(?:world|future|scenario)\b", 2, "rhetorical opener", "describe the case", None),
    _r("en.whether-you", r"\bwhether you'?re (?:a |an )?[^,]{2,40}(?:,\s*or| or )", 2,
       "audience-sweeping construction", "name one reader", None),
    _r("en.from-to", r"\bfrom (?:beginners?|newcomers?|hobbyists?) to (?:experts?|professionals?|veterans?)\b", 2,
       "audience-sweeping construction", "pick the reader", None),
    _r("en.in-conclusion", r"\b(?:in conclusion|to sum up|in summary|all in all)\b", 1, "essay closing", "end on a fact", None),
    _r("en.important-to-note", r"\bit(?:'s| is) (?:important|worth) (?:to note|noting) that\b", 2,
       "hedge opener", "delete it and state the fact", "Note: "),
    _r("en.at-the-end", r"\bat the end of the day\b", 2, "stock phrase", "say 'in practice'", None),
    _r("en.gone-are", r"\bgone are the days\b", 3, "stock phrase", "describe the change", None),
    _r("en.little-did", r"\blittle did (?:they|we|i) know\b", 3, "narrative cliché", "say what happened next", None),

    # filler words with safe replacements
    _r("en.utilize", r"\butili[sz](?:e|es|ed|ing)\b", 2, "inflated verb", "say 'use'", None),
    _r("en.leverage", r"\bleverag(?:e|es|ed|ing)\b", 2, "inflated verb", "say 'use'", None),
    _r("en.in-order-to", r"\bin order to\b", 1, "padding", "say 'to'", "to"),
    _r("en.due-to-fact", r"\bdue to the fact that\b", 2, "padding", "say 'because'", "because"),
    _r("en.at-this-point", r"\bat this (?:point in time|moment in time)\b", 2, "padding", "say 'now'", "now"),
    _r("en.in-the-event", r"\bin the event that\b", 1, "padding", "say 'if'", "if"),
    _r("en.prior-to", r"\bprior to\b", 1, "padding", "say 'before'", "before"),
    _r("en.subsequent-to", r"\bsubsequent to\b", 1, "padding", "say 'after'", "after"),
    _r("en.a-number-of", r"\ba (?:large )?number of\b", 1, "padding", "say 'many' or a figure", "many"),
    _r("en.it-should-be-noted", r"\bit should be noted that\b", 2, "hedge opener", "delete it", ""),
]

# ---------------------------------------------------------------------------
# Chinese
# ---------------------------------------------------------------------------

CHINESE_RULES = [
    _r("zh.suizhe", r"随着[^，。]{0,20}?(?:的)?(?:不断)?(?:发展|进步|普及|兴起|深入)", 2,
       "「随着…的发展」式开头", "直接说发生了什么", None, lang="zh"),
    _r("zh.zai-dangjin", r"在(?:当今|如今|当下)[^，。]{0,12}?(?:时代|社会|环境|背景)下?", 3,
       "「在当今…的时代」式开头", "直接从事实开始", None, lang="zh"),
    _r("zh.fuyu", r"赋能", 3, "「赋能」是重灾区", "用「帮助」「让…能」", "帮助", lang="zh"),
    _r("zh.zhuli", r"助力", 3, "「助力」是重灾区", "用「帮助」", "帮助", lang="zh"),
    _r("zh.dazao", r"打造", 2, "「打造」偏营销", "用「做」「建」", "做", lang="zh"),
    _r("zh.yizhanshi", r"一站式", 3, "「一站式」是套话", "说清楚包含哪些", "", lang="zh"),
    _r("zh.bihuan", r"闭环", 3, "「闭环」是套话", "说清流程起点终点", None, lang="zh"),
    _r("zh.zhuashou", r"抓手", 3, "「抓手」是套话", "说具体动作", None, lang="zh"),
    _r("zh.kelidu", r"颗粒度", 2, "「颗粒度」是套话", "说「多细」", None, lang="zh"),
    _r("zh.shendu", r"深度赋能|全方位赋能|多维度赋能", 3, "堆叠套话", "说清具体做了什么", None, lang="zh"),
    _r("zh.zhideyiti", r"值得一提的是[，,]?", 3, "「值得一提的是」是填充", "删掉直接说", "", lang="zh"),
    _r("zh.xuyaozhuyi", r"需要注意的是[，,]?", 2, "填充语", "删掉直接说", "", lang="zh"),
    _r("zh.bukefouren", r"不可否认的是[，,]?|毋庸置疑[，,]?|显而易见[，,]?", 3, "空洞强调", "删掉，直接给依据", "", lang="zh"),
    _r("zh.zhongsuo", r"(?:综上所述|总而言之|总的来说)[，,]", 2, "作文式收尾", "用一句事实收尾", "总之，", lang="zh"),
    _r("zh.zhongsuozhi", r"众所周知[，,]?", 3, "「众所周知」通常是废话", "删掉并给出处", "", lang="zh"),
    _r("zh.zhongyaoyiyi", r"具有(?:重要|深远)意义|起着?(?:至关重要|重要)的作用|发挥着重要作用", 3,
       "「具有重要意义」是空话", "说清带来了什么变化", None, lang="zh"),
    _r("zh.youxiao", r"(?:有效|显著|大幅|极大)(?:地)?(?:提升|提高|改善|增强)", 2,
       "无数据的效果描述", "给出数字或删掉", None, lang="zh"),
    _r("zh.dianjiding", r"为[^，。]{2,20}?(?:奠定|提供)(?:了)?(?:坚实|有力|强有力)?(?:的)?(?:基础|支撑|保障)", 3,
       "官方稿句式", "直接说做了什么", None, lang="zh"),
    _r("zh.youci", r"(?:由此可见|由此可知|据此可见)[，,]", 2, "作文式过渡", "直接给结论", None, lang="zh"),
    _r("zh.womenkeyi", r"我们可以看到|我们不难发现|笔者认为", 2, "论文腔", "直接陈述", None, lang="zh"),
    _r("zh.rangwomen", r"让我们一起|让我们来(?:看看|了解|探索)", 2, "导游腔", "直接进入内容", None, lang="zh"),
    _r("zh.xinxi", r"在这个(?:信息爆炸|数字化|智能化|快节奏)的?(?:时代|社会)", 3, "时代开场白", "直接从问题开始", None, lang="zh"),
    _r("zh.keji", r"(?:随着)?(?:科技的|技术的)?(?:飞速|快速|迅猛)发展", 2, "时代开场白", "直接说变化", None, lang="zh"),
    _r("zh.buji", r"不仅[^，。]{0,30}?而且[^，。]{0,30}?更", 2, "排比递进", "拆成两句", None, lang="zh"),
    _r("zh.yifangmian", r"一方面[^，。]{0,40}?另一方面", 2, "两面说法", "只保留真的那一面", None, lang="zh"),
    _r("zh.yuelaiyue", r"越来越多的|日益增长|不断涌现|层出不穷", 2, "模糊量词", "给数字或例子", None, lang="zh"),
    _r("zh.beishou", r"备受关注|引起了?广泛(?:关注|讨论)|引发热议", 3, "新闻套话", "说清楚谁在讨论什么", None, lang="zh"),
    _r("zh.shengtai", r"生态(?:圈|体系|闭环)?|全链路|端到端", 2, "行业黑话", "说清具体范围", None, lang="zh"),
    _r("zh.changjing", r"场景化|落地|沉淀|复用", 2, "行业黑话", "说具体做了什么", None, lang="zh"),
    _r("zh.jiangben", r"降本增效|提质增效|提效降本", 3, "行业黑话", "给出前后对比", None, lang="zh"),
    _r("zh.dapo", r"打破[^，。]{0,10}?(?:壁垒|边界|瓶颈)|注入(?:新的)?(?:动力|活力)|焕发(?:新的)?(?:生机|活力)", 3,
       "堆砌动词", "说具体结果", None, lang="zh"),
    _r("zh.hexin", r"核心竞争力|底层逻辑|方法论", 2, "行业黑话", "说清楚是什么", None, lang="zh"),
    _r("zh.shouxian", r"首先[，,][^。]{0,80}?其次[，,]", 2, "作文式排列", "用小标题或直接叙述", None, lang="zh"),
    _r("zh.zhongdian", r"重点(?:在于|是)[，,]?", 1, "填充", "删掉直接说", None, lang="zh"),
    _r("zh.zhide", r"值得(?:我们)?(?:深思|思考|关注)", 2, "空泛呼吁", "给出你的判断", None, lang="zh"),
    _r("zh.tigao", r"为用户提供了?[^，。]{0,20}?(?:体验|价值|便利)", 2, "泛化价值陈述", "说清哪一步变快了", None, lang="zh"),
]

ALL_RULES = ENGLISH_RULES + CHINESE_RULES

RULES_BY_ID = {rule.id: rule for rule in ALL_RULES}

FIXABLE = [rule for rule in ALL_RULES if rule.fix is not None]

