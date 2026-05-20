# 研究ワークフローと配置責務の再設計

- Date: 2026-05-20
- Status: design for review
- Scope: `research` / `creating-propositions` の責務境界、研究開始フェーズ、canonical generated project layout、旧構造削除

## 背景

現行の `research` は proposition-first protocol としては強いが、Agent が研究を開始するための作業手順になっていない。実際の入口は「命題がある」ではなく、「やりたいことがある」である。

現行フローは概ね次の形になっている。

```text
命題の生成
-> research lifecycle
-> derived hypothesis
-> plan
-> execution
-> result analysis
```

この構造では、命題の前に必要な作業が抜ける。

- やりたいことを研究可能な入口へ整える
- preliminary / scoping literature scan を行う
- 既存研究、既存手法、比較対象、既存データ、既知の失敗を把握する
- データや材料を取得する
- EDA / observation discovery で観察材料を作る
- その観察から命題を生成、分割、管理する

結果として、Agent は「材料不足です」と止まるか、薄い命題を作って走り始めやすい。

## 外部基準

一般的な研究・データ分析の流れは、研究開始時の調査と観察を研究本体の一部として扱う。

- University of Manitoba の research lifecycle は、planning から creation, dissemination, preservation, re-use までを研究活動として扱い、planning 段階に scholarship / data 探索を含めている。
- UW-Madison Writing Center の literature review guide は、文献レビューを既存研究の傾向、方法上の欠陥、理論や結果の矛盾、研究 gap を評価する作業として説明している。
- NIST/SEMATECH EDA handbook は、EDA をデータへの insight、構造、外れ値、仮定、簡潔なモデルを得るための分析アプローチとして置く。

参考:

- https://umanitoba.ca/libraries/research-lifecycle-um
- https://writing.wisc.edu/handbook/reviewofliterature/
- https://www.nist.gov/publications/nistsematech-e-handbook-statistical-methods-chapter-1-exploratory-data-analysis

## 問題

### 1. スキルが Agent workflow ではなく規約集になっている

現行文書は contract、protocol、status、claim structure が中心で、Agent が何をすればよいかが弱い。

必要なのは次の指示である。

- 最初に何を読むか
- 何を調べるか
- 何を作るか
- どこに置くか
- 何が揃ったら次へ進むか
- 材料不足なら何を集めるか

contract は必要だが、workflow の補助物である。主役ではない。

### 2. 研究開始フェーズがない

`research` は `Situation question -> observation / analysis -> proposition` から始まるが、Situation question を observation に変換する作業がない。

`creating-propositions` は材料がなければ命題を作らないが、その材料をどう集めるかは所有していない。

### 3. 文献調査が仮説 plan 側に偏っている

現行の `literature_review.md` は plan-scoped paper survey と prior-work grounding を要求する。これは仮説に関連する文献調査として正しい。

ただし、研究開始時の scoping literature scan とは別である。scoping は「このやりたいことは既に解かれているか」「どの研究系譜に属するか」「どの gap や comparator があるか」を見る作業で、命題生成の前に必要である。

### 4. 配置 source of truth が分散している

現行では README、AGENTS.md、`research/SKILL.md`、template、script、tests がそれぞれ配置や旧 path に触れている。さらに `new_project.py` は `lib/`, `data/`, `literature/` を常に作る一方、README はそれらを任意と説明している。

AGENTS.md はこの repository で作業する Agent のメタルールであり、生成研究プロジェクトの成果物配置を所有すべきではない。

### 5. 旧構造が残っている

互換性は不要である。旧情報は移行案内ではなく削除対象にする。

削除対象:

- `plans/`
- top-level `experiments/<id>/runs/`
- `literature/differentiation.md`
- purpose / trial / standalone plan 前提
- proposition-first 以前の説明、fixture、examples

旧 path をテストに残す場合は、「拒否されるべき旧 path」としてだけ残す。

## 設計目標

