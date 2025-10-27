import pandas as pd
import nfl_data_py as nfl
import matplotlib.pyplot as plt

pbp = nfl.import_pbp_data([2023, 2024])
falcons_def = pbp[(pbp['defteam'] == 'ATL') & (pbp['play_type'] == 'pass')].copy()
falcons_def.loc[:, 'pressure'] = (falcons_def['sack'] == 1) | (falcons_def['qb_hit'] == 1)


pressure_rate = falcons_def['pressure'].mean()
epa_by_pressure = falcons_def.groupby('pressure')['epa'].mean()
comp_by_pressure = falcons_def.groupby('pressure')['complete_pass'].mean()
print(f"Falcons pressure rate: {pressure_rate:.2%}")
print(epa_by_pressure)
print(comp_by_pressure)

colors = ['#C8102E', '#A5ACAF']


fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].bar(['No Pressure', 'Pressure'], epa_by_pressure, color=colors)
axes[0].set_title('EPA Allowed Under Pressure vs No Pressure')
axes[0].set_ylabel('Average EPA per Play')
axes[0].set_xlabel('Situation')

for i, val in enumerate(epa_by_pressure):
    axes[0].text(i, val - 0.08 if val > 0 else val + 0.1, f'{val:.2f}', 
                 ha='center', va='bottom' if val > 0 else 'top')

axes[1].bar(['No Pressure', 'Pressure'], comp_by_pressure, color=colors)
axes[1].set_title('Completion % Under Pressure vs No Pressure')
axes[1].set_ylabel('Completion Rate')
axes[1].set_xlabel('Situation')
for i, val in enumerate(comp_by_pressure):
    axes[1].text(i, val - 0.03, f'{val:.2%}', ha='center', va='top')

plt.suptitle('Atlanta Falcons Defensive Pressure Impact (2023–24)', fontsize=14, fontweight='bold', y=1.10)
plt.tight_layout(rect=[0, 0, 1, 0.9])
plt.show()

