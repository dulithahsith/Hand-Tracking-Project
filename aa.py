import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

# Load the dataset
data = pd.read_csv('supermarket.csv')

# Preprocess the data
basket = pd.get_dummies(data)

# Apply the FP-Growth algorithm
frequent_itemsets = fpgrowth(basket, min_support=0.1, use_colnames=True)

# Generate association rules
rules = association_rules(
    frequent_itemsets, metric="confidence", min_threshold=0.5)

# Sort and select the top 3 interesting rules
rules = rules.sort_values(by='lift', ascending=False)
interesting_rules = rules.head(3)

for index, rule in interesting_rules.iterrows():
    print(f"Rule {index+1}:")
    print(f"  {', '.join(rule['antecedents'])
               } --> {', '.join(rule['consequents'])}")
    print(f"  Support: {rule['support']}")
    print(f"  Confidence: {rule['confidence']}")
    print(f"  Lift: {rule['lift']}")
    print()