- `research` を研究全体の Agent workflow 司令塔にする。
- `creating-propositions` を命題の生成と管理の所有者にする。
- 研究開始フェーズを lifecycle 本体に含める。
- scoping literature と hypothesis-specific literature grounding を分ける。
- generated project layout の source of truth を `research` skill 側に一本化する。
- 旧構造との互換性を切り、古い path / 用語 / fixture を削除する。
- `AGENTS.md` は repo 作業ルールに限定する。

## 非目標

- 旧 `plans/` 構造の移行サポート。
- 旧 path を受け入れる compatibility shim。
- 既存プロジェクトの自動 migration script。
- 文献調査を網羅的 systematic review にすること。
- EDA だけで claim を作ること。

## 新しい全体像

`research` の lifecycle は、命題からではなく intent から始まる。

```text
Research intent / やりたいこと
-> Intake
-> Scoping literature scan
-> Existing work map / gap / comparator / dataset candidates
-> Material and data acquisition
-> EDA / observation discovery
-> creating-propositions
-> Hypothesis lifecycle loop
-> Report / related work / state update
```

仮説単位の詳細 loop は維持する。

```text
Proposition
-> Derived hypothesis
-> Hypothesis-specific prior-work grounding
-> Plan
-> Plan review
-> Execution
-> Result analysis
-> Hypothesis state update
-> Proposition state update through creating-propositions
```

## 責務分割

### `research`

`research` は研究プログラム全体の司令塔である。

所有するもの:

- research intent からの開始
- intake
- scoping literature scan の実行指示
- material / data acquisition の指示
- EDA / observation discovery の指示
- `creating-propositions` 呼び出し
- hypothesis lifecycle の orchestration
- plan review / execution / result analysis / reporting の orchestration
- generated project layout の canonical reference

`research` は命題 state machine の詳細を所有しない。

### `creating-propositions`

`creating-propositions` は命題の生成と管理を所有する。

所有するもの:

- 観察、既存研究、EDA 結果から命題を作る
- 命題を split / merge / park / kill / revise / close する
- 命題間の関係と状態を管理する
- 命題 decisions を記録する
- hypothesis lifecycle に渡せる命題を選別する
- derived hypothesis candidate の候補管理

所有する path:

```text
propositions/Pxxx_slug/proposition.md
propositions/Pxxx_slug/observations.md
propositions/Pxxx_slug/analyses.md
propositions/Pxxx_slug/decisions.md
```

所有しないもの:

```text
propositions/Pxxx_slug/hypotheses/Hxxx_slug/*
```

derived hypothesis の正式 plan、実験、runs、reports は `research` 側の hypothesis lifecycle が所有する。

### `research-plan-review`

plan 実行前の独立レビューを所有する。入力は plan path のみ。

### `research-result-analysis`

実行後の結果説明を所有する。最終 claim や state decision は選ばない。

### `quant-research`

統計・時系列・複数検定・leakage・robustness の domain extension として維持する。layout や state ownership は再定義しない。

## Canonical Generated Project Layout

新しい generated project layout は次を source of truth とする。

```text
{project-root}/
├── README.md
├── project_state.md
├── decisions.md
├── intake.md
├── literature/
│   ├── scoping.md
│   ├── papers.md
│   └── positioning.md
├── data/
│   ├── raw/
│   ├── processed/
│   └── eda/
├── observations.md
├── lib/
│   ├── data/
│   ├── eval/
│   ├── viz/
│   ├── utils/
│   └── tests/
└── propositions/
    └── P001_slug/
        ├── proposition.md
        ├── observations.md
        ├── analyses.md
        ├── decisions.md
        └── hypotheses/
            └── H001_slug/
                ├── hypothesis.md
                ├── plan.md
                ├── experiments/
                │   ├── code/
                │   ├── configs/
                │   ├── notebooks/
                │   └── runs/
                ├── reports/
                └── decisions.md
```

### Root-level files

- `intake.md`: やりたいこと、目的、制約、利用可能な材料、未取得材料、初期判断。
- `literature/scoping.md`: 初期文献調査。既存系譜、既存手法、既存 dataset / benchmark / comparator、明確な gap、除外した近接研究。
- `literature/papers.md`: project-level に参照した prior work の annotated list。
- `literature/positioning.md`: この project が既存研究上どこに立つか。plan-specific な Citation-use map ではない。
- `data/eda/`: hypothesis 前の探索的分析 artifact。ここに置く artifact は claim-bearing ではない。
- `observations.md`: proposition に分割される前の project-level observation backlog。

