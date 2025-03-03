from config import db
import random

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50), unique=True, nullable=False)
    
    def to_json(self):
        return {
            "id": self.id,
            "word": self.word
        }
    
    @classmethod
    def get_random_word(cls):
        count = cls.query.count()
        if count == 0:
            return None
        random_offset = random.randint(0, count - 1)
        return cls.query.offset(random_offset).first()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    guessed_letters = db.Column(db.String(26), default="", nullable=False)
    attempts_left = db.Column(db.Integer, default=5, nullable=False)
    status = db.Column(db.String(10), default="ongoing", nullable=False)  # ongoing, won, lost
    
    word = db.relationship('Word', backref=db.backref('games', lazy=True))
    
    def to_json(self):
        word_to_guess = self.word.word.lower()
        masked_word = ""
        
        for letter in word_to_guess:
            if letter in self.guessed_letters.lower():
                masked_word += letter
            else:
                masked_word += "_"
        
        return {
            "id": self.id,
            "maskedWord": masked_word,
            "guessedLetters": self.guessed_letters,
            "attemptsLeft": self.attempts_left,
            "status": self.status
        }
    
    def check_victory(self):
        word_to_guess = self.word.word.lower()
        return all(letter in self.guessed_letters for letter in word_to_guess)
