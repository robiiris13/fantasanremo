""" Knapsack problem using MIP in Google or-tools """
# Quote snai from https://www.snai.it/sport/SPETTAC/FESTIVAL%20DI%20SANREMO

from ortools.linear_solver import pywraplp
import pandas as pd
from pathlib import Path

class Performer():
    
    def __init__(self, name: str, baudi: int, quota_snai: int):
        
        self.name = name
        self.baudi = baudi
        self.quota_snai = quota_snai
    
    def from_df_to_list_of_class_instances(path_to_xlsx: Path) -> list:
        
        df = pd.read_excel(path_to_xlsx, engine='openpyxl')
        performers = df.values.tolist()
        performer_instances = []
        for performer_instance in performers:
            performer_instances.append(Performer(*performer_instance))
            
        return performer_instances


def main():

  # Create the solver
  solver = pywraplp.Solver.CreateSolver('CBC')
  
  # Get data
  data = Performer.from_df_to_list_of_class_instances('./data/input/performers.xlsx')
  
  # Get solver parameters
  capacity = 100 # baudi
  values = [dat.quota_snai for dat in data]    
  weights = [dat.baudi for dat in data]
  
  # Get indices
  values_idxs = list(range(len(values)))

  # Variable
  var_take = [solver.BoolVar('variable[%i]' % vi) for vi in values_idxs]

  # Constraint
  ## Total weight of all items taken has to be lower than total capacity
  solver.Add(solver.Sum([weights[vi] * var_take[vi] for vi in values_idxs]) <= capacity)
  ## The team has to be composed of 5 members
  solver.Add(solver.Sum([var_take[vi] for vi in values_idxs]) == 5)

  # Objective function: minimize quota_snai
  objective_function = solver.Sum([values[vi] * var_take[vi] for vi in values_idxs])
  objective = solver.Minimize(objective_function)

  # Solve
  solver.Solve()

  print()
  print('Objective value: ', int(solver.Objective().Value()))
  
  print()
  print('Solution:', end=' \n')
  for vi in values_idxs:
    if int(var_take[vi].SolutionValue()) == 1:
        print(vi, ') ', data[vi].name, end=' \n')
  print()
  
  solution = [data[vi] for vi in values_idxs if int(var_take[vi].SolutionValue()) == 1]
  print(solution)
  df_output = pd.DataFrame.from_records([sol.__dict__ for sol in solution])
  df_output.to_excel('./data/output/performers_best_team.xlsx', index=False)
  
  print()
  print('Solver time:', solver.WallTime(), 'ms')


if __name__ == '__main__':

  main()