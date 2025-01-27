import csv

# Global BST root
ownerRoot = None

########################
# 0) Read from CSV -> HOENN_DATA
########################


def read_hoenn_csv(filename):
    """
    Reads 'hoenn_pokedex.csv' and returns a list of dicts:
      [ { "ID": int, "Name": str, "Type": str, "HP": int,
          "Attack": int, "Can Evolve": "TRUE"/"FALSE" },
        ... ]
    """
    data_list = []
    with open(filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=',')  # Use comma as the delimiter
        first_row = True
        for row in reader:
            # It's the header row (like ID,Name,Type,HP,Attack,Can Evolve), skip it
            if first_row:
                first_row = False
                continue

            # row => [ID, Name, Type, HP, Attack, Can Evolve]
            if not row or not row[0].strip():
                break  # Empty or invalid row => stop
            d = {
                "ID": int(row[0]),
                "Name": str(row[1]),
                "Type": str(row[2]),
                "HP": int(row[3]),
                "Attack": int(row[4]),
                "Can Evolve": str(row[5]).upper()
            }
            data_list.append(d)
    return data_list


HOENN_DATA = read_hoenn_csv("hoenn_pokedex.csv")

########################
# 1) Helper Functions
########################

def read_int_safe(prompt):
    """
    Prompt the user for an integer, re-prompting on invalid input.
    """
    return int(input(prompt))
    pass

