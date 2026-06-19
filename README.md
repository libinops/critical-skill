# Critical Skill

> 让 LLM 闭嘴干活：拒绝谄媚、拒绝过度设计、拒绝无中生有。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
[![Cursor](https://img.shields.io/badge/Cursor-Rules-black)](https://docs.cursor.com/en/context/rules)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

基于李开复老师的反谄媚系统指令改造，为 Claude / Cursor 提供一套「**准确性重于认可**」的编码行为准则。强制模型标注证据来源、暴露隐含假设、要求可验证的成功标准——从根本上对抗 LLM 编程中的拍马屁、过度工程、虚构细节。

## 目录

- [它解决什么问题](#它解决什么问题)
- [核心特性](#核心特性)
- [安装](#安装)
- [效果对比](#效果对比)
- [原理：六类证据标签 + 五档置信度](#原理六类证据标签--五档置信度)
- [使用场景](#使用场景)
- [与其他方案的对比](#与其他方案的对比)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 它解决什么问题

LLM 写代码时有三类典型恶习：

1. **谄媚**：你写 `var`，它说「这个命名很好」；你问「这样写行吗」，它说「完全可以」——然后跑不起来。
2. **过度设计**：让你「为未来扩展」加抽象层、加配置项、加 fallback，三行需求写出三百行。
3. **虚构细节**：编造不存在的 API、库函数、引用、配置项，编得煞有介事。

这套 skill/rules 把反制机制写进系统指令，强制模型**先反驳、再回答、先标注、后下结论**。

## 核心特性

- **证据标签系统**：每条陈述必须打上 `[KNOWN]` / `[COMPUTED]` / `[INFERRED]` / `[COMMON]` / `[FRAME]` / `[GUESS]` 六类标签之一
- **置信度分级**：HIGH / MED / LOW / VERY LOW / UNKNOWN，未知即说「我不知道」
- **反谄媚信号检测**：自动识别并修剪「过于圆滑」「未经举证就妥协」的输出
- **事后诸葛亮检验**：发现事后自圆其说的解释时标记 `[INFERRED, post-hoc]`
- **零框架映射**：禁止把占星、MBTI 等符号框架直接翻译为医学/法律主张
- **精准修改原则**：禁止「顺手重构」「顺便优化」，代码改动严格匹配任务范围

## 安装

### Claude Skills（推荐）

将 `skills/critical/SKILL.md` 复制到 Claude 的 skills 目录：

```bash
# 项目级
mkdir -p .claude/skills/critical
cp skills/critical/SKILL.md .claude/skills/critical/SKILL.md

# 或用户级（影响所有项目）
mkdir -p ~/.claude/skills/critical
cp skills/critical/SKILL.md ~/.claude/skills/critical/SKILL.md
```

### Cursor Rules

将 `.cursor/rules/critical.md` 复制到项目根目录的 `.cursor/rules/`：

```bash
mkdir -p .cursor/rules
cp .cursor/rules/critical.md .cursor/rules/critical.md
```

或直接在 Cursor Settings → Rules 中粘贴内容。文件中 `alwaysApply: true` 会全局生效；如需按文件类型触发，改为 `globs` 模式。

### 自定义修改

所有规则都是纯文本 Markdown，直接编辑即可生效。建议修改前先读完 [SKILL.md](skills/critical/SKILL.md) 全文。

## 效果对比

**未启用 Critical Skill：**

> 用户：这样实现有问题吗？
>
> Claude：完全可以，这个实现非常优雅！建议再加一层抽象以方便未来扩展……

**启用 Critical Skill：**

> 用户：这样实现有问题吗？
>
> Claude：[INFERRED] 有两处问题：
> 1. 第 12 行的边界条件未处理，输入为负数时会越界
> 2. 「为未来扩展加抽象层」是过度设计（[COMMON] YAGNI 原则），当前需求不需要
>
> 置信度 MED。建议先加单测覆盖这两个场景再决定是否抽象。

## 原理：六类证据标签 + 五档置信度

| 标签 | 含义 | 示例 |
|---|---|---|
| `[KNOWN]` | 训练数据中的事实 | `Python 3.10 引入了 match 语句` |
| `[COMPUTED]` | 计算得出 | `O(n log n) 排序复杂度` |
| `[INFERRED]` | 演绎推理 | `基于现有代码风格推断的命名` |
| `[COMMON]` | 标准领域知识 | `HTTP 200 表示成功` |
| `[FRAME]` | 符号系统 | `MBTI 性格分类`（需声明非现实映射）|
| `[GUESS]` | 无根据的猜测 | 「应该用 Redis 缓存」 |

置信度上限：涉及现实的 `[FRAME]` 和 `[GUESS]` 不得超过 LOW。

完整定义见 [skills/critical/SKILL.md](skills/critical/SKILL.md)。

## 使用场景

- **Code Review**：避免 AI 帮你「美化」问题或无脑点赞
- **重构建议**：强制 AI 给出可验证的改动理由，不接受「看起来更优雅」
- **架构讨论**：阻止 AI 凭空推荐未经验证的技术栈
- **新人引导**：让 AI 回答时明确标注「这是常识」还是「我在猜」
- **写作辅助**：防止 AI 在长文里编造引用和数据

## 与其他方案的对比

| 方案 | 覆盖范围 | 强制力 | 可定制 | 学习成本 |
|---|---|---|---|---|
| **Critical Skill（本项目）** | 编码 + 通用回答 | 系统级 | 高（纯文本）| 低 |
| 通用「请直接回答」Prompt | 仅当前对话 | 用户级 | 中 | 低 |
| Anthropic Constitutional AI | 模型训练层 | 模型级 | 不可改 | 无 |
| 自写 Rules 散落各处 | 视实现而定 | 视实现而定 | 高 | 高 |

本项目优势：**把反谄媚和反过度设计做成可分发、可复用的系统级配置**，而不是每次手动输入 prompt。

## 常见问题

**Q：会和 Cursor/Claude 自带的规则冲突吗？**
A：不会。系统指令是叠加生效，冲突时按特异性排序。本 skill 设计为 `alwaysApply`，会覆盖同等粒度的通用规则。

**Q：会不会让 AI 变得太「冷」？**
A：不会。规则只禁止「无证据的赞美」和「无根据的自信」，有证据的肯定性表述仍然保留。

**Q：能用于非编码任务吗？**
A：可以。证据标签和置信度系统对所有需要严谨输出的场景都适用——写作、调研、决策分析等。

**Q：为什么不直接用英文？**
A：中文社区同样存在 LLM 谄媚问题（甚至更严重，因为文化语境下「附和」更自然）。中英双语底层逻辑一致。

## 贡献指南

欢迎 PR。重点欢迎：

- 新的反模式案例与反制规则
- 误用边界条件的测试用例
- 其他 LLM 平台（Codeium、Cody、Copilot）的适配版本
- 翻译（英文 README、Japanese 适配等）

提交前请确保：所有新规则都附带 [KNOWN] 证据或可复现的对话示例。

## 许可证

MIT License — 详见 [LICENSE](LICENSE) 文件。

## Star History

如果这个项目帮你少被 LLM 拍马屁、少写过度设计的代码，欢迎点个 Star 让更多人看到。

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/critical-skill&type=Date)](https://star-history.com/#YOUR_USERNAME/critical-skill)

---

## 关注我获取更多 LLM 编码实践

[](./img/mingpian.jpg)
