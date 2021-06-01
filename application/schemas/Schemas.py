import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from datetime import datetime as dt
from graphql import GraphQLError
from graphene_sqlalchemy.registry import get_global_registry

from ..models.models import db
from ..models.models import User as UserModel
from ..models.models import Book as BookModel
from ..models.models import Author as AuthorModel
from ..models.models import Serie as SerieModel
from ..models.models import Collection as CollectionModel
from ..models.models import UserCollection as UCModel
from ..models.models import UserBook as UBModel
from ..models.models import UserSerie as USModel
from ..models.models import AuthorBook as ABModel

def get_model_type(model):
    registry = get_global_registry()
    return lambda: registry.get_type_for_model(model)

#Objects
class UserBookObject(SQLAlchemyObjectType):
    class Meta:
        model = UBModel
        interfaces = (relay.Node, )

class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node, )
    books = graphene.List(get_model_type(UBModel))

class BookObject(SQLAlchemyObjectType):
    class Meta:
        model = BookModel
        interfaces = (relay.Node, )
    owners = graphene.List(get_model_type(UBModel))
    authors = graphene.List(get_model_type(AuthorModel))

class AuthorObject(SQLAlchemyObjectType):
    class Meta:
        model = AuthorModel
        interfaces = (relay.Node, )
    books = graphene.List(get_model_type(BookModel))

class SerieObject(SQLAlchemyObjectType):
    class Meta:
        model = SerieModel
        interfaces = (relay.Node, )

class CollectionObject(SQLAlchemyObjectType):
    class Meta:
        model = CollectionModel
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    node = relay.Node.Field()
    all_books = SQLAlchemyConnectionField(BookObject)
    all_users = SQLAlchemyConnectionField(UserObject)
    all_authors = SQLAlchemyConnectionField(AuthorObject)
    all_series = SQLAlchemyConnectionField(SerieObject)
    all_collections = SQLAlchemyConnectionField(CollectionObject)
    all_user_books = SQLAlchemyConnectionField(UserBookObject)
    book = relay.Node.Field(BookObject)
    user = relay.Node.Field(UserObject)
    author = relay.Node.Field(AuthorObject)
    serie = relay.Node.Field(SerieObject)
    collection = relay.Node.Field(CollectionObject)
    user_book = relay.Node.Field(UserBookObject)

    find_user = graphene.Field(lambda: UserObject, username=graphene.String())

    def resolve_find_user(self, info, **kwargs):
        query = UserObject.get_query(info)
        username = kwargs.get('username')
        return query.filter(UserModel.username == username).first()

# User Mutations
class AddUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, username, email):
        user = UserModel(username=username, email=email, created=dt.now(), admin=False)
        db.session.add(user)
        db.session.commit()
        return AddUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=False, default_value=None)
        admin = graphene.Boolean(required=False, default_value=False)
    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, username, **kwargs):
        email = kwargs.get('email', None)
        admin = kwargs.get('admin', False)

        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            raise GraphQLError('User not found.')
        
        user.username = username

        if email is not None:
            user.email = email

        if admin is not None:
            user.admin = admin

        db.session.commit()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
    user = graphene.Field(lambda: UserObject)

    def mutate(self, info, username):
        user = UserModel.query.filter_by(username=username).first()
        if user is None:
            raise GraphQLError('User not found.')
        
        user.books = []

        db.session.commit()
        db.session.delete(user)
        db.session.commit()
        return UpdateUser(user=user)


