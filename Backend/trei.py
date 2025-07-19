class Node:
    def __init__(self):
        self.childern={}
        self.end_of_word=False


class Trie:
    def __inint__(self):
        self.root=Node()



    def insert(self,word:str):
        current=self.root
        for character in word:
            if character not in current.childern:
                current.childern[character]=Node()

            current=current.childern[character]

        current.end_of_word=True


    def search(self,word):
        current=self.root
        for character in word:
            if character not in current.childern():
                return False

            current=current.childern[character]
            return current.end_of_word


    def starts_with(self,prefix:str):
        current=self.root
        for character in prefix:
            if character in current.children():
                return False

            current=current.childern[character]

        return True
