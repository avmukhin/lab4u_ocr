import pandas as pd

data = pd.DataFrame(columns=['ID', 'Timestamp', 'Age', 'Sex',
                             'Pregnancy', 'Meno', 'Weight',
                             'Height', 'IMT', 'Vegan',
                             'Coffee', 'Sweet', 'Alcohol', 'Stress',
                             'Sport', 'Travel', 'Sleep',
                             'Antibiotics', 'Immunity', 'Surgery'])

data.to_csv('symptom_log.csv', index=False)