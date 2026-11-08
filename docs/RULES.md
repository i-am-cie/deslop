# Rule reference

106 rules: 70 English, 36 Chinese, 26 with a safe rewrite.

Severity 3 = the phrase almost never appears in careful human writing,
2 = common in generated copy, 1 = fine once but suspicious when it repeats.

| Rule | Lang | Sev | What it flags | Fix (safe) |
| --- | --- | --- | --- | --- |
| `en.fast-paced` | en | 3 | opening cliché | `Today` |
| `en.evolving-landscape` | en | 3 | generic evolution phrase | - |
| `en.in-the-realm` | en | 3 | ornate filler | `in` |
| `en.in-a-world` | en | 3 | cinematic opener | - |
| `en.at-the-intersection` | en | 2 | conference-speak | - |
| `en.navigate-complexity` | en | 2 | abstract difficulty talk | - |
| `en.delve` | en | 3 | 'delve' is a strong tell | `look into` |
| `en.dive-in` | en | 3 | stage-direction opener | - |
| `en.dive-deep` | en | 2 | stock phrase | `look at` |
| `en.unlock` | en | 3 | marketing verb | - |
| `en.unleash` | en | 3 | marketing verb | - |
| `en.harness` | en | 3 | marketing verb | - |
| `en.supercharge` | en | 3 | hype verb | - |
| `en.elevate` | en | 3 | hype verb | - |
| `en.master-art` | en | 3 | course-sales phrase | - |
| `en.embark` | en | 3 | narrative filler | - |
| `en.pave-way` | en | 2 | stock transition | - |
| `en.shed-light` | en | 2 | stock transition | - |
| `en.underscore` | en | 2 | formal filler | - |
| `en.catalyze` | en | 2 | formal filler | - |
| `en.cutting-edge` | en | 2 | unsupported superlative | `recent` |
| `en.seamless` | en | 2 | vague quality claim | `smooth` |
| `en.seamlessly` | en | 2 | vague quality claim | `smoothly` |
| `en.robust` | en | 1 | vague quality claim | - |
| `en.effortless` | en | 2 | vague quality claim | - |
| `en.pivotal` | en | 1 | importance filler | - |
| `en.meticulous` | en | 2 | decorative adverb | - |
| `en.multifaceted` | en | 2 | abstract adjective | - |
| `en.holistic` | en | 2 | consultant word | - |
| `en.nuanced` | en | 1 | vague quality claim | - |
| `en.vibrant` | en | 2 | travel-brochure word | - |
| `en.bustling` | en | 2 | travel-brochure word | - |
| `en.nestled` | en | 2 | travel-brochure word | - |
| `en.profound` | en | 1 | importance filler | - |
| `en.unwavering` | en | 2 | empty loyalty word | - |
| `en.unparalleled` | en | 2 | unsupported superlative | - |
| `en.tapestry` | en | 3 | 'tapestry' is a meme | - |
| `en.testament` | en | 3 | essay-cliché | - |
| `en.beacon` | en | 3 | essay-cliché | - |
| `en.labyrinth` | en | 2 | ornate metaphor | - |
| `en.plethora` | en | 2 | inflated quantity | `many` |
| `en.game-changer` | en | 3 | hype phrase | - |
| `en.revolutionize` | en | 3 | hype verb | - |
| `en.transformative` | en | 2 | hype adjective | - |
| `en.paradigm` | en | 3 | consultant phrase | - |
| `en.synergy` | en | 3 | consultant phrase | - |
| `en.ecosystem` | en | 2 | generic praise | - |
| `en.landscape-of` | en | 2 | vague framing | - |
| `en.moreover` | en | 2 | essay connector at sentence start | - |
| `en.not-only` | en | 2 | balanced construction | - |
| `en.not-just` | en | 3 | 'not just X, it's Y' pattern | - |
| `en.heres-thing` | en | 3 | blog-voice filler | - |
| `en.imagine` | en | 2 | rhetorical opener | - |
| `en.whether-you` | en | 2 | audience-sweeping construction | - |
| `en.from-to` | en | 2 | audience-sweeping construction | - |
| `en.in-conclusion` | en | 1 | essay closing | - |
| `en.important-to-note` | en | 2 | hedge opener | `Note: ` |
| `en.at-the-end` | en | 2 | stock phrase | - |
| `en.gone-are` | en | 3 | stock phrase | - |
| `en.little-did` | en | 3 | narrative cliché | - |
| `en.utilize` | en | 2 | inflated verb | - |
| `en.leverage` | en | 2 | inflated verb | - |
| `en.in-order-to` | en | 1 | padding | `to` |
| `en.due-to-fact` | en | 2 | padding | `because` |
| `en.at-this-point` | en | 2 | padding | `now` |
| `en.in-the-event` | en | 1 | padding | `if` |
| `en.prior-to` | en | 1 | padding | `before` |
| `en.subsequent-to` | en | 1 | padding | `after` |
| `en.a-number-of` | en | 1 | padding | `many` |
| `en.it-should-be-noted` | en | 2 | hedge opener | (delete) |
| `zh.suizhe` | zh | 2 | 「随着…的发展」式开头 | - |
| `zh.zai-dangjin` | zh | 3 | 「在当今…的时代」式开头 | - |
| `zh.fuyu` | zh | 3 | 「赋能」是重灾区 | `帮助` |
| `zh.zhuli` | zh | 3 | 「助力」是重灾区 | `帮助` |
| `zh.dazao` | zh | 2 | 「打造」偏营销 | `做` |
| `zh.yizhanshi` | zh | 3 | 「一站式」是套话 | (delete) |
| `zh.bihuan` | zh | 3 | 「闭环」是套话 | - |
| `zh.zhuashou` | zh | 3 | 「抓手」是套话 | - |
| `zh.kelidu` | zh | 2 | 「颗粒度」是套话 | - |
| `zh.shendu` | zh | 3 | 堆叠套话 | - |
| `zh.zhideyiti` | zh | 3 | 「值得一提的是」是填充 | (delete) |
| `zh.xuyaozhuyi` | zh | 2 | 填充语 | (delete) |
| `zh.bukefouren` | zh | 3 | 空洞强调 | (delete) |
| `zh.zhongsuo` | zh | 2 | 作文式收尾 | `总之，` |
| `zh.zhongsuozhi` | zh | 3 | 「众所周知」通常是废话 | (delete) |
| `zh.zhongyaoyiyi` | zh | 3 | 「具有重要意义」是空话 | - |
| `zh.youxiao` | zh | 2 | 无数据的效果描述 | - |
| `zh.dianjiding` | zh | 3 | 官方稿句式 | - |
| `zh.youci` | zh | 2 | 作文式过渡 | - |
| `zh.womenkeyi` | zh | 2 | 论文腔 | - |
| `zh.rangwomen` | zh | 2 | 导游腔 | - |
| `zh.xinxi` | zh | 3 | 时代开场白 | - |
| `zh.keji` | zh | 2 | 时代开场白 | - |
| `zh.buji` | zh | 2 | 排比递进 | - |
| `zh.yifangmian` | zh | 2 | 两面说法 | - |
| `zh.yuelaiyue` | zh | 2 | 模糊量词 | - |
| `zh.beishou` | zh | 3 | 新闻套话 | - |
| `zh.shengtai` | zh | 2 | 行业黑话 | - |
| `zh.changjing` | zh | 2 | 行业黑话 | - |
| `zh.jiangben` | zh | 3 | 行业黑话 | - |
| `zh.dapo` | zh | 3 | 堆砌动词 | - |
| `zh.hexin` | zh | 2 | 行业黑话 | - |
| `zh.shouxian` | zh | 2 | 作文式排列 | - |
| `zh.zhongdian` | zh | 1 | 填充 | - |
| `zh.zhide` | zh | 2 | 空泛呼吁 | - |
| `zh.tigao` | zh | 2 | 泛化价值陈述 | - |

Rules with a fix are applied by `deslop fix`; the rest are reported and left to you.