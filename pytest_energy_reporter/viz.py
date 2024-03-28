import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Visualize energy report measurements.")
  parser.add_argument('file_link', type=str, help='The relative path to the energy report file.')

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
  names = [f'{x["name"].split("::")[-1]} ({len(x["energy"])})' for x in cases]
  energies = [x["energy"] for x in cases]
  avg_energies = [np.mean(x["energy"]) for x in cases]
  powers = [x["power"] for x in cases]
  
  plt.figure()
  plt.boxplot(energies)
  plt.bar(ticks, avg_energies, alpha=0.2)
  plt.violinplot(energies)
  plt.ylim(bottom=0)
  plt.ylabel("Energy [J]")
  plt.title("Energy [J]")
  # plt.title("Average Power [W]")
  # plt.ylabel("Average Power [W]")
  plt.xticks(ticks=ticks, labels=names)
  plt.grid(linestyle="--", linewidth=0.5)
  plt.show(block=False)
  plt.xticks(rotation=-45)
  plt.tight_layout()

  plt.show()
  