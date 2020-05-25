import pandas as pd

library = pd.read_csv('library.csv')

class Shelf:

    def __init__(self, library, rating = None, period_of_my_life = None, genre = None, subgenre = None):
        self.shelf = library
        self.rating = rating
        self.period_of_my_life = period_of_my_life
        self.genre = genre
        self.subgenre = subgenre
        self.prune_shelf()
    
    def prune_shelf(self):
        if self.rating is not None:
            self.shelf = self.shelf[self.shelf['rating'] == self.rating]
        if self.period_of_my_life is not None:
            self.shelf = self.shelf[self.shelf['period_of_my_life'] == self.period_of_my_life]
        if self.genre is not None:
            self.shelf = self.shelf[self.shelf['genre'] == self.genre]
        if self.subgenre is not None:
            self.shelf = self.shelf[self.shelf['subgenres'].str.contains(self.subgenre)]
        self.shelf.sort_values(by='author_surname')
    
    def make_page(self):
        id, title = self.make_yaml_attributes()
        page = [
            '---\n',
            'layout: page\n',
            f'title: "{title}"\n',
            'published: true\n',
            f'permalink: /{id}/\n',
            'backlinks: \n',
            '---\n\n'
        ]
        for index, book in self.shelf.iterrows():
            string = f"* {book['author_surname']}, *{book['title']}* ({book['publication_year']})"
            if self.rating is None:
                if book['rating'] == 'loved':
                    string += ' ★'
            page.append(string + '\n')
        return page
    
    def make_yaml_attributes(self):
        if self.rating is not None:
            return f'bookshelf-{self.rating}', f'Bookshelf: {self.rating}'
        if self.period_of_my_life is not None:
            return (
                f'bookshelf-read-in-my-{self.period_of_my_life}', 
                f'Bookshelf: read in my {self.period_of_my_life}'
            )
        if self.genre is not None:
            return (
                f'bookshelf-{self.genre.lower()}', 
                f'Bookshelf: {self.genre}'
            )
        if self.subgenre is not None:
            return (
                f'bookshelf-{self.subgenre.lower().replace(" ", "-").replace("&", "")}', 
                f'Bookshelf: {self.subgenre}'
            )
        else:
            return (
                f'all-books', 
                f'All books'
            )

def write_page(filepath, content):
    """Write a page."""
    with open(filepath, 'w') as f:
        return f.write(content)

all_books = Shelf(library)

for rating in ['loved', 'liked', 'disliked']:
    shelf = Shelf(library, rating=rating)
    id, title = shelf.make_yaml_attributes()
    page = shelf.make_page()
    write_page(filepath=f'pages/{id}.md', content=''.join(page))

for period in ['childhood', 'teens', '20s']:
    shelf = Shelf(library, period_of_my_life=period)
    id, title = shelf.make_yaml_attributes()
    page = shelf.make_page()
    write_page(filepath=f'pages/{id}.md', content=''.join(page))

for genre in ['Fiction', 'Non-Fiction']:
    shelf = Shelf(library, genre=genre)
    id, title = shelf.make_yaml_attributes()
    page = shelf.make_page()
    write_page(filepath=f'pages/{id}.md', content=''.join(page))

subgenres = [
    'Behavioral Economics',
    'Biographies',
    'Business',
    'Comics',
    'Computer Science & Programming',
    'Economics',
    'Essays',
    'Fantasy',
    'Historical Fiction',
    'History',
    'Learning',
    'Literature',
    'Memoirs',
    'Parables',
    'Personal Finance',
    'Philosophy', 
    'Plays',
    'Psychology', 
    'Religion',
    'Science', 
    'Science-Fiction',
    'Self-Help',
    'Short Stories',
    'Westerns',
    'Writing'
]

for subgenre in subgenres:
    shelf = Shelf(library, subgenre=subgenre)
    id, title = shelf.make_yaml_attributes()
    page = shelf.make_page()
    write_page(filepath=f'pages/{id}.md', content=''.join(page))