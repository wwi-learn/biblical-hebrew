from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True, autoincrement=True)
    hebrew = Column(String, nullable=False, unique=True)
    root = Column(String)
    language = Column(String, nullable=False)
    strongs = Column(String)
    transliteration = Column(String)

    verse_words = relationship('VerseWord', order_by='VerseWord.id', back_populates='word')
    word_morphologies = relationship('WordMorphology', order_by='WordMorphology.id', back_populates='word')


class WordMorphology(Base):
    __tablename__ = 'word_morphology'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    index = Column(Integer, nullable=False)
    part_of_speech = Column(String, nullable=False)
    word_type = Column(String)
    stems = Column(String)
    person = Column(String)
    gender = Column(String)
    number = Column(String)
    state = Column(String)

    word = relationship('Word', back_populates='word_morphologies')


class VerseWord(Base):
    __tablename__ = 'verse_word'
    __table_args__ = (UniqueConstraint('book', 'chapter', 'verse', 'verse_position', name='_verse_word_uc'),)
    id = Column(Integer, primary_key=True, autoincrement=True)
    book = Column(String, nullable=False)
    chapter = Column(Integer, nullable=False)
    verse = Column(Integer, nullable=False)
    verse_position = Column(Integer, nullable=False)
    word_id = Column(Integer, ForeignKey('word.id'), nullable=False)
    english = Column(String, nullable=False)

    word = relationship('Word', back_populates='verse_words')


DATABASE_URL = 'sqlite:///words.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def get_session():
    Base.metadata.create_all(engine)
    return Session()