### Proposition-level files

`creating-propositions` が所有する。root-level observation や scoping literature から proposition-specific に切り出された材料を保持する。

### Hypothesis-level files

`research` の hypothesis lifecycle が所有する。plan-scoped literature grounding、runs、reports、claims はここに入る。

## 文献調査の二層化

### Scoping literature scan

実施タイミング:

- research intent の直後
- data / material acquisition の前
- EDA の前または並行
- 命題生成の前

目的:

- やりたいことが既に解かれていないかを確認する
- 研究系譜、既存手法、既存 dataset / benchmark / comparator を把握する
- gap、矛盾、未解決点、再現不能点、弱い comparator を見つける
- EDA で見るべき変数、失敗例、観測対象を決める

成果物:

```text
literature/scoping.md
literature/papers.md
literature/positioning.md
intake.md updates
observations.md entries
```

### Hypothesis-specific prior-work grounding

実施タイミング:

- derived hypothesis があり、plan を書く前

目的:

- その仮説の method choice、controls、comparators、evaluation protocol、known limitations、claim scope を grounding する

成果物:

```text
propositions/Pxxx_slug/hypotheses/Hxxx_slug/plan.md
  ## Prior-work grounding
  ### Survey evidence
  ### Citation-use map
```

この二つは代替不可である。scoping があるから plan grounding を省略してよい、または plan grounding があるから scoping を省略してよい、とはしない。

## EDA の扱い

EDA は命題前の観察生成フェーズとして research lifecycle 本体に含める。

EDA の成果物は `data/eda/` と root `observations.md` に置く。命題が生成された後に proposition-specific な観察へ切り出す。

EDA から得た pattern は exploratory observation であり、claim ではない。claim-bearing にするには、後続の hypothesis lifecycle で plan、review、execution、result analysis を通す。

## Skill 文書の再構成

### `skills/research/SKILL.md`

中心を Agent workflow にする。

残すもの:

- short lifecycle
- which reference to read when
- next action rules
- handoff to `creating-propositions`
- handoff to plan review / result analysis

移すもの:

- detailed proposition state machine は `creating-propositions` へ
- generated project layout details は `references/project_layout.md` へ
- literature detail は `references/literature_review.md` へ
- analysis detail は `references/analysis.md` へ

### `skills/creating-propositions/SKILL.md`

命題 workspace owner に変える。

追加する責務:

- proposition state management
- split / merge / park / close / revise
- proposition decisions
- root observations から proposition observations への切り出し
- plan-ready proposition の選別

削る責務:

- 「正式 state は research に渡す」という記述
- `propositions/` に書かないという境界

### `skills/research/references/project_layout.md`

新設する。canonical generated project layout と artifact placement を所有する。

README、scripts、tests はこの layout に従う。

### `AGENTS.md`

repo 作業ルールだけに限定する。

含める:

- branch / test / commit / push / PR
- test admission gate
- plugin version update
- skill pressure testing の方針

含めない:

- generated project layout
- research artifact placement
- old path migration rules

## Script 変更

### `new_project.py`

新 layout を常に生成する。

追加:

- `intake.md`
- `literature/scoping.md`
- `data/eda/`
- root `observations.md`

既存の `lib/`, `data/`, `literature/` は「任意」ではなく generated layout の一部として扱う。

### `new_proposition.py`

`creating-propositions` 側へ移動する。互換 shim は作らない。

```text
skills/research/scripts/new_proposition.py
-> skills/creating-propositions/scripts/new_proposition.py
```

公開導線では `creating-propositions` が命題作成・管理 script を所有する。`research` はこの script を直接説明せず、命題管理工程として `creating-propositions` を呼ぶ。

### `new_hypothesis.py`

`research` 側に残す。plan-ready proposition から hypothesis lifecycle を開始する script である。

## README / plugin metadata 変更

README は新 workflow を先に説明する。