# Book Mutations
class AddBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        authors = graphene.String(required=False, default_value=None)
        owners = graphene.String(required=True)
        description = graphene.String(required=False, default_value=None)
        rating = graphene.Int(required=False, default_value=None)
        category = graphene.String(required=False, default_value=None)
        price = graphene.Float(required=False, default_value=None)
        purchaseDate = graphene.DateTime(required=False, default_value=None)
        edition = graphene.String(required=False, default_value=None)
        type = graphene.String(required=False, default_value=None)
        language = graphene.String(required=False, default_value=None)
        pages = graphene.Int(required=False, default_value=None)
        collection = graphene.String(required=False, default_value=None)
        serie = graphene.String(required=False, default_value=None)
    book = graphene.Field(lambda: BookObject)

    def mutate(self, info, title, owners, **kwargs):
        authors = kwargs.get('authors', None)
        description = kwargs.get('description', None)
        rating = kwargs.get('rating', None)
        category = kwargs.get('category', None)
        price = kwargs.get('price', None)
        purchaseDate = kwargs.get('purchaseDate', None)
        edition = kwargs.get('edition', None)
        type = kwargs.get('type', None)
        language = kwargs.get('language', None)
        pages = kwargs.get('pages', None)
        collection = kwargs.get('collection', None)
        serie = kwargs.get('serie', None)

        user = UserModel.query.filter_by(username=owners).first()
        if user is None:
            raise GraphQLError('Book cannot be added to non-existent user.')
        
        book = BookModel.query.filter_by(title=title).first()
        if book is None:
            userbook = UBModel(read=0)
            book = BookModel(title=title)
            userbook.book = book
            print(book.owners)
            print(user)
            user.books.append(userbook)
        else:
            userbook = UBModel(read=0)
            userbook.book = book
            user.books.append(userbook)

        if authors is not None:
            newAuthor = AuthorModel.query.filter_by(name=authors).first()
            if newAuthor is None:
                raise GraphQLError('Author does not exist.')
            book.authors = [newAuthor]
        
        if description is not None:
            book.description = description
        
        if rating is not None:
            book.rating = rating
        
        if category is not None:
            book.category = category
        
        if price is not None:
            book.price = price
        
        if purchaseDate is not None:
            book.purchaseDate = purchaseDate
        
        if edition is not None:
            book.edition = edition
        
        if type is not None:
            book.type = type
        
        if language is not None:
            book.language = language
        
        if pages is not None:
            book.pages = pages
        
        if serie is not None:
            newSerie = SerieModel.query.filter_by(title=serie).first()
            if newSerie is None:
                raise GraphQLError('Serie does not exist.')
            book.serie = newSerie
        
        if collection is not None:
            newCollection = CollectionModel.query.filter_by(title=collection).first()
            if newCollection is None:
                raise GraphQLError('Collection does not exist.')
            book.collection = newCollection

        db.session.add(book)
        db.session.commit()
        return AddBook(book=book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        title = graphene.String(required=False, default_value=None)
        authors = graphene.String(required=False, default_value=None)
        owners = graphene.String(required=False, default_value=None)
        description = graphene.String(required=False, default_value=None)
        rating = graphene.Int(required=False, default_value=None)
        category = graphene.String(required=False, default_value=None)
        read = graphene.Int(required=False, default_value=None)
        price = graphene.Float(required=False, default_value=None)
        purchaseDate = graphene.DateTime(required=False, default_value=None)
        edition = graphene.String(required=False, default_value=None)
        type = graphene.String(required=False, default_value=None)
        language = graphene.String(required=False, default_value=None)
        pages = graphene.Int(required=False, default_value=None)
        collection = graphene.String(required=False, default_value=None)
        serie = graphene.String(required=False, default_value=None)
    book = graphene.Field(lambda: BookObject)

    def mutate(self, info, id, **kwargs):
        title = kwargs.get('title', None)
        authors = kwargs.get('authors', None)
        description = kwargs.get('description', None)
        rating = kwargs.get('rating', None)
        category = kwargs.get('category', None)
        price = kwargs.get('price', None)
        purchaseDate = kwargs.get('purchaseDate', None)
        edition = kwargs.get('edition', None)
        type = kwargs.get('type', None)
        language = kwargs.get('language', None)
        pages = kwargs.get('pages', None)
        collection = kwargs.get('collection', None)
        serie = kwargs.get('serie', None)

        book = BookModel.query.filter_by(title=id).first()
        if book is None:
            raise GraphQLError('Book to update cannot be found.')
        
        if title is not None:
            book.title = title

        if authors is not None:
            newAuthor = AuthorModel.query.filter_by(name=authors).first()
            if newAuthor is None:
                raise GraphQLError('Author does not exist.')
            book.authors.append(newAuthor)
        
        if description is not None:
            book.description = description
        
        if rating is not None:
            book.rating = rating
        
        if category is not None:
            book.category = category
        
        if price is not None:
            book.price = price
        
        if purchaseDate is not None:
            book.purchaseDate = purchaseDate
        
        if edition is not None:
            book.edition = edition
        
        if type is not None:
            book.type = type
        
        if language is not None:
            book.language = language
        
        if pages is not None:
            book.pages = pages
        
        if serie is not None:
            newSerie = SerieModel.query.filter_by(title=serie).first()
            if newSerie is None:
                raise GraphQLError('Serie does not exist.')
            book.serie = newSerie
        
        if collection is not None:
            newCollection = CollectionModel.query.filter_by(title=collection).first()
            if newCollection is None:
                raise GraphQLError('Collection does not exist.')
            book.collection = newCollection

        db.session.commit()
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        authors = graphene.String(required=False, default_value=None)
        owners = graphene.String(required=False, default_value=None)
        collection = graphene.String(required=False, default_value=None)
        serie = graphene.String(required=False, default_value=None)
    book = graphene.Field(lambda: BookObject)

    def mutate(self, info, title, **kwargs):
        owners = kwargs.get('owners', None)
        authors = kwargs.get('authors', None)

        fullDelete = True
        book = BookModel.query.filter_by(title=title).first()
        if book is None:
            raise GraphQLError('Book to delete cannot be found.')

        if owners is not None:
            newUser = UserModel.query.filter_by(username=owners).first()
            if newUser is None:
                raise GraphQLError('Book cannot be removed from non-existent user.')
            userbook = UBModel.query.filter_by(bookId=book.id, userId=newUser.id).first()
            if userbook is None:
                raise GraphQLError('UserBook instance not found.')
            book.owners.remove(userbook)
            db.session.delete(userbook)
            db.session.commit()
            print(len(book.owners))
            if len(book.owners) > 0:
                fullDelete = False

        if authors is not None:
            newAuthor = AuthorModel.query.filter_by(name=authors).first()
            if newAuthor is None:
                raise GraphQLError('Author does not exist.')
            book.authors.remove(newAuthor)
            if len(book.authors) > 0:
                fullDelete = False
        db.session.commit()
        if fullDelete:
            book.authors=[]
            book.owners=[]
            db.session.delete(book)
            db.session.commit()
        return UpdateBook(book=book)

class UpdateUserBook(graphene.Mutation):
    class Arguments:
        book = graphene.String(required=True)
        user = graphene.String(required=True)
        read = graphene.Int(required=False, default_value=None)
    book = graphene.Field(lambda: BookObject)

    def mutate(self, info, book, user, **kwargs):
        read = kwargs.get('read', None)
        realBook = BookModel.query.filter_by(title=book).first()
        if realBook is None:
            raise GraphQLError('Book to update cannot be found.')

        realUser = UserModel.query.filter_by(username=user).first()
        if realUser is None:
            raise GraphQLError('User to update cannot be found.')
        if read is not None:
            userbook = UBModel.query.filter_by(bookId=realBook.id, userId=realUser.id).first()
            userbook.read = read

        db.session.commit()
        return UpdateUserBook(book=realBook)


# Serie Mutations
class AddSerie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    serie = graphene.Field(lambda: SerieObject)

    def mutate(self, info, title):
        serie = SerieModel(title=title)
        db.session.add(serie)
        db.session.commit()
        return AddSerie(serie=serie)

class UpdateSerie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        collection = graphene.String(required=False, default_value=None)
        book = graphene.String(required=False, default_value=None)
    serie = graphene.Field(lambda: SerieObject)

    def mutate(self, info, title, **kwargs):
        collection = kwargs.get('collection', None)
        book = kwargs.get('book', None)

        serie = SerieModel.query.filter_by(title=title).first()
        if serie is None:
            raise GraphQLError('Serie is not found.')
        
        serie.title = title

        if collection is not None:
            realCollection = CollectionModel.query.filter_by(title=collection).first()
            if realCollection is None:
                raise GraphQLError('Collection not found')
            serie.collection = realCollection
        
        if book is not None:
            realBook = BookModel.query.filter_by(title=book).first()
            if realBook is None:
                raise GraphQLError('Book not found')
            if serie.books is None:
                serie.books = [realBook]
            else:
                serie.books.append(realBook)
        
        db.session.commit()
        return UpdateSerie(serie=serie)

class DeleteSerie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    serie = graphene.Field(lambda: SerieObject)

    def mutate(self, info, title):
        serie = SerieModel.query.filter_by(title=title).first()
        if serie is None:
            raise GraphQLError('Serie is not found.')

        serie.books = []

        db.session.commit()
        db.session.delete(serie)
        db.session.commit()
        return DeleteSerie(serie=serie)

# Collection Mutations
class AddCollection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    collection = graphene.Field(lambda: CollectionObject)

    def mutate(self, info, title):
        collection = CollectionModel(title=title)
        db.session.add(collection)
        db.session.commit()
        return AddCollection(collection=collection)

class UpdateCollection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        serie = graphene.String(required=False, default_value=None)
        book = graphene.String(required=False, default_value=None)
    collection = graphene.Field(lambda: CollectionObject)

    def mutate(self, info, title, **kwargs):
        serie = kwargs.get('serie', None)
        book = kwargs.get('book', None)

        collection = CollectionModel.query.filter_by(title=title).first()
        if collection is None:
            raise GraphQLError('Collection is not found.')
        
        collection.title = title

        if serie is not None:
            realSerie = SerieModel.query.filter_by(title=serie).first()
            if realSerie is None:
                raise GraphQLError('Serie not found')
            if collection.series is None:
                collection.series = [realSerie]
            else:
                collection.series.append(realSerie)
        
        if book is not None:
            realBook = BookModel.query.filter_by(title=book).first()
            if realBook is None:
                raise GraphQLError('Book not found')
            if collection.books is None:
                collection.books = [realBook]
            else:
                collection.books.append(realBook)

        db.session.commit()
        return UpdateCollection(collection=collection)

class DeleteCollection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
    collection = graphene.Field(lambda: CollectionObject)

    def mutate(self, info, title):
        collection = CollectionModel.query.filter_by(title=title).first()
        if collection is None:
            raise GraphQLError('Collection is not found.')

        collection.books = []
        collection.series = []

        db.session.commit()
        db.session.delete(collection)
        db.session.commit()
        return DeleteCollection(collection=collection)


# Author Mutations
class AddAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    author = graphene.Field(lambda: AuthorObject)

    def mutate(self, info, name):
        author = AuthorModel(name=name)
        db.session.add(author)
        db.session.commit()
        return AddAuthor(author=author)

class UpdateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    author = graphene.Field(lambda: AuthorObject)

    def mutate(self, info, name):
        author = AuthorModel.query.filter_by(name=name).first()
        if author is None:
            raise GraphQLError('Author not found.')
        
        author.name = name

        db.session.commit()
        return UpdateAuthor(author=author)

class DeleteAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
    author = graphene.Field(lambda: AuthorObject)

    def mutate(self, info, name):
        author = AuthorModel.query.filter_by(name=name).first()
        if author is None:
            raise GraphQLError('Author not found.')
        
        author.books = []

        db.session.commit()
        db.session.delete(author)
        db.session.commit()
        return DeleteAuthor(author=author)

class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    update_user_book = UpdateUserBook.Field()

    add_book = AddBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()

    add_serie = AddSerie.Field()
    update_serie = UpdateSerie.Field()
    delete_serie = DeleteSerie.Field()

    add_collection = AddCollection.Field()
    update_collection = UpdateCollection.Field()
    delete_collection = DeleteCollection.Field()

    add_author = AddAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)