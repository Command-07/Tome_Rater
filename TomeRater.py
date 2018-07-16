class User():
    def __init__(self, name, email):
        if isinstance(name, str):
            self.name = name
        else:
            print("Name of user has invalid characters")
            raise TypeError
        if isinstance(email, str):
            self.email = email
        else:
            print("Email is of invalid type")
            raise TypeError
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        if isinstance(address, str):
            self.email = address
            print("{}\'s email has been updated".format(self.name))
        else:
            print("The new email you entered is of invalid type")
            raise TypeErrorw

    def __repr__(self):
        return "User: {}, email: {}, books read: {}".format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        rating_sum = 0
        for book_rating in self.books.values():
            if book_rating != None:
                rating_sum += book_rating
        average_rating = rating_sum / len(self.books)
        return average_rating


class Book():
    def __init__(self, title, isbn):
        if isinstance(title, str) and isinstance(isbn, int):
            self.title = title
        else:
            print("Title of the book is of an invalid type")
            raise TypeError
        if isinstance(isbn, int):
            self.isbn = isbn
        else:
            print("ISBN is of invalid type")
            raise TypeError
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, newISBN):
        if isinstance(newISBN, int):
            self.isbn = newISBN
            print("{}\'s ISBN has been updated successfully".format(self.title))
        else:
            print("The new ISBN you entered is of invalid type.")
            raise TypeError

    def add_rating(self, rating):
        if rating >= 0 and rating <= 4:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        total_sum = 0
        for rating in self.ratings:
            total_sum += rating
        return total_sum / len(self.ratings)

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __repr__(self):
        return "Title: {}, ISBN: {}".format(self.title, self.isbn)

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        if isinstance(author, str):
            self.author = author
        else:
            print("The author name is not a string.")
            raise TypeError

    #Returns the author of the book.
    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        if isinstance(subject, str):
            self.subject = subject
        else:
            print("Subject argument is not a string")
            raise TypeError
        if isinstance(level, str):
            self.level = level
        else:
            print("level argument is not a string")
            raise TypeError

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title = self.title, level = self.level, subject = self.subject)


class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}
        self.ISBN_Index = {}

    def create_book(self, title, isbn):
        if isbn not in self.ISBN_Index.keys():
            newBook = Book(title, isbn)
            self.ISBN_Index[isbn] = title
            return newBook
        else:
            print("A book with the ISBN already exists")
            raise DuplicateBook

    def create_novel(self, title, author, isbn):
        if isbn not in self.ISBN_Index.keys():
            newFictionBook = Fiction(title, author, isbn)
            self.ISBN_Index[isbn] = title
            return newFictionBook
        else:
            print("A book with the ISBN already exists")
            raise DuplicateBook

    def create_non_fiction(self, title, subject, level, isbn):
        if isbn not in self.ISBN_Index.keys():
            newNonFictionBook = Non_Fiction(title, subject, level, isbn)
            self.ISBN_Index[isbn] = title
            return newNonFictionBook
        else:
            print("A book with the ISBN already exists")
            raise DuplicateBook

    def add_book_to_user(self, book, email, rating = None):
        if email in self.users.keys():
            self.users[email].read_book(book, rating)
        else:
            print("No user with email {}!".format(email))
        if rating != None:
            book.add_rating(rating)
            if book not in self.books:
                self.books[book] = 1
            else:
                self.books[book] += 1

    def add_user(self, name, email, user_books = None):
        newUser = User(name, email)
        if '@' in email:
            if '.com' in email or '.edu' in email or '.org' in email:
                if not email in self.users.keys():
                    self.users[email] = newUser
                else:
                    print("User already exists")
            else:
                print("Invalid Email Address")
                raise InvalidEmail
        else:
            print("Invalide Email Address")
            raise InvalidEmail
        if user_books != None:
            for book in user_books:
                self.add_book_to_user(book, email)

    def print_catalog(self):
        for key in self.books.keys():
            print(key)

    def print_users(self):
        for value in self.users.values():
            print(value)

    def get_most_read_book(self):
        book_list = list(self.books.keys())
        value_list = list(self.books.values())
        max_value = 0
        for val in value_list:
            if val > max_value:
                max_value = val
        return book_list[value_list.index(max_value)]

    def highest_rated_book(self):
        highest_average = float("-inf")
        for book in self.books.keys():
            if book.get_average_rating() > highest_average:
                highest_average = book.get_average_rating()
        for bookz in self.books.keys():
            if bookz.get_average_rating() == highest_average:
                return bookz

    def most_positive_user(self):
        highest_positive_rating = 0
        for user in self.users.values():
            if user.get_average_rating() > highest_positive_rating:
                highest_positive_rating = user.get_average_rating()
        for userz in self.users.values():
            if userz.get_average_rating() == highest_positive_rating:
                return userz

    def get_n_most_read_books(self, n):
        read_times = list(self.books.values())
        book_objects = list(self.books.keys())
        output_list = []
        for i in range(n):
            maximum_read = max(read_times)
            output_list.append(book_objects[read_times.index(maximum_read)])
            remove_index = read_times.index(maximum_read)
            read_times.pop(remove_index)
            book_objects.pop(remove_index)
        return output_list

    def get_n_most_prolific_readers(self, n):
        users = list(self.users.values())
        output_list = []
        for i in range(n):
            highest_books_read = 0
            user_who_read_it = None
            for user in users:
                number_of_books_read = len(user.books.keys())
                if number_of_books_read > highest_books_read:
                    highest_books_read = number_of_books_read
                    user_who_read_it = user
            output_list.append(user_who_read_it)
            users.pop(users.index(user_who_read_it))
        return output_list

    def __repr__(self):
        return "Number of users: {}, Number of Books: {}".format(len(self.users.values()),len(self.books.keys()))

    def __eq__(self, other):
        same = True
        if len(self.users.values()) != len(other.users.values()):
            return False
        else:
            self_users = list(self.users.values())
            other_users = list(other.users.values())
            for i in range(len(other_users)):
                if other_users[i] not in self_users:
                    same = False
            return same

#Exceptions

class TypeError(Exception):
    """ Input is of different Type"""
    pass


class DuplicateBook(Exception):
    """Trying to add a book that already exists"""
    pass


class InvalidEmail(Exception):
    """Email is not valid. Kindly check and retry."""
    pass