```text
intent
-> scoping literature
-> material acquisition
-> EDA / observations
-> creating-propositions
-> hypothesis lifecycle
```

`creating-propositions` の説明は「命題候補を作る」ではなく「命題 workspace を生成・管理する」に変える。

plugin metadata も public behavior change として更新する。

## テスト方針

Test Admission Gate classification:

- Behavior / public contract change
- Documentation contract
- Generated project layout contract

repository tests を追加・更新してよい対象:

- `new_project.py` が新 layout を生成すること
- README / SKILL / project_layout reference が旧 path を通常説明として含まないこと
- `plans/`, top-level `experiments/<id>/runs/`, `literature/differentiation.md` が通常説明に残らないこと
- plan/report checker が旧 path を拒否し続けること

repository tests にしない対象:

- 好みの文言
- release checklist state
- current version number
- PR / push / merge state

skill behavior は pressure scenarios で検証する。

## Pressure Scenarios

### Scenario 1: vague intent

User says: 「Transformer を超える研究をしたい」

Expected:

- Agent does not create a proposition immediately.
- Agent creates / updates `intake.md`.
- Agent performs scoping literature scan or records retrieval-unavailable evidence.
- Agent identifies material acquisition / EDA needs.

### Scenario 2: data-first project

User provides a dataset and says: 「ここから研究テーマを見つけたい」

Expected:

- Agent routes to EDA / observation discovery.
- EDA artifacts go under `data/eda/`.
- Project-level observations go to root `observations.md`.
- No claim is made from EDA.

### Scenario 3: prior work contradiction

User says a method is novel, but scoping finds a close prior method.

Expected:

- Agent records the prior work in `literature/scoping.md` and `literature/papers.md`.
- Agent narrows novelty / claim scope.
- Agent can still create a proposition if a real gap remains.

### Scenario 4: proposition management

User has three overlapping propositions.

Expected:

- `creating-propositions` manages split / merge / park / revise.
- `research` does not manually edit proposition state outside that workflow.
- Only plan-ready propositions proceed to `new_hypothesis.py`.

### Scenario 5: old path pressure

User asks to put a plan in `plans/01.md`.

Expected:

- Agent rejects old path.
- Agent routes to canonical hypothesis path or explains that no plan exists before a plan-ready proposition.

## 実装順

1. Add `project_layout.md` and rewrite `research/SKILL.md` around Agent workflow.
2. Rewrite `creating-propositions/SKILL.md` as proposition generation and management owner.
3. Update templates and scripts for new root intake / scoping / EDA / observations layout.
4. Remove old path references from README, tests, docs, and plugin metadata except explicit rejection tests.
5. Update or add repository contract tests for generated layout and removed old paths.
6. Run pressure scenarios with subagents and tighten skill prose from observed failures.
7. Run verification:
   - `python -m pytest tests/test_research_docs_contract.py`
   - `python -m pytest tests/test_multiple_testing.py`
   - `python -m json.tool .codex-plugin/plugin.json`
   - `git diff --check`

## リスク

### Scope creep

`research` が再び巨大な規約集になるリスクがある。対策として、`SKILL.md` は workflow と reference navigation に限定する。

### Responsibility drift

`research` と `creating-propositions` が同じ proposition files を編集し始めるリスクがある。対策として、`creating-propositions` を `propositions/` state owner と明記する。

### EDA claim leakage

EDA の発見を claim として扱うリスクがある。対策として、EDA は observation discovery に限定し、claim-bearing は hypothesis lifecycle に送る。

### Old-path residue

docs や tests に旧 path が残り、Agent が旧構造を模倣するリスクがある。対策として、旧 path は削除し、残す場合は rejection fixture としてだけ残す。

## 承認後の成果物

実装後、次が成り立つ状態にする。

- Agent は「やりたいこと」から研究を開始できる。
- 初期 literature / EDA / observation discovery が research lifecycle 本体に入っている。
- `creating-propositions` は命題生成と命題管理を所有している。
- `research` は研究全体の workflow 司令塔になっている。
- generated project layout の配置ルールが一本化されている。
- 旧構造の互換性説明が消えている。
