#!/usr/bin/env python

# 29.04.2023
# YiffMap V4.0

from colorama import Fore
from sys import argv
from tools import Map, check_arguments


SPLASH_SCREEN = """
YiffMap V4.0
Made by Klue
"""



def main():
    # Check arguments
    check_arguments(argv)
    data_file = argv[1]
    output_file = argv[2]

    print(SPLASH_SCREEN)
    # 1) Initialisation...
    map = Map(data_file, True)
    # 2) Check the contents of the file
    map.check_file_contents()
    # 3) Display statistics
    map.display_stats()
    # 4) Create the graph
    map.graph(output_file)
    


if __name__ == '__main__':
    main()


    













# ## Make normalized relation list (only 2-people links with information if they were 2,3,etc... at the beginning)
# # Also adds a hash corresponding to each relation
# relations_normalized = {}
# for r in relations:
    
#     ind = r[RELATIONS_INDIVIDUALS_KEY]
#     try:
#         privacy = r[RELATIONS_PRIVACY_KEY]
#     except KeyError as e:
#         print(colored(255,0,0,f"Missing privacy key from relation {ind}"))
#     else:
#         privacy = 2

#     #print(f"relation : {ind}")
    
#     tier = len(ind)
#     if tier == 2:
#         hash = "0x00000000"
#     else:
#         text_to_hash = '-'.join(ind)
#         hash = hex(zlib.crc32(text_to_hash.encode()))

#     for a in ind:
#         for b in ind:
#             if b != a:
#                 people  = [a, b]
#                 people.sort() # sort the relation, allows to remove duplicates

#                 weight = 1/(tier-1)
#                 #weight = 1

#                 name = '@'.join(people)

#                 if name in relations_normalized.keys():
#                     # Normalized relation already exists
#                     if relations_normalized[name][0] < weight:
#                         # Adjust the weight
#                         relations_normalized[name][0] = weight
#                 else:
#                     # The relation doesn't exist
#                     relations_normalized[name] = [weight, tier, hash, privacy]
                    

# print(f"    {len(relations_normalized)} normalized relations")

# # Export to csv files
# ## Individuals
# with open(individuals_file, 'w', newline='', encoding='utf-8') as f:
#     csvwriter = csv.writer(f)
#     # Write header
#     csvwriter.writerow(["Id", "Label", "Country code", "Species"])
#     # Write data
#     for i in individuals:
#         country_code = i[INDIVIDUALS_COUNTRY_CODE_KEY] if INDIVIDUALS_COUNTRY_CODE_KEY in i else ""
#         csvwriter.writerow([i[INDIVIDUALS_NAME_KEY], i[INDIVIDUALS_NAME_KEY], country_code, i[INDIVIDUALS_SPECIES_KEY]])

# ## Relations
# with open(relations_file, 'w', newline='', encoding='utf-8') as f:
#     csvwriter = csv.writer(f)

#     # Write header
#     csvwriter.writerow(["Source", "Target", "Weight", "Tier", "Hash", "Privacy"])

#     for name, values in relations_normalized.items():
#         people = name.split('@')
#         csvwriter.writerow([*people, *values])