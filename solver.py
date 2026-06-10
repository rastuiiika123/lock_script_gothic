import os
from collections import deque

# === Получаем путь к папке, где лежит скрипт ===
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'in.txt')

# === Чтение из in.txt ===
with open(input_file, 'r', encoding='utf-8') as f:
    lines = [line.strip() for line in f.readlines() if line.strip()]

initial = {}
rules = []
rule_id = 1

for line in lines:
    line = line.strip()
    if '=' in line and '->' not in line:
        # Начальные значения: a = 4
        var, val = [x.strip() for x in line.split('=')]
        initial[var] = int(val)
    
    elif '->' in line:
        left, right = [x.strip() for x in line.split('->')]
        
        # Левая часть: aA или bD
        left_var = left[0]
        left_dir = 1 if left[1].upper() == 'A' else -1
        
        # Правая часть
        effects = []
        right = right.strip()
        
        if right in ['0', '0 ']:
            # Только меняем левую переменную
            pass
        else:
            for item in right.split(','):
                item = item.strip()
                if item:
                    var = item[0]
                    dir_sign = 1 if item[1].upper() == 'A' else -1
                    effects.append((var, dir_sign))
        
        rules.append({
            'id': rule_id,
            'var': left_var,
            'left_dir': left_dir,
            'effects': effects
        })
        rule_id += 1

# Автоматическое определение переменных
vars_order = sorted([v for v in initial.keys() if v in 'abcdef'])
target = tuple([4] * len(vars_order))

print(f"Обнаружено переменных: {len(vars_order)} → {vars_order}")
print(f"Цель: все равны 4\n")

def state_to_tuple(s):
    return tuple(s.get(v, 4) for v in vars_order)

def apply_rule(state, rule_idx, multiplier):
    rule = rules[rule_idx]
    new_state = state.copy()
    
    # Левая часть
    left_var = rule['var']
    change = rule['left_dir'] * multiplier
    new_state[left_var] = new_state.get(left_var, 4) + change
    if not (1 <= new_state[left_var] <= 7):
        return None
    
    # Правые эффекты
    for var, sign in rule['effects']:
        change = sign * multiplier
        new_state[var] = new_state.get(var, 4) + change
        if not (1 <= new_state[var] <= 7):
            return None
    
    return new_state

# BFS
start = initial.copy()
queue = deque([(start, [])])
visited = {state_to_tuple(start)}

solution = None
max_depth = 150   # можно увеличить

while queue:
    state, path = queue.popleft()
    if state_to_tuple(state) == target:
        solution = path
        break
    if len(path) >= max_depth:
        continue
    
    for r in range(len(rules)):
        for m, dir_name in [(1, 'A'), (-1, 'D')]:
            new_state = apply_rule(state, r, m)
            if new_state and state_to_tuple(new_state) not in visited:
                visited.add(state_to_tuple(new_state))
                queue.append((new_state, path + [(rules[r]['id'], dir_name)]))

# Вывод результата
if solution:
    print(f"✅ Решение найдено за {len(solution)} шагов\n")
    print("Последовательность (группами):")
    i = 0
    while i < len(solution):
        rule, direc = solution[i]
        count = 1
        j = i + 1
        while j < len(solution) and solution[j] == (rule, direc):
            count += 1
            j += 1
        if count > 1:
            print(f"**{rule}{direc} ×{count}**")
        else:
            print(f"**{rule}{direc}**")
        i += count
    print(f"\nВсего шагов: {len(solution)}")
else:
    print("❌ Решение не найдено в пределах max_depth.")