# LLM Ensemble Labs — 퀴즈 & 실습 과제 (학생용)

> 이 과제는 **Ollama 로컬 모델**을 사용하며, 코드를 실행하고 결과를 관찰하는 **탐구형 실습**입니다.  
> 정답을 외우는 것보다 **실험 설계 → 관찰 → 분석 → 개선** 흐름을 익히는 것이 목표입니다.

## 제출물 안내

각 퀴즈마다 아래 항목을 포함한 짧은 리포트(1~2페이지)를 제출하세요.

- 실험 설정 (모델명, 파라미터 값)
- 터미널 출력 캡처 또는 결과 텍스트
- 결과 비교표 (파라미터별 정확도 / 속도 등)
- 한계 및 개선 아이디어 (최소 3가지)

---

## 공통 준비 사항

### 권장 모델

| 상황 | 권장 모델 |
|------|-----------|
| 기본 (RAM 8 GB 이상) | `qwen2.5:3b-instruct` |
| 저사양 / 속도 우선 | `qwen2.5:1.5b-instruct` |
| 대안 | `llama3.2:3b` |

### Ollama 서버 확인

```bash
# 서버가 실행 중인지 확인 (응답이 오면 정상)
curl http://localhost:11434/api/tags
```

> 응답이 없으면 `ollama serve` 명령으로 서버를 먼저 시작하세요.

---

## Quiz 1 — Self-Consistency로 정확도 올리기 (Lab 01)

> 관련 파일: `labs/01_self_consistency_ollama.py`

### 배경

같은 문제를 여러 번 물어보고 **다수결**로 최종 답을 고르면 단일 응답보다 정확도가 높아질 수 있습니다.  
이번 실습에서는 샘플 수를 바꿔 가며 이 효과를 직접 측정합니다.

### Q1-1 샘플 수 비교

아래 세 가지 설정으로 각각 실행하고, 결과를 비교하세요.

```bash
# 실험 1 — 샘플 1개 (사실상 단일 응답)
python labs/01_self_consistency_ollama.py --model qwen2.5:3b-instruct --num-samples 1

# 실험 2 — 샘플 3개
python labs/01_self_consistency_ollama.py --model qwen2.5:3b-instruct --num-samples 3

# 실험 3 — 샘플 5개
python labs/01_self_consistency_ollama.py --model qwen2.5:3b-instruct --num-samples 5
```

#### 결과 기록 예시

| 설정 | Single-shot 정확도 | SC 정확도 | 총 LLM 호출 수 | 소요 시간 (초) |
|------|--------------------|-----------|----------------|----------------|
| `--num-samples 1` | | | | |
| `--num-samples 3` | | | | |
| `--num-samples 5` | | | | |

#### 제출 질문

1. 샘플 수를 늘릴수록 정확도가 항상 올라갔나요? 그렇지 않은 경우가 있었다면 이유가 무엇이라고 생각하나요?
2. **정확도 상승 폭 ÷ 추가 호출 횟수** 기준으로 가장 효율적인 설정은 무엇이었나요?
3. 샘플 수를 늘릴 때 실제 비용(시간 / API 비용)은 어떻게 변하나요? 현실적인 트레이드오프를 서술하세요.

### Q1-2 데이터셋 확장 (코드 수정)

`labs/01_self_consistency_ollama.py` 파일을 열어 `DATASET` 리스트를 수정하세요.

- 기존 문제 외에 **10개 이상** 새 문제를 추가하세요.
- 단순 덧셈/뺄셈 외에도 괄호가 있는 수식(예: `(12 + 7) - 5`)을 포함하세요.
- 실험 후 **모델이 틀린 유형**을 최소 2가지 찾아 기록하고, 왜 틀렸는지 추측해보세요.

---

## Quiz 2 — Tree-of-Thought(ToT)로 추론 경로 탐색하기 (Lab 02)

> 관련 파일: `labs/02_tot_ollama.py`

### 배경

ToT는 여러 추론 경로를 동시에 탐색하고 점수를 매겨 좋은 경로를 선택하는 방법입니다.  
`depth`(탐색 깊이)와 `beam-width`(유지할 후보 수)가 결과 품질과 속도에 미치는 영향을 실험합니다.

### Q2-1 Depth × Beam-width 비교

아래 조합을 실행하고 결과를 기록하세요.

```bash
# depth 1, beam-width 1 (단일 경로)
python labs/02_tot_ollama.py --model qwen2.5:3b-instruct --depth 1 --beam-width 1

# depth 2, beam-width 2
python labs/02_tot_ollama.py --model qwen2.5:3b-instruct --depth 2 --beam-width 2

# depth 3, beam-width 2
python labs/02_tot_ollama.py --model qwen2.5:3b-instruct --depth 3 --beam-width 2
```

#### 결과 기록 예시

| depth | beam-width | 최종 답 | 정답 여부 | 소요 시간 (초) | 총 LLM 호출 수 |
|-------|------------|---------|-----------|----------------|----------------|
| 1 | 1 | | | | |
| 2 | 2 | | | | |
| 3 | 2 | | | | |

#### 제출 질문

1. depth / beam-width를 키울수록 답의 품질이 좋아졌나요? 항상 그런가요?
2. depth 3 vs depth 1 의 소요 시간 차이는 얼마나 되었나요? 이 차이가 실용적으로 허용 가능한 수준인가요?
3. "좋은 후보"가 충분히 다양하게 나오지 않는 경우가 있었나요? 어떤 상황에서 그런 현상이 발생했나요?

### Q2-2 프롬프트 개선 (코드 수정)

`labs/02_tot_ollama.py` 안의 `propose_candidates()` 함수 프롬프트를 개선하세요.

