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
        for i in range(len(basket)):
            for j in range(i+1, len(basket)):
                for k in range(j+1, len(basket)):
                    item1 = basket[i]
                    item2 = basket[j]
                    item3 = basket[k]

                    triple = tuple(sorted([item1,item2,item3]))
                    if triple in triple_counts:
                            triple_counts[triple] += 1
                    else:
                            triple_counts[triple] = 1

    # Filtering frequent triples based on minimum support
    frequent_triples = {triple: count for triple, count in triple_counts.items() if count >= min_support}
    # print(frequent_triples)
   
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


def get_top_rules_by_confidence(frequent_triples, frequent_pairs):
    top_rules = []
    
    # Loop through each frequent triple
    for triple in frequent_triples:
        A, B, C = triple
        # print(triple)
        support_A_B = frequent_pairs.get((A, B), frequent_pairs.get((B,A),0))
        support_A_C = frequent_pairs.get((A, C), frequent_pairs.get((C,A),0))
        support_B_C = frequent_pairs.get((B, C), frequent_pairs.get((C,B),0))
        confidence_AB_C = frequent_triples.get((A, B, C), 0) / support_A_B if support_A_B != 0 and frequent_triples.get((A, B, C), 0) < support_A_B  else 0
        confidence_AC_B = frequent_triples.get((A, B, C), 0) / support_A_C if support_A_C != 0 and frequent_triples.get((A, B, C), 0) < support_A_C else 0
        confidence_BC_A = frequent_triples.get((A, B, C), 0) / support_B_C if support_B_C != 0 and frequent_triples.get((A, B, C), 0) < support_B_C else 0

        # Get support_A from frequent_pairs
        
        # print((A,B))
        # Get support_A_union_B from frequent_triples
        # support_A_union_B = frequent_triples.get(triple, 0)
        # print(support_A_union_B)
        # Calculate confidence
        # if support_A != 0:
        #     confidence_AB_C = support_A_union_B / support_A
        # else:
        #     confidence_AB_C = 0
        
        # Calculate confidence for other permutations
        # confidence_AC_B = frequent_triples.get((A, C, B), 0) / support_A if support_A != 0 else 0
        # confidence_BC_A = frequent_triples.get((B, C, A), 0) / support_A if support_A != 0 else 0
        # confidence_AB_C = frequent_triples.get((A, B, C), 0) / support_A if support_A != 0 else 0
        
        # Append rules and their confidences to top_rules list
        top_rules.append((f"({A}, {B}) -> {C}", confidence_AB_C))
        top_rules.append((f"({A}, {C}) -> {B}", confidence_AC_B))
        top_rules.append((f"({B}, {C}) -> {A}", confidence_BC_A))
        # if triple == ('ground beef', 'mineral water', 'spaghetti'):
        #     print(frequent_triples.get((A, B, C), 0))
        #     print( B , C ,A ,confidence_BC_A)
            # print(support_A_union_B ,',',support_A)
    # Sort the rules based on confidence score in descending order
    top_rules.sort(key=lambda x: x[1], reverse=True)
    
    return top_rules[:5]


# Function to calculate interest of association rules
def calculate_interest(itemset_I, item_j,frequent_items, frequent_triples, frequent_pairs, total_transactions):
    # Calculate confidence of the association rule I -> j
    # confidence = calculate_confidence(itemset_I, [item_j], frequent_triples, frequent_pairs)
    
    triple = (itemset_I[0],itemset_I[1],item_j)
    pair = (itemset_I[0],itemset_I[1])
    support_pair = frequent_pairs.get(pair , frequent_pairs.get((itemset_I[0],itemset_I[1]) , 0))
    confidence = frequent_triples.get(tuple(triple),0) / support_pair if support_pair!=0 else 0
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
    for pair, count in frequent_triples.items():
        A,B,C = pair
        
        # Calculate interest score for the rule I -> j
        interest_AB_C = calculate_interest([A,B], C, frequent_items,frequent_triples, frequent_pairs, total_transactions)
        interest_AC_B = calculate_interest([A,C], B, frequent_items,frequent_triples, frequent_pairs, total_transactions)
        interest_BC_A = calculate_interest([C,B], A, frequent_items,frequent_triples, frequent_pairs, total_transactions)
        # print(I)
        # Add the rule and its interest score to the list
        top_rules.append((f"{A,B} -> {C}", interest_AB_C))
        top_rules.append((f"{A,C} -> {B}", interest_AC_B))
        top_rules.append((f"{C,B} -> {A}", interest_BC_A))
    
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
    # print(union_itemset ,':' , support_A_union_B)
    
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
    top_rules = get_top_rules_by_confidence(frequent_triples, frequent_pairs)
    
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
    top_rules_lift = calculate_lift_for_triples(frequent_items , frequent_triples , frequent_pairs)
    
    # Print the top rules based on lift
    print("Top 5 rules based on lift:")
    for rule, lift in top_rules_lift:
        print(rule, ":", lift)











'''''
# Function to calculate confidence score of association rules
def calculate_confidence(itemset_A, itemset_B, frequent_triples, frequent_pairs):
    # Join A and B to create the union itemset
    union_itemset = set(itemset_A).union(set(itemset_B))
    # union_itemset = itemset_A + itemset_B
    # # Calculate support of A and B
    
    # if union_itemset in frequent_triples.items():
    #     support_A_union_B = frequent_triples.get(tuple(union_itemset), 0)
    #     support_A = frequent_pairs.get(tuple(itemset_A), 0)
    # # print(support_A)
    # Convert union_itemset to a tuple
    union_itemset_tuple = tuple(union_itemset)
    
    # Check if union_itemset_tuple is in frequent_triples keys
    if union_itemset_tuple in frequent_triples:
       
        # If it exists, get the support value
        support_A_union_B = frequent_triples[union_itemset_tuple]
        support_A = frequent_pairs.get(tuple(itemset_A), 0)
    
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
    
    return top_rules[:5]   # Return top 5 rules
    '''     