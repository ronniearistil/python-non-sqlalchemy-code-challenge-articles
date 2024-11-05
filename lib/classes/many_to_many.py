class Article:
    all = []  # Tracks all instances of Article

    def __init__(self, author, magazine, title):
        self.author = author  # Will use the setter below
        self.magazine = magazine  # Will use the setter below
        self.title = title  # Will use the setter below
        type(self).all.append(self)  # Add instance to Article.all

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not hasattr(self, '_title'):  # Only set at birth
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value
            else:
                raise ValueError("Title must be a string between 5 and 50 characters.")
        else:
            raise AttributeError("Title is immutable and cannot be changed.")

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise TypeError("Author must be an instance of Author class.")

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise TypeError("Magazine must be an instance of Magazine class.")


class Author:
    all = []  # Tracks all instances of Author

    def __init__(self, name):
        self.name = name  # Will use the setter below
        type(self).all.append(self)  # Add instance to Author.all

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not hasattr(self, '_name'):  # Set name only once
            if isinstance(value, str) and len(value) > 0:
                self._name = value
            else:
                raise ValueError("Name must be a non-empty string.")
        else:
            raise AttributeError("Name is immutable and cannot be changed.")

    def articles(self):
        # Returns articles written by this author
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        # Returns unique magazines the author has written for
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        # Creates and returns a new Article associated with this author and a specified magazine
        return Article(self, magazine, title)

    def topic_areas(self):
        # Returns unique list of magazine categories the author has written for
        return list({magazine.category for magazine in self.magazines()}) if self.articles() else None


class Magazine:
    all = []  # Tracks all instances of Magazine

    def __init__(self, name, category):
        self.name = name  # Uses setter for validation
        self.category = category  # Uses setter for validation
        type(self).all.append(self)  # Adds instance to Magazine.all

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Allows updates to name, with validation
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Allows updates to category, with validation
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string.")

    def articles(self):
        # Returns articles published in this magazine
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        # Returns unique authors who have written articles for this magazine
        return list({article.author for article in self.articles()})

    def article_titles(self):
        # Returns a list of titles for articles in this magazine
        return [article.title for article in self.articles()] if self.articles() else None

    def contributing_authors(self):
        # Returns authors with more than 2 articles in this magazine
        author_count = {}
        for article in self.articles():
            author_count[article.author] = author_count.get(article.author, 0) + 1
        return [author for author, count in author_count.items() if count > 2] or None  # Returns None if no authors meet the criteria

    @classmethod
    def top_publisher(cls):
        # Returns the Magazine with the most articles
        return max(cls.all, key=lambda magazine: len(magazine.articles()), default=None)

