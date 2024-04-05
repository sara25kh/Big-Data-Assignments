# Function to read data from the CSV file
def read_data(file_name):
    with open(file_name, 'r') as file:
        data = [line.strip().split(',') for line in file.readlines()]
    return data

# Function to get frequent items based on minimum support
def get_frequent_items(data, min_support):
    item_counts = {}
    frequent_items = {}
    
    # Counting occurrences of each item
    for basket in data:
        for item in basket:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
    
    # Filtering frequent items based on minimum support
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}
    
    return frequent_items

# Function to get frequent pairs of items based on minimum support
def get_frequent_pairs(data, min_support, frequent_items):
    pair_counts = {}
    frequent_pairs = {}
    
    # Counting occurrences of pairs of items
    for basket in data:
        for i in range(len(basket)):
            for j in range(i+1, len(basket)):
                item1 = basket[i]
                item2 = basket[j]
                
                # Sorting the items to ensure consistent pair representation
                pair = tuple(sorted([item1, item2]))
                
                if pair in pair_counts:
                    pair_counts[pair] += 1
                else:
                    pair_counts[pair] = 1
    
    # Filtering frequent pairs based on minimum support and valid items
    frequent_pairs = {pair: count for pair, count in pair_counts.items() if count >= min_support 
                      and pair[0] in frequent_items and pair[1] in frequent_items}
    
    return frequent_pairs

# Function to get frequent triples of items based on minimum support
def get_frequent_triples(data, min_support, frequent_pairs):
    triple_counts = {}
    frequent_triples = {}
    
    # Counting occurrences of triples of items
    for basket in data:
        for pair, count in frequent_pairs.items():
            if pair[0] in basket and pair[1] in basket:
                for item in basket:
                    if item != pair[0] and item != pair[1]:
                        triple = tuple(sorted(list(pair) + [item]))
                        if triple in triple_counts:
                            triple_counts[triple] += 1
                        else:
                            triple_counts[triple] = 1
    
    # Filtering frequent triples based on minimum support
    frequent_triples = {triple: count for triple, count in triple_counts.items() if count >= min_support}
    
    return frequent_triples

# Function to print the most frequent items
def print_most_frequent_items(frequent_items, n):
    sorted_items = sorted(frequent_items.items(), key=lambda x: x[1], reverse=True)[:n]
    print("Top", n, "most frequent items:")
    for item, count in sorted_items:
        print(item, ":", count)

# Function to print the most frequent pairs of items
def print_most_frequent_pairs(frequent_pairs, n):
    sorted_pairs = sorted(frequent_pairs.items(), key=lambda x: x[1], reverse=True)[:n]
    print("Top", n, "most frequent pairs of items:")
    for pair, count in sorted_pairs:
        print(pair, ":", count)

# Function to print the most frequent triples of items
def print_most_frequent_triples(frequent_triples, n):
    sorted_triples = sorted(frequent_triples.items(), key=lambda x: x[1], reverse=True)[:n]
    print("Top", n, "most frequent triples of items:")
    for triple, count in sorted_triples:
        print(triple, ":", count)

# Function to calculate confidence score of association rules
def calculate_confidence(itemset_A, itemset_B, frequent_triples, frequent_pairs):
    # Join A and B to create the union itemset
    union_itemset = set(itemset_A).union(set(itemset_B))
    # print('union_itemset',tuple(union_itemset))
    # print(type(frequent_itemsets.keys()))
    # for key in frequent_itemsets.keys():
    #     if(len(key) > 2):
    #         print('key', key)
    # Calculate support of A and B
    # print('looking for', tuple(union_itemset))
    support_A_union_B = frequent_triples.get(tuple(union_itemset), 0)
    support_A = frequent_pairs.get(tuple(itemset_A), 0)
    # print("support_A_union_B", support_A_union_B)
    # Calculate confidence
    if support_A != 0:
        confidence = support_A_union_B / support_A
    else:
        confidence = 0
    
    return confidence

# Function to get top rules based on confidence
def get_top_rules(frequent_triples, frequent_pairs):
    top_rules = []
    
    # Loop through each frequent triple
    for triple, count in frequent_triples.items():
        A, B, C = triple
        
        # Calculate confidence scores for the rules (A, B) -> C, (A, C) -> B, and (B, C) -> A
        confidence_AB_C = calculate_confidence([A, B], [C], frequent_triples, frequent_pairs)
        confidence_AC_B = calculate_confidence([A, C], [B], frequent_triples, frequent_pairs)
        confidence_BC_A = calculate_confidence([B, C], [A], frequent_triples, frequent_pairs)
        
        # Add the rules and their confidence scores to the list
        top_rules.append((f"({A}, {B}) -> {C}", confidence_AB_C))
        top_rules.append((f"({A}, {C}) -> {B}", confidence_AC_B))
        top_rules.append((f"({B}, {C}) -> {A}", confidence_BC_A))
    
    # Sort the rules based on confidence score in descending order
    top_rules.sort(key=lambda x: x[1], reverse=True)
    
    return top_rules[:5]  # Return top 5 rules

