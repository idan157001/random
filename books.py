
class Books:
    def __init__(self,book:str):
        self.books_list = ['Python','C','Javascript','Shell']
        self.book = book.capitalize()

    def ask_for_password(self,action:str) -> bool:
        print('* This action is password protected  *\n')
        print(f'\t{action} Action\n')

        password = input("Enter Password ")
        if password == '1234':
            return True
        else:
            return False

    def book_in_list(self) -> bool:
        for book_name in self.books_list:
            if book_name == self.book:
                return True
        return False

    def add_book(self):
        if self.ask_for_password('Add Book') is False:
            return

        if self.book_in_list():
            return f'{self.book} is already in books list'

        self.books_list.append(self.book)
        return f'{self.book} added to books list\n{self.books_list}'

    def remove_book(self):
        if self.ask_for_password('Remove Book') is False:
            return
  
        if self.book_in_list() is False:
            return

        self.books_list.remove(self.book)
        return f'{self.book} removed from books list\n{self.books_list}'


book_name = input('Enter Books Name ')
x = Books(book_name)
#print(x.add_book())
print(x.remove_book())