개선 목표 중 하나를 선택하세요:

- **다양성**: 후보 3개가 너무 비슷한 내용을 반복할 때 → 서로 다른 접근법을 유도하는 지시 추가
- **구체성**: 후보가 너무 추상적일 때 → 계산 단계를 명시적으로 포함하도록 지시 추가

#### 제출물

- 변경 **전** 프롬프트 전문
- 변경 **후** 프롬프트 전문
- 동일 문제에 대한 출력 비교 로그 (변경 전 / 후)

---

## Quiz 3 — Pseudo-MoE Router 확장하기 (Lab 03)

> 관련 파일: `labs/03_router_moe_ollama.py`

### 배경

규칙 기반 라우터는 질의 유형을 키워드로 판별해 적합한 전문가 프롬프트에 연결합니다.  
이번 실습에서는 라우터를 확장하고 한계를 직접 탐색합니다.

### Q3-1 번역 전문가 추가

`labs/03_router_moe_ollama.py`를 수정해 **4번째 전문가: translation**을 추가하세요.

```python
# 힌트: route() 함수에 번역 키워드 조건을 추가하고,
# build_prompt() 함수에 translation 분기를 추가하세요.
# 예시 키워드: "translate", "번역", "영어로", "한국어로"
```

확장 후 아래 명령으로 실행하세요.

```bash
python labs/03_router_moe_ollama.py --model qwen2.5:3b-instruct
```

#### 제출 질문

1. 새로 추가한 번역 전문가가 잘 동작하는지 테스트 입력 예시 3개를 만들어 결과를 기록하세요.
2. **잘못 라우팅된(misrouted) 입력**을 5개 이상 찾아 기록하세요. 왜 오류 라우팅이 발생했나요?
3. 규칙 기반 라우터의 근본적인 한계는 무엇이라고 생각하나요? 개선 방법을 2가지 제안하세요.

### Q3-2 모델 기반 라우터 (심화 선택 과제)

키워드 대신 **LLM 자체를 라우터로 사용**해보세요.

짧은 프롬프트로 모델이 `route: math`, `route: code`, `route: summary`, `route: translation` 중 하나만 출력하도록 만들고, 그 결과로 전문가를 선택하세요.

```python
# 힌트: 아래와 같은 프롬프트를 사용할 수 있습니다.
ROUTER_PROMPT = """다음 질문의 유형을 판별하세요.
가능한 유형: math, code, summary, translation

다음 형식으로만 답하세요 (다른 말 금지):
route: <유형>

질문: {query}
"""
```

#### 제출물

- 모델 기반 라우팅 프롬프트 전문
- 직접 만든 테스트 질문 20개와 정답 route, 모델 예측 route 비교표
- 규칙 기반 vs 모델 기반의 라우팅 정확도 비교

---

## Mini Project — 나만의 앙상블 파이프라인 설계

아래 두 옵션 중 **하나를 선택**해서 구현하고 분석 리포트를 작성하세요.

---

### 옵션 A: Verifier-Reranker 파이프라인

**개요**

1. LLM으로 후보 답변 N개를 생성합니다.
2. 검증기 프롬프트(verifier prompt)로 각 후보에 0~10 점수를 매깁니다.
3. 가장 높은 점수의 답변을 최종 선택합니다.

**구현 힌트**

```python
# 1단계: 후보 생성
candidates = [ollama_generate(model, question_prompt) for _ in range(N)]

# 2단계: 검증 점수 계산
scores = [score_answer(model, question, c) for c in candidates]

# 3단계: 최고 점수 선택
best = candidates[scores.index(max(scores))]
```

**제출 질문**

1. Majority vote(다수결) vs Verifier-Reranker 중 어느 쪽이 더 안정적이었나요?
2. 검증기가 잘못된 점수를 매긴 경우가 있었나요? 어떤 상황에서 발생했나요?
3. N(후보 수)을 늘릴수록 결과가 좋아졌나요? 최적의 N은 얼마였나요?

---

### 옵션 B: Debate with Judge

**개요**

1. Agent A와 Agent B가 같은 문제에 대해 서로 다른 관점에서 해법을 제시합니다.
2. Judge 에이전트가 두 주장을 보고 최종 답을 선택합니다.

**구현 힌트**

```python
AGENT_A_PROMPT = "다음 문제를 풀되, 단계별 계산을 보여주세요.\n문제: {question}"
AGENT_B_PROMPT = "다음 문제를 풀되, 다른 풀이 방법을 사용하세요.\n문제: {question}"
JUDGE_PROMPT = """두 에이전트의 답변을 검토하고 더 정확한 것을 선택하세요.

Agent A: {answer_a}
Agent B: {answer_b}

최종 답: """
```

**제출 질문**

1. Judge가 항상 올바른 답변을 선택했나요? 실패 사례를 기록하세요.
2. Agent A와 B가 같은 답을 내는 경우가 얼마나 자주 있었나요?
3. Judge의 편향(항상 A 또는 항상 B를 선택)이 관찰되었나요? 이를 줄이는 방법을 제안하세요.

---

## 제출 체크리스트

제출 전에 아래 항목을 모두 확인하세요.

- [ ] 모든 코드가 실제로 실행됨 (에러 없이)
- [ ] 사용한 모델명과 파라미터가 명시됨
- [ ] 각 실험의 터미널 출력(로그)이 포함됨
- [ ] 파라미터 비교표가 1개 이상 포함됨
- [ ] 제출 질문에 대한 본인의 분석이 서술됨
- [ ] 한계와 개선 아이디어가 3개 이상 제시됨
- [ ] (Mini Project) 구현 코드가 포함됨