# Function to calculate interest of association rules
def calculate_interest(itemset_I, item_j,frequent_items, frequent_triples, frequent_pairs, total_transactions):
    # Calculate confidence of the association rule I -> j
    confidence = calculate_confidence(itemset_I, [item_j], frequent_triples, frequent_pairs)
    
    # Calculate support of j
    support_j = frequent_items.get(item_j, 0)
    # Calculate fraction of baskets that contain j
    fraction_baskets_containing_j = support_j / total_transactions
    
    # Calculate interest
    interest = confidence - fraction_baskets_containing_j
    
    return interest

# Function to get top rules based on interest
def get_top_rules_by_interest(frequent_items,frequent_triples, frequent_pairs, total_transactions):
    top_rules = []
    
    # Loop through each frequent pair
    for pair, count in frequent_pairs.items():
        I, j = pair
        
        # Calculate interest score for the rule I -> j
        interest_I_j = calculate_interest([I], j, frequent_items,frequent_triples, frequent_pairs, total_transactions)
        
        # Add the rule and its interest score to the list
        top_rules.append((f"{I} -> {j}", interest_I_j))
    
    # Sort the rules based on interest score in descending order
    top_rules.sort(key=lambda x: x[1], reverse=True)
    
    return top_rules[:5]  # Return top 5 rules

# Function to calculate lift of association rules
def calculate_lift(itemset_A, itemset_B,frequent_items ,frequent_triples, frequent_pairs):
    # Calculate support of A and B
    support_A = frequent_pairs.get(tuple(itemset_A), 0)
    support_B = frequent_items.get(tuple(itemset_B)[0], 0)
   
    # Calculate support of A union B
    union_itemset = set(itemset_A).union(set(itemset_B))
    support_A_union_B = frequent_triples.get(tuple(union_itemset), 0)
    
    # Calculate lift
    if support_A != 0 and support_B != 0:
        lift = support_A_union_B / (support_A * support_B)
    else:
        lift = 0
    
    return lift

# Function to calculate lift scores for association rules based on frequent triples
def calculate_lift_for_triples(frequent_items , frequent_triples, frequent_pairs):
    top_rules_lift = []
    
    # Loop through each frequent triple
    for triple, count in frequent_triples.items():
        A, B, C = triple
        
        # Calculate lift scores for the rules (A, B) -> C, (A, C) -> B, and (B, C) -> A
        lift_AB_C = calculate_lift([A, B], [C], frequent_items, frequent_triples, frequent_pairs)
        lift_AC_B = calculate_lift([A, C], [B], frequent_items, frequent_triples, frequent_pairs)
        lift_BC_A = calculate_lift([B, C], [A], frequent_items, frequent_triples, frequent_pairs)
        
        # Add the rules and their lift scores to the list
        top_rules_lift.append((f"({A}, {B}) -> {C}", lift_AB_C))
        top_rules_lift.append((f"({A}, {C}) -> {B}", lift_AC_B))
        top_rules_lift.append((f"({B}, {C}) -> {A}", lift_BC_A))
    
    # Sort the rules based on lift score in descending order
    top_rules_lift.sort(key=lambda x: x[1], reverse=True)
    
    return top_rules_lift[:5]  # Return top 5 rules
# Main function
if __name__ == "__main__":
    # File name
    file_name = "store.csv"
    
    # Minimum support thresholds
    min_support_item = 200
    min_support_pair = 100
    min_support_triple = 75
    
    # Read data from CSV file
    data = read_data(file_name)
    
    total_transactions = len(data)
    # Get frequent items
    frequent_items = get_frequent_items(data, min_support_item)
    
    # Print most frequent items
    print_most_frequent_items(frequent_items, 10)
    
    # Get frequent pairs of items
    frequent_pairs = get_frequent_pairs(data, min_support_pair, frequent_items)
    
    # Print most frequent pairs of items
    print_most_frequent_pairs(frequent_pairs, 10)
    
    # Get frequent triples of items
    frequent_triples = get_frequent_triples(data, min_support_triple, frequent_pairs)
    
    # Print most frequent triples of items
    print_most_frequent_triples(frequent_triples, 10)

    # Get top rules based on confidence
    top_rules = get_top_rules(frequent_triples, frequent_pairs)
    
    # Print the top rules
    print("Top 5 rules based on confidence:")
    for rule, confidence in top_rules:
        print(rule, ":", confidence)

    # Get top rules based on interest
    top_rules_interest = get_top_rules_by_interest(frequent_items , frequent_triples , frequent_pairs, total_transactions)
    
    # Print the top rules based on interest
    print("Top 5 rules based on interest:")
    for rule, interest in top_rules_interest:
        print(rule, ":", interest)

    # Calculate lift scores for association rules based on frequent triples
    top_rules_lift = calculate_lift_for_triples(frequent_items , frequent_triples, frequent_pairs)
    
    # Print the top rules based on lift
    print("Top 5 rules based on lift:")
    for rule, lift in top_rules_lift:
        print(rule, ":", lift)