def get_poke_dict_by_id(poke_id):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by ID, or None if not found.
    """
    pass

def get_poke_dict_by_name(name):
    """
    Return a copy of the Pokemon dict from HOENN_DATA by name, or None if not found.
    """
    pass

def display_pokemon_list(poke_list):
    """
    Display a list of Pokemon dicts, or a message if empty.
    """
    pass


########################
# 2) BST (By Owner Name)
########################

def create_owner_node(owner_name, first_pokemon=None):
    """
    Create and return a BST node dict with keys: 'owner', 'pokedex', 'left', 'right'.
    """
    return {'owner': owner_name, 'pokedex': first_pokemon, 'left': None , 'right': None}

def insert_owner_bst(root, new_node):
    """
    Insert a new BST node by owner_name (alphabetically). Return updated root.
    """
    # init new tree
    if root is None:
        return new_node
    # find the correct placement for the new node
    if root['owner'] == new_node['owner']:
        return root
    elif root['owner'] < new_node['owner']:
        root['right'] = insert_owner_bst(root['right'], new_node)
    else:
        root['left'] = insert_owner_bst(root['left'], new_node)
    return root

def find_owner_bst(root, owner_name):
    """
    Locate a BST node by owner_name. Return that node or None if missing.
    """
    # if not found return None
    if root is None:
        return None
    # go over all nodes and try to find the name in one of them
    if root['owner'].lower() == owner_name.lower():
        return root
    elif root['owner'].lower() > owner_name.lower():
        return find_owner_bst(root['left'], owner_name)
    else:
        return find_owner_bst(root['right'], owner_name)

def min_node(node):
    """
    Return the leftmost node in a BST subtree.
    """
    pass

def delete_owner_bst(root, owner_name):
    """
    Remove a node from the BST by owner_name. Return updated root.
    """
    pass


########################
# 3) BST Traversals
########################

def bfs_traversal(root):
    """
    BFS level-order traversal. Print each owner's name and # of pokemons.
    """
    pass

def pre_order(root):
    """
    Pre-order traversal (root -> left -> right). Print data for each node.
    """
    pass

def in_order(root):
    """
    In-order traversal (left -> root -> right). Print data for each node.
    """
    pass

def post_order(root):
    """
    Post-order traversal (left -> right -> root). Print data for each node.
    """
    pass


########################
# 4) Pokedex Operations
########################

def add_pokemon_to_owner(owner_node):
    """
    Prompt user for a Pokemon ID, find the data, and add to this owner's pokedex if not duplicate.
    """
    # get an id from the user
    pokemon_id = read_int_safe("Enter Pokemon ID to add: ")
    if not 1 <= pokemon_id <= 135:
        print("ID", pokemon_id, "not found in Honen data.\n")
        return owner_node

    # if pokemon is already in the pokedex
    if any(pokemon_id == pokemon['ID'] for pokemon in owner_node['pokedex']):
        print("Pokemon already in the list. No changes made.\n")
        return owner_node

    # if valid - insert to the pokedex
    owner_node['pokedex'].append(HOENN_DATA[pokemon_id - 1])
    print("Pokemon",HOENN_DATA[pokemon_id - 1]['Name']
          ,"(ID", pokemon_id,
          ") added to",owner_node['owner'],"'s Pokedex.\n")
    return owner_node

def release_pokemon_by_name(owner_node):
    """
    Prompt user for a Pokemon name, remove it from this owner's pokedex if found.
    """
    poke_name = input("Enter Pokemon Name to release: ")
    # check if the given name is in the pokedex
    for pokemon in owner_node['pokedex']:
        if pokemon['Name'].lower() == poke_name.lower():
            # if found - remove from the pokedex
            print("Releasing",poke_name,"from",owner_node['owner'],".\n")
            owner_node['pokedex'].remove(pokemon)
            return
    # if the pokemon was not found
    print("No Pokemon named'",poke_name,"'in op's Pokedex.\n")
    return

def evolve_pokemon_by_name(owner_node):
    """
    Evolve a Pokemon by name:
    1) Check if it can evolve
    2) Remove old
    3) Insert new
    4) If new is a duplicate, remove it immediately
    """
    name_to_evolve = input("Enter Pokemon Name to evolve: ")
    # check if the pokemon is in the owner's pokedex
    is_found = False
    evolution_flag = False
    for pokemon in owner_node['pokedex']:
        # if pokemon is found by name
        if name_to_evolve.lower() == pokemon['Name'].lower():
            # pokemon was found
            is_found = True
            pokemon_id = pokemon['ID']
            # check if pokemon can evolve
            if pokemon['Can Evolve'] == 'TRUE':
                # check if the evolved form was already in the pokedex
                if HOENN_DATA[pokemon_id] in owner_node['pokedex']:
                    evolution_flag = True

                # evolve the pokemon
                owner_node['pokedex'].append(HOENN_DATA[pokemon_id])  # insert to pokedex
                owner_node['pokedex'].remove(pokemon)  # remove from pokedex
                print("Pokemon evolved from", pokemon['Name'], "(ID",pokemon_id,") to",
                      HOENN_DATA[pokemon['ID']]['Name'],"(ID",pokemon_id + 1,").\n")

                # if the evolved form was already in the pokedex release it at once
                if evolution_flag:
                    print(HOENN_DATA[pokemon_id]['Name'], "was already present; releasing it immediately.\n")
                    owner_node['pokedex'].pop(-1)
                return
            # if pokemon cannot evolve
            else:
                print(pokemon['Name'],"cannot evolve.\n")
                return
    # if the pokemon was not found in the pokedex
    if not is_found:
        print("No Pokemon named '",name_to_evolve,"' in",owner_node['owner'],"'s Pokedex.\n")
        return

    pass


########################
# 5) Sorting Owners by # of Pokemon
########################

def gather_all_owners(root, arr):
    """
    Collect all BST nodes into a list (arr).
    """
    pass

def sort_owners_by_num_pokemon():
    """
    Gather owners, sort them by (#pokedex size, then alpha), print results.
    """
    pass


########################
# 6) Print All
########################

def print_all_owners():
    """
    Let user pick BFS, Pre, In, or Post. Print each owner's data/pokedex accordingly.
    """
    pass

def pre_order_print(node):
    """
    Helper to print data in pre-order.
    """
    pass

def in_order_print(node):
    """
    Helper to print data in in-order.
    """
    pass

def post_order_print(node):
    """
    Helper to print data in post-order.
    """
    pass


########################
# 7) The Display Filter Sub-Menu
########################

def display_filter_sub_menu(owner_node):
    """
    1) Only type X
    2) Only evolvable
    3) Only Attack above
    4) Only HP above
    5) Only name starts with
    6) All
    7) Back
    """
    while True:
        prompt = "-- Display Filter Menu --\n" \
              + "1. Only a certain Type\n" \
              + "2. Only Evolvable\n" \
              + "3. Only Attack above __\n" \
              + "4. Only HP above __\n" \
              + "5. Only names starting with letter(s)\n" \
              + "6. All of them!\n" \
              + "7. Back\n" \
              + "Your choice: "
        display_choice = read_int_safe(prompt)
        match display_choice:
            # only a certain type
            case 1:
                flag = False
                type_to_print = input("Which Type? (e.g. GRASS, WATER): ")
                for pokemon in owner_node['pokedex']:
                    # check if the type is the same word as the required type
                    if pokemon['Type'].lower() == type_to_print.lower():
                        flag = True
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                # if a pokemon has not been printed
                if not flag:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                print("\n")
                continue
            # only evolvable
            case 2:
                flag = False
                for pokemon in owner_node['pokedex']:
                    # check if pokemon can evolve
                    if pokemon['Can Evolve'] == 'TRUE':
                        flag = True
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                # if a pokemon has not been printed
                if not flag:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                continue
            # only attack above __
            case 3:
                flag = False
                prompt = "Enter Attack threshold: "
                threshold = read_int_safe(prompt)
                for pokemon in owner_node['pokedex']:
                    # check if pokemon has higher atk than the threshold
                    if pokemon['Attack'] > threshold:
                        flag = True
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                # if a pokemon has not been printed
                if not flag:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                continue
            # only HP above __
            case 4:
                flag = False
                prompt = "Enter HP threshold: "
                threshold = read_int_safe(prompt)
                for pokemon in owner_node['pokedex']:
                    # check if pokemon has higher atk than the threshold
                    if pokemon['HP'] > threshold:
                        flag = True
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                # if a pokemon has not been printed
                if not flag:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                continue
            # only names beginning with a given letter
            case 5:
                flag = False
                letter = input("Starting letter(s): ")
                for pokemon in owner_node['pokedex']:
                    # check if a pokemon's name starts with the given letter
                    if pokemon['Name'].lower().startswith(letter):
                        flag = True
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                # if a pokemon has not been printed
                if not flag:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                continue
            # all of them
            case 6:
                # checks if the pokedex is empty
                if not owner_node['pokedex']:
                    print("There are no Pokemons in this Pokedex that match the criteria.\n")
                # print all pokemon in the owner's pokedex
                else:
                    for pokemon in owner_node['pokedex']:
                        # take every key and value of a pokemon, pair them and add ',' between every pair
                        stat_print_format = [f"{key}: {value}" for key, value in pokemon.items()]
                        print(", ".join(stat_print_format))
                    print("\n")
                continue
            # back
            case 7:
                print("Back to Pokedex Menu.\n")
                break
            case _:
                print("Invalid choice.\n")
                continue
    pass


########################
# 8) Sub-menu & Main menu
########################

def existing_pokedex():
    """
    Ask user for an owner name, locate the BST node, then show sub-menu:
    - Add Pokemon
    - Display (Filter)
    - Release
    - Evolve
    - Back
    """
    global ownerRoot
    owner_name = input("Owner name: ")
    owner = find_owner_bst(ownerRoot, owner_name)

    # if the owner is found - go to pokedex menu
    if owner is not None:
        while True:
            prompt = "--" + owner_name + "'s Pokedex Menu --\n" \
                     + "1. Add Pokemon\n" \
                     + "2. Display Pokedex\n" \
                     + "3. Release Pokemon\n" \
                     + "4. Evolve Pokemon\n" \
                     + "5. Back to Main\n" \
                     + "Your choice: "
            menu_choice = read_int_safe(prompt)
            match menu_choice:
                # add a pokemon
                case 1:
                    owner = add_pokemon_to_owner(owner)
                    continue
                # display pokemon
                case 2:
                    display_filter_sub_menu(owner)
                    continue
                # release pokemon
                case 3:
                    release_pokemon_by_name(owner)
                    continue
                # evolve pokemon
                case 4:
                    evolve_pokemon_by_name(owner)
                    continue
                # return to menu
                case 5:
                    print("Back to Main Menu.\n")
                    break
                case _:
                    print("Invalid choice.\n")
                    continue
    # if the owner is not found print message and go back
    else:
        print("Owner ", owner_name , " not found.\n")
        return

    pass

def main_menu():
    """
    Main menu for:
    1) New Pokedex
    2) Existing Pokedex
    3) Delete a Pokedex
    4) Sort owners
    5) Print all
    6) Exit
    """
    print("=== Main Menu ===\n"
          "1. New Pokedex\n"
          "2. Existing Pokedex\n"
          "3. Delete a Pokedex\n"
          "4. Display owners by number of Pokemon\n"
          "5. Print All\n"
          "6. Exit\n")
    pass

def new_pokedex():
    global ownerRoot
    # get name from user
    name = input("Owner name: ")
    if ownerRoot is not None and name in ownerRoot:
        print("Owner '" , name, "' already exists. No new Pokedex created.")
        return

    # ask for a starter choice
    prompt = ("Choose your starter Pokemon:\n"
                                   "1) Treecko\n"
                                   "2) Torchic\n"
                                   "3) Mudkip\n"
                                   "Your choice: ")
    starter_choice = read_int_safe(prompt)

    # check outcome based on starter choice
    match starter_choice:
        case 1:
            new_owner = create_owner_node(name)
            # make pokedex a list starting with Treecko
            new_owner['pokedex'] = [HOENN_DATA[0]]
            pass
        case 2:
            new_owner = create_owner_node(name)
            # make pokedex a list starting with Torchic
            new_owner['pokedex'] = [HOENN_DATA[3]]
            pass
        case 3:
            new_owner = create_owner_node(name)
            # make pokedex a list starting with Mudkip
            new_owner['pokedex'] = [HOENN_DATA[6]]
            pass
        case _:
            print("Invalid. No new Pokedex created.\n")
            return

    # insert the new node to owners tree
    ownerRoot = insert_owner_bst(ownerRoot, new_owner)
    print("New Pokedex created for", name, "with starter", new_owner['pokedex'][0]['Name'] ,".")
    return


def main():
    "Entry point: calls main_menu()."

    while True:
        main_menu()
        choice = read_int_safe("Your choice: ")
        match choice:
            # create a new pokedex
            case 1:
                new_pokedex()
                continue
            # enter a pokedex
            case 2:
                if ownerRoot is None:
                    print("No owners at all.\n")
                else:
                    existing_pokedex()
                continue
            # delete a pokedex
            case 3:
                continue
            # display owners by number of pokemon
            case 4:
                continue
            # print all owners
            case 5:
                continue
            # exit
            case 6:
                print("Goodbye!\n")
                break
            # default case
            case _:
                print("Invalid choice.\n")
                continue

if __name__ == "__main__":
    main()
