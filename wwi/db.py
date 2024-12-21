from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    root = Column(String, nullable=False)
    language = Column(String, nullable=False)
    word_type = Column(String, nullable=False)
    word_subtype = Column(String)
    person = Column(String)
    gender = Column(String)
    number = Column(String)
    state = Column(String)


class VerseWord(Base):
    __tablename__ = 'verse_words'
    id = Column(Integer, primary_key=True, autoincrement=True)
    book = Column(String, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    strongs = Column(String, nullable=False)
    word_id = Column(Integer, ForeignKey('words.id'), nullable=False)

    transliteration = Column(String)
    hebrew = Column(String, nullable=False)
    english = Column(String, nullable=False)

    word = relationship('Word', back_populates='verses')


Word.verses = relationship('VerseWords', order_by=VerseWords.id, back_populates='word')


DATABASE_URL = 'sqlite:///words.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)