import difflib
import filecmp

def display_diff(file1, file2):
    with open(file1, 'r',encoding='iso-8859-1') as f1,open(file2, 'r',encoding='iso-8859-1') as f2:
        file_1 = f1.readlines()
        file_2 = f2.readlines()

    d=difflib.Differ()
    diff=list((d.compare(file_1, file_2)))
    print("The differences between the two files is:")
    for line in diff:
        print(line)

choice=input("Enter your choice: ")
if choice=="1":
    text1=input("Enter text 1: ")
    text2=input("Enter text 2: ")
    if text1==text2:
        print("Text 1 equals Text 2")
    else:
        print("Text 1 does not equal Text 2")
    sim=difflib.SequenceMatcher(None, text1, text2)
    similarity_ratio=sim.ratio()
    print(f"The similarity ratio is : {similarity_ratio:.2f}")


    words1=text1.split()
    words2=text2.split()

    word_count1=len(words1)
    word_count2=len(words2)

    print("The word count of text1 is :",word_count1)
    print("The word count of text2 is :",word_count2)

elif choice=="2":
    f1=input("Enter file 1: ")
    f2=input("Enter file 2: ")
    result=filecmp.cmp(f1,f2,shallow=False)
    if result:
        print("File 1 equals File 2")
        print(result)

    else:
        print("File 1 does not equal File 2")
        display_diff(f1,f2)









