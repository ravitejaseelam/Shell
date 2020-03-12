import json
import sys
import os
import os.path


def ask_which_to_keep(each1, each2, dic):
    print("\nSame priority is encountered Plz handle by giving which one to keep\n")
    print(json.dumps(each1, indent=4))
    print(json.dumps(each2, indent=4))
    name = input("Enter name to be inserted")
    if each1["name"] == name:
        dic[each1['Id']] = each1
    elif each2["name"] == name:
        dic[each2['Id']] = each2
    else:
        print("Name not found plz enter the correct name ")
    return dic


def check(each, dic):
    if each['priority'] < dic[each['Id']]['priority']:
        dic[each['Id']] = each
    elif each['priority'] == dic[each['Id']]['priority']:
        dic = ask_which_to_keep(each, dic[each['Id']], dic)
    return dic


def is_file_exist_check(filename):
    if not os.path.isfile(filename):
        print(filename + ' File dosent exist')
        sys.exit(0)


def is_file_empty_check(filename):
    if os.path.getsize(filename) == 0:
        print('File is empty')
        sys.exit(1)


def load_json_data_from_file(filename):
    with open(filename, 'r') as f:
        return [json.loads(line) for line in f]


def get_duplicates(x):
    x = [i for i in x if i['healthchk_enabled'] == True]
    t = [each['Id'] for each in x]
    duplicates = [item for item in t if t.count(item) > 1]
    t = [each for each in x if each['Id'] in duplicates]
    return t


def print_if_duplicates(t):
    if len(t) != 0:
        sorted_data = sort_when_healthchk_enbled(t)
        print("These are the Duplicate Data in provided file" + filename)
        print(json.dumps(sorted_data, indent=4))
        return True
    return False


def remove_duplicates(x):
    dic = {}
    for each in x:
        if each['Id'] not in dic:
            dic[each['Id']] = each
        else:
            dic = check(each, dic)
    return dic.values()


def sort_when_healthchk_enbled(x):
    x = [i for i in x if i['healthchk_enabled'] == True]
    return sorted(x, key=lambda k: (k['priority'], int(k["Id"]), k["name"]))


def load_json_data_into_file(outputfilename, lines):
    json_object = json.dumps(lines, indent=4)
    with open(outputfilename, "w") as outfile:
        outfile.write(json_object)


def verify_arguments():
    if len(sys.argv) < 3:
        print(
            "Plz provide requires arguments in command line example(python " + sys.argv[0] + " source.json output.json")
        exit(3)
    elif len(sys.argv) > 3:
        print("Extra arguments found in command line Plz look into an example(python " + sys.argv[
            0] + " source.json output.json")
        exit(3)


def delete_object_from_conflicts(t, name, id):
    for i in t:
        if i["name"] == name and i["Id"] == id:
            t.remove(i)
            return t
    return t


def delete_object_from_original(x, name, id):
    for i in x:
        if i["name"] == name and i["Id"] == id:
            x.remove(i)
            return x


def get_id_conflicts(conflict):
    Ids = []
    for i in conflict:
        Ids.append(i["Id"])
    return Ids


verify_arguments()

filename = sys.argv[1]
outputfilename = sys.argv[2]

is_file_exist_check(filename)

is_file_empty_check(filename)

original = load_json_data_from_file(filename)

conflict = get_duplicates(original)

i = print_if_duplicates(conflict)

if i:
    resp = input("Do you want to the duplicates to be deleted? (y/n)")
    if resp == 'y':
        resp2 = input("By default the priority with high number is deleted to you want to proceed? (y/n)")
        if resp2 == 'y':
            original = remove_duplicates(original)
        elif resp2 == 'n':
            while len(conflict) != 0:
                print_if_duplicates(conflict)
                print("\nPLZ RESOLVE CONFLICTS ONE BY ONE BY GIVING NAME AND ID FROM ABOVE OBJECTS\n")
                Ids = get_id_conflicts(conflict)
                Ids=set(Ids)
                if (len(Ids) > 1):
                    Id = input("Enter id to be handled:")
                else:
                    Id = Ids.pop()
                print(Id+" is selected to be handled")
                Names = input("Enter names to be deleted:").split(",")
                for Name in Names:
                    conflict_dup = conflict.copy()
                    conflict = delete_object_from_conflicts(conflict, Name, Id)
                    if conflict == conflict_dup:
                        print("\nIncorrect name and id \nPlz try id and name only from above printed objects\n")
                    else:
                        original = delete_object_from_original(original, Name, Id)
                        conflict = get_duplicates(conflict)
                        print("\nSuccessfully deleted " + Name + " from conflict created by id:" + Id + "\n")

        else:
            print("Wrong Input it should be either y or n be carefull with case")
            sys.exit(0)

    elif resp == 'n':
        pass
    else:
        print("Wrong Input it should be either y or n be carefull with case")
        sys.exit(0)

lines = sort_when_healthchk_enbled(original)

load_json_data_into_file(outputfilename, lines)

print("Process Done Plz find the output in file " + outputfilename)
