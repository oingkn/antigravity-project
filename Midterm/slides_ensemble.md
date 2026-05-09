---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 26px;
  }
  h1 { color: #2c3e50; font-size: 1.8em; }
  h2 { color: #2980b9; border-bottom: 2px solid #2980b9; padding-bottom: 4px; }
  h3 { color: #16a085; }
  table { width: 100%; border-collapse: collapse; }
  th { background: #2980b9; color: white; padding: 6px 12px; }
  td { padding: 6px 12px; border: 1px solid #ddd; }
  tr:nth-child(even) { background: #f4f8fb; }
  code { background: #f0f0f0; border-radius: 4px; padding: 2px 6px; }
  blockquote { border-left: 4px solid #2980b9; padding-left: 12px; color: #555; }
---

# 모델 성능 향상과 앙상블 기법

**주요 학습 목표**

1. 과대적합(Overfitting)과 과소적합(Underfitting) 이해
2. 교차검증(Cross-Validation)의 개념과 활용
3. 앙상블 학습과 랜덤 포레스트 원리 이해

---

## 목차

1. 과대적합과 과소적합
   - 편향-분산 트레이드오프
   - 원인과 해결 방법
2. 교차검증의 이해
   - K-Fold / StratifiedKFold
   - 폴드 수 선택 기준
3. 앙상블 학습: 랜덤 포레스트
   - 배깅(Bagging) 개념
   - 특성 중요도(Feature Importance)

---

## 1. 과대적합과 과소적합

**모델 복잡도와 성능의 관계**

| 상태 | 학습 데이터 성능 | 테스트 성능 | 원인 |
|------|----------------|-------------|------|
| 과소적합 | 낮음 ↓ | 낮음 ↓ | 모델이 너무 단순 |
| 적정 모델 | 높음 ↑ | 높음 ↑ | 균형 잡힌 복잡도 |
| 과대적합 | 매우 높음 ↑↑ | 낮음 ↓ | 모델이 너무 복잡 |

> 목표: **Train 성능과 Test 성능의 간격을 최소화**

---

## 편향-분산 트레이드오프

```
오류(Error)
│
│  \        /    ← 전체 오류 (U자형)
│   \      /
│    \    /  ← 분산(Variance): 복잡도↑ 시 증가
│     \  /
│      \/
│  ────── ← 편향(Bias): 복잡도↑ 시 감소
│
└────────────────────── 모델 복잡도
     낮음         높음
  (과소적합)    (과대적합)
```

- **편향(Bias)**: 모델의 가정이 현실과 달라 생기는 오류
- **분산(Variance)**: 학습 데이터 변화에 따른 예측 불안정성

---

## 과대적합 예방 방법

| 방법 | 설명 |
|------|------|
| **모델 단순화** | 파라미터 수 줄이기 (max_depth 제한) |
| **정규화(Regularization)** | L1(Lasso), L2(Ridge) 패널티 추가 |
| **더 많은 데이터** | 학습 데이터 확보로 일반화 향상 |
| **드롭아웃(Dropout)** | 신경망에서 일부 뉴런 무작위 비활성화 |
| **앙상블** | 여러 모델 결합으로 분산 감소 |
| **조기 종료(Early Stopping)** | 검증 오류가 증가하면 학습 중단 |

---

## 실습: 결정 트리 max_depth 변화

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

depths = range(1, 20)
train_scores, test_scores = [], []

for depth in depths:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_scores.append(accuracy_score(y_train, model.predict(X_train)))
    test_scores.append(accuracy_score(y_test, model.predict(X_test)))
```

- depth=1~2 → **과소적합**: 두 점수 모두 낮음
- depth=5~7 → **적정**: Test 점수 최고점
- depth=15+ → **과대적합**: Train 높지만 Test 하락

---

## 2. 교차검증의 이해

**왜 교차검증이 필요한가?**

단순 Hold-out 분리의 문제점:
- 분리 방법에 따라 결과가 크게 달라질 수 있음
- 작은 데이터셋에서 평가 신뢰도 낮음

**해결책: K-Fold 교차검증**

```
K = 5 일 때:
┌─────┬─────┬─────┬─────┬─────┐
│ Val │Train│Train│Train│Train│  ← Fold 1
│Train│ Val │Train│Train│Train│  ← Fold 2
│Train│Train│ Val │Train│Train│  ← Fold 3
│Train│Train│Train│ Val │Train│  ← Fold 4
│Train│Train│Train│Train│ Val │  ← Fold 5
└─────┴─────┴─────┴─────┴─────┘
```

---

## KFold vs StratifiedKFold

| 구분 | KFold | StratifiedKFold |
|------|-------|-----------------|
| 클래스 비율 유지 | ❌ | ✅ |
| 불균형 데이터 | 불안정 | 안정적 |
| 권장 용도 | 회귀 문제 | **분류 문제** |

```python
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')

print(f"평균: {scores.mean():.4f}")
print(f"표준편차: {scores.std():.4f}")
```

---

## 폴드 수(K) 선택 기준

| K 값 | 장점 | 단점 |
|------|------|------|
| 작을수록 (K=3) | 빠른 계산 | 높은 편향, 불안정 |
| 클수록 (K=10) | 낮은 편향, 안정적 | 계산 비용 증가 |
| **K=5 또는 K=10** | **균형 있는 선택** | — |

> **일반적으로 K=5 또는 K=10을 권장**

---

## 3. 앙상블 학습

**핵심 아이디어**: "여럿이 협력하면 혼자보다 낫다"

```
원본 데이터
    │
    ├──[샘플 1] → 모델 1 → 예측 1 ─┐
    ├──[샘플 2] → 모델 2 → 예측 2 ─┼─ 다수결/평균 → 최종 예측
    │              ⋮              ⋮
    └──[샘플 N] → 모델 N → 예측 N ─┘
```

**주요 앙상블 기법**

| 기법 | 방식 | 대표 알고리즘 |
|------|------|---------------|
| 배깅(Bagging) | 병렬, 독립 학습 | 랜덤 포레스트 |
| 부스팅(Boosting) | 순차, 오류 보정 | XGBoost, LightGBM |
| 스태킹(Stacking) | 메타 모델 결합 | 다양한 조합 |

---

## 랜덤 포레스트(Random Forest)

**배깅 + 특성 무작위성**으로 다양성을 극대화

### 동작 원리

1. **부트스트랩 샘플링**: 원본 데이터에서 복원 추출로 N개의 서브셋 생성
2. **특성 무작위 선택**: 각 분기점에서 √(전체 특성 수)개의 특성만 사용
3. **독립 트리 학습**: 각 서브셋으로 결정 트리를 독립적으로 학습
4. **다수결 투표**: 모든 트리의 예측을 다수결로 최종 결정

> 무작위성 → 트리 간 **다양성 확보** → **분산 감소** → 일반화 성능 향상

---

## 랜덤 포레스트 코드 실습

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold

rf = RandomForestClassifier(
    n_estimators=100,   # 트리 수
    max_depth=None,     # 트리 깊이 제한 없음 (기본)
    max_features='sqrt',# 각 분기에서 사용할 특성 수
    random_state=42
)

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(rf, X, y, cv=cv, scoring='accuracy')

print(f"RF CV 평균 정확도: {scores.mean():.4f}")
```

---

## 단일 트리 vs 랜덤 포레스트

| 항목 | 단일 결정 트리 | 랜덤 포레스트 |
|------|--------------|--------------|
| 학습 속도 | 빠름 | 느림 |
| 과대적합 | 취약 | 강건 |
| 해석 가능성 | 높음 | 낮음 |
| 예측 정확도 | 보통 | **높음** |
| 특성 중요도 | 제공 | **제공** |

> **앙상블로 분산을 줄이면서 편향은 유지** → 전반적인 성능 향상

---

## 특성 중요도(Feature Importance)

각 특성이 불순도(Gini Impurity)를 얼마나 감소시키는지 측정

```python
rf.fit(X_train, y_train)

importances = rf.feature_importances_  # 합계 = 1.0
indices = np.argsort(importances)[::-1]

# 상위 10개 특성 출력
for i in range(10):
    print(f"{feature_names[indices[i]]}: {importances[indices[i]]:.4f}")
```

활용 방법:
- **특성 선택(Feature Selection)**: 중요도 낮은 특성 제거
- **도메인 이해**: 어떤 변수가 예측에 영향을 미치는지 파악

---

## 주요 하이퍼파라미터 정리

| 파라미터 | 설명 | 기본값 | 팁 |
|----------|------|--------|----|
| `n_estimators` | 트리 수 | 100 | 많을수록 안정, 보통 100~300 |
| `max_depth` | 트리 최대 깊이 | None | 과대적합 시 제한 |
| `max_features` | 분기 시 고려 특성 수 | `'sqrt'` | 분류: sqrt, 회귀: 1.0 |
| `min_samples_split` | 분기 최소 샘플 수 | 2 | 높이면 과대적합 방지 |
| `min_samples_leaf` | 리프 최소 샘플 수 | 1 | 높이면 과대적합 방지 |

---

## 전체 요약

| 개념 | 핵심 메시지 |
|------|-------------|
| **과소적합** | 모델을 더 복잡하게 만들거나 더 많은 특성을 사용 |
| **과대적합** | 정규화, 데이터 증강, 앙상블로 일반화 향상 |
| **교차검증** | K-Fold로 신뢰도 높은 성능 추정, 분류엔 Stratified |
| **랜덤 포레스트** | 배깅 + 무작위 특성 선택 → 과대적합 방지 + 성능 향상 |

### 실무 팁
1. 항상 **교차검증으로 성능 평가** (단일 분리 지양)
2. 베이스라인은 **랜덤 포레스트**로 시작
3. 특성 중요도로 **도메인 인사이트** 도출

---

## 참고 자료 및 실습

- 실습 노트북: `week_ensemble.ipynb`
- 사용 데이터: `sklearn.datasets.load_breast_cancer`
- 주요 라이브러리: `scikit-learn`, `numpy`, `matplotlib`

### 다음 시간 예고
> **하이퍼파라미터 튜닝**: Grid Search, Random Search, Bayesian Optimization
