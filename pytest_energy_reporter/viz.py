import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Visualize energy report measurements.")
  parser.add_argument('file_link', type=str, help='The relative path to the energy report file.')
  parser.add_argument('-s', '--save', type=str, help='The directory to save the visualization in. If not provided, the visualization will just be displayed without being saved.')

  args = parser.parse_args()
  file_path = os.path.join(os.getcwd(), args.file_link)
  
  print(f"File link: {file_path}")
  with open(file_path, 'r') as file:
    data = json.load(file)
  
  results = data["results"]
  _cases = results["cases"]
  
  _filtered_cases = [case for case in _cases if 'lambda' not in case["name"]]
  
  # cases = sorted(_filtered_cases, key=lambda x: np.mean(x["energy"]), reverse=True)
  cases = _filtered_cases
  
  ticks = [i + 1 for i in range(len(cases))]
  names = []
  for case in cases:
    name = case["name"]
    removed_postfix = name.split("::")[-1]
    remove_test = removed_postfix.split("test_")[-1]
    case_n = len(case["energy"])
    tick_name = f"{remove_test} (n={case_n})"
    names.append(tick_name)
  energies = [x["energy"] for x in cases]
  avg_energies = [np.mean(x["energy"]) for x in cases]
  powers = [x["power"] for x in cases]
  avg_powers = [np.mean(x["power"]) for x in cases]
  timing = [x["execution_time"] for x in cases]
  avg_timing = [np.mean(x["execution_time"]) for x in cases]
  edp = [[x * y / 1000 for (x, y) in zip(timing[i], energies[i])] for i in range(len(cases))]
  avg_edp = [np.mean(x) for x in edp]
  
  fig = plt.figure()
  fig.set_size_inches(5, 4)
  plt.boxplot(energies)
  plt.bar(ticks, avg_energies, alpha=0.2)
  plt.violinplot(energies)
  plt.ylim(bottom=0)
  plt.title("Energy [J] per test case")
  plt.ylabel("Energy [J]")
  # plt.title("Average Power [W]")
  # plt.ylabel("Average Power [W]")
  plt.xticks(ticks=ticks, labels=names)
  plt.grid(linestyle="--", linewidth=0.5)
  plt.show(block=False)
  plt.xticks(rotation=-45, ha='left')
  plt.tight_layout()
  
  save_path = os.path.join(os.getcwd(), args.save) if args.save else None
  
  if args.save:
    plt.savefig(os.path.join(save_path, "figure_j"), dpi=300, bbox_inches='tight')
  
  fig = plt.figure()
  fig.set_size_inches(5, 4)
  plt.boxplot(powers)
  plt.bar(ticks, avg_powers, alpha=0.2)
  plt.violinplot(powers)
  plt.ylim(bottom=0)
  plt.title("Average Power [W] per test case")
  plt.ylabel("Average Power [W]")
  plt.xticks(ticks=ticks, labels=names)
  plt.grid(linestyle="--", linewidth=0.5)
  plt.show(block=False)
  plt.xticks(rotation=-45, ha='left')
  plt.tight_layout()
  if args.save:
    plt.savefig(os.path.join(save_path, "figure_w"), dpi=300, bbox_inches='tight')

  fig = plt.figure()
  fig.set_size_inches(5, 4)
  plt.boxplot(timing)
  plt.bar(ticks, avg_timing, alpha=0.2)
  plt.violinplot(timing)
  plt.ylim(bottom=0)
  plt.title("Average Time [ms] per test case")
  plt.ylabel("Average Time [ms]")
  plt.xticks(ticks=ticks, labels=names)
  plt.grid(linestyle="--", linewidth=0.5)
  plt.show(block=False)
  plt.xticks(rotation=-45, ha='left')
  plt.tight_layout()
  
  if args.save:
    plt.savefig(os.path.join(save_path, "figure_t"), dpi=300, bbox_inches='tight')

  fig = plt.figure()
  fig.set_size_inches(5, 4)
  plt.boxplot(edp)
  plt.bar(ticks, avg_edp, alpha=0.2)
  plt.violinplot(edp)
  plt.ylim(bottom=0)
  plt.title("Average Energy Delay Product [j s] per test case")
  plt.ylabel("Average Energy Delay Product [j s] ")
  plt.xticks(ticks=ticks, labels=names)
  plt.grid(linestyle="--", linewidth=0.5)
  plt.show(block=False)
  plt.xticks(rotation=-45, ha='left')
  plt.tight_layout()
  
  if args.save:
    plt.savefig(os.path.join(save_path, "figure_edp"), dpi=300, bbox_inches='tight')

  metrics =  ["energy", "power", "execution_time"]
  max_cv = {}
  max_std = {}
  for x in metrics:
    max_std[x] = 0
    max_cv[x] = 0
  
  for index, case in enumerate(cases):
    print("--------------------")
    print(f"Case {index+1}: {case['name']}")
    for x in metrics:
      print(f"-- {x} --")
      max_energy = np.max(case[x])
      min_energy = np.min(case[x])
      abs_diff = max_energy - min_energy
      std = np.std(case[x])
      mean = np.mean(case[x])
      cv = std / mean
      max_std[x] = max(max_std.get(x, 0), std)
      max_cv[x] = max(max_cv.get(x, 0), cv)
      print(f"Max: {max_energy}")
      print(f"Min: {min_energy}")
      print(f"Mean: {mean}")
      print(f"Abs diff: {abs_diff}")
      print(f"Std: {std}")
    print(f"Avg EDP: {avg_edp[index]}")
    print()
  
  print(f"Max CV: {max_cv}")
  print(f"Max STD: {max_std}")
  
  plt.show()
  
  