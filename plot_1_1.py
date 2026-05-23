import numpy as np
import matplotlib.pyplot as plt
import platform
import os

import matplotlib.font_manager as fm

# NanumGothic 폰트 캐시를 스캔/업데이트 (설치 후 폰트를 찾지 못하는 문제 해결)
fm._load_fontmanager(try_read_cache=False)

# rcParams 설정 필수로 적용하여 NanumGothic 지정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False


# 1-1. Figure / Axes 구조 이해
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Matplotlib 주요 그래프 유형', fontsize=16, fontweight='bold', y=1.01)

x = np.linspace(0, 2 * np.pi, 100)
np.random.seed(42)
colors = ['#4f8ef7', '#a78bfa', '#34d399', '#fbbf24', '#f87171']

# 1) 선 그래프
axes[0, 0].plot(x, np.sin(x), label='sin(x)', color='steelblue', linewidth=2)
axes[0, 0].plot(x, np.cos(x), label='cos(x)', color='tomato', linewidth=2, linestyle='--')
axes[0, 0].set_title('선 그래프')
axes[0, 0].set_xlabel('x'); axes[0, 0].set_ylabel('y')
axes[0, 0].legend(); axes[0, 0].grid(alpha=0.3)

# 2) 막대 그래프
cats = ['A', 'B', 'C', 'D', 'E']
vals = [23, 45, 32, 67, 41]
axes[0, 1].bar(cats, vals, color=colors, edgecolor='white', linewidth=0.7)
axes[0, 1].set_title('막대 그래프')
for i, v in enumerate(vals):
    axes[0, 1].text(i, v + 0.5, str(v), ha='center', fontsize=10)

# 3) 산점도
x_s = np.random.randn(100)
y_s = 2 * x_s + np.random.randn(100) * 0.8
sc = axes[0, 2].scatter(x_s, y_s, c=y_s, cmap='coolwarm', alpha=0.7, s=40)
axes[0, 2].set_title('산점도')
fig.colorbar(sc, ax=axes[0, 2])

# 4) 히스토그램 + KDE
data = np.random.normal(50, 15, 500)
axes[1, 0].hist(data, bins=30, color='#4f8ef7', edgecolor='white', alpha=0.8, density=True)
from scipy.stats import norm
x_kde = np.linspace(data.min(), data.max(), 200)
axes[1, 0].plot(x_kde, norm.pdf(x_kde, data.mean(), data.std()), 'r-', lw=2)
axes[1, 0].set_title('히스토그램 + KDE')

# 5) 박스 플롯
data_box = [np.random.normal(loc, 1, 100) for loc in range(5)]
bp = axes[1, 1].boxplot(data_box, patch_artist=True,
                         medianprops=dict(color='white', linewidth=2))
for patch, c in zip(bp['boxes'], colors):
    patch.set_facecolor(c); patch.set_alpha(0.7)
axes[1, 1].set_title('박스 플롯')

# 6) 파이 차트
sizes = [30, 25, 20, 15, 10]
labels = ['Python', 'Java', 'C++', 'JS', '기타']
axes[1, 2].pie(sizes, labels=labels, autopct='%1.1f%%',
               startangle=90, colors=colors,
               wedgeprops=dict(edgecolor='white'))
axes[1, 2].set_title('파이 차트')

plt.tight_layout()
plt.savefig('1_matplotlib_basics.png', dpi=150, bbox_inches='tight')
print("Plot saved to 1_matplotlib_basics.png")
