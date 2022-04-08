import random
import re

class TreeNode:
    def __init__(self, data):
        self.data: str = data
        self.children: list[TreeNode] = list[TreeNode]()
        self.parent: TreeNode or None = None

    def get_data(self):
        return self.data

    def get_children(self):
        return self.children

    def get_parent(self):
        return self.parent

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level

    def print_tree(n, d2, depth=0):
        if not n:
            return
        if depth > d2:
            return
        for chld in n.get_children():
            print("  " * depth + chld.get_data())
            TreeNode.print_tree(chld, d2, depth + 1)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


file = open('dialog.txt', mode='r', encoding='utf-8-sig')
lines = file.readlines()
file.close()

rootNode: TreeNode = TreeNode("")

arrayDict = {}
variableDict = {}

for index, line in enumerate(lines):
    # strip extra whitespace
    line = line.strip()

    if not len(line) == 0 and line[0] != "#" and line[0] != "~" and len(line.split(":")) == 3:

        if line.split(":")[0] == "u":

            newNode = TreeNode(line)
            rootNode.add_child(newNode)

        else:
            # if not add to the previous dictionary as a sub dictionary
            if line.split(":")[0] == "u1":
                line1 = TreeNode(line)
                newNode.add_child(line1)


            elif line.split(":")[0] == "u2":
                line2 = TreeNode(line)
                line1.add_child(line2)


            elif line.split(":")[0] == "u3":
                line3 = TreeNode(line)
                line2.add_child(line3)


            elif  line.split(":")[0] == "u4":
                line4 = TreeNode(line)
                line3.add_child(line4)

            elif  line.split(":")[0] == "u5":
                line4 = TreeNode(line)
                line3.add_child(line4)

            # lineA = TreeNode(line)
            # newRoot.add_child(lineA)
            # continue

    elif line[0] == "~":
        # create a dictionary with ~name: value as a key/value pair
        # can then call random.choice(arrayDict[name]) to get a random string
        nameOfArray = line.split(":")[0].strip("~")
        contentsOfArray = line.split(":")[1].lstrip().rstrip().strip('[]').split(" ")
        arrayDict.update({nameOfArray: contentsOfArray})
        #print(arrayDict)

    elif line[0] == "#":
        continue
    elif len(line.split(":")) != 3:
        print("Syntax error on line " + str(index + 1) + ". This line will be ignored")
    else:
        print("Unknown error on line " + str(index + 1) + ". This line will be ignored")

#print(arrayDict.get("greetings"))

def trim(s: str) -> str:
    return s.lstrip().rstrip().strip("()")
userInput = ""
currentNode: TreeNode or None = None
while userInput.lower() != "bye":
    userInput = input("input: ")
    found = False
    for n in [currentNode, rootNode]:
        if found:
            break
        if n is None:
            continue
        for child in n.get_children():
            if found:
                break
            data = re.match("u[\\d]*\\s?:\\s?\\(([^)]+)", child.get_data())
            #print("'{}' == '{}'\n".format(userInput, data.group(1)))
            if userInput.lower() == data.group(1).lower() or data.group(1).lower().replace("_", "") in userInput.lower() or re.match("^i.am.[\d]*.years.old", userInput.lower()):
                #check when you get rid of the _ and the same position in the string
                currentNode = child
                found = True
                response = trim(child.get_data().split(':')[2])
                if "$" in response:
                    #get the variable name
                    varName = trim(child.get_data().split(':')[2].split("$")[1].split()[0])

                    if "_" in trim(child.get_data().split(':')[1]):

                        holder = str(trim(child.get_data().split(':')[1])).split()
                        #holder = holder.split()
                        #print(holder.index("_"))
                        indexOf = holder.index("_")
                        if userInput.split()[indexOf]:
                            varContent = str(userInput.split()[indexOf])
                        else:
                            varContent = " : you didnt give a name"
                    #gets the last thing in the string
                    #varContent = userInput.split()[-1]
                    #TODO HERHEHRHE

                    variableDict.update({varName: varContent})
                    #print(variableDict)
                    #print("robot: " + str(response).split("$")[0] + variableDict.get(varName))

                    print("robot: " + str(response.replace("$" + varName, varContent)))


                elif "~" in response:
                    getName = response.split("~")[1]
                    print("robot: " + str(random.choice(arrayDict.get(getName))))
                elif "[" in response:
                    print("robot: " + str(random.choice(response.strip("[]").split())))
                else:
                    print("robot: " + str(response))


    # for n in [currentNode, rootNode]:
    #     if n is None:
    #         continue
    #     for i in n.get_children():
    #         split = str(i.get_data()).split(":")
    #         human = trim(split[1])
    #         response = trim(split[2])
    #         # words = list(map(str, response.split()))
    #         # respone = list(map())
    #         if "~" in human:
    #             dictLookup = human.strip("~")
    #             # print(arrayDict[dictLookup])
    #             if currentNode and userInput in currentNode.get_children():
    #                 pass
    #             if userInput in arrayDict[dictLookup]:
    #                 if "[" in response:
    #                     words = list(map(str, response.strip("[]").split()))
    #                     # response = response.strip("[]")
    #                     print(random.choice(words))
    #
    #         elif "_" in human and human.strip("_") in userInput:
    #             key = response.split("$")[1]
    #             variable = userInput.split()[-1]
    #             arrayDict.update({key: variable})
    #
    #             print(str(response.split("$")[0]) + str(arrayDict[key]))
    #
    #         else:
    #             res = None
    #             for kid in i.get_children():
    #                 import re
    #                 data = re.match("u[\\d]*\\s?:\\s?\\(([^)]+)", kid.get_data())
    #                 print("'{}' == '{}'\n".format(userInput, data.group(1)))
    #                 if userInput == data.group(1):
    #                     print("Match")
    #                     currentNode = kid
    #                     res = data.group(1)
    #                     break
    #             # res = None
    #             # if currentNode:
    #             #     for child in currentNode.get_children():
    #             #         if child.get_data() is userInput:
    #             #             currentNode = child
    #             #             res = currentNode.get_data()
    #             #             break
    #             # if res is None:
    #             #     for child in treeArray:
    #             #         import re
    #             #         data = re.match("u[\\d]*\\s?:\\s?\\(([^)]+)", child.get_data())
    #             #         if userInput == data.group(1):
    #             #             currentNode = child
    #             #             res = data.group(1)
    #             #             break
    #
    #             if res is None:
    #                 continue
    #             else:
    #                 print(response)
    #                 print("Current: {} {}".format(currentNode.get_data(), len(currentNode.get_children())))
    #                 for node in currentNode.get_children():
    #                     print("Child: {}".format(node.get_data()))
    #                 break
