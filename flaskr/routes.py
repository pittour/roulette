from flask import Blueprint, request
from flaskr.database import get_db
import random, math


bp = Blueprint('routes', __name__)

@bp.route('/balance')
def get_balance():
    db=get_db()
    balance = db.execute(
        'SELECT amount FROM balance WHERE id = ?', (1,)
    ).fetchone()[0]
    return {
        "balance": balance
    }

@bp.route('/topup', methods=('POST', 'PUT'))
def topup():
    amount = int(request.json['amount'])
    db = get_db()
    db.execute(
        'UPDATE balance SET amount = amount + ? WHERE id = 1',
        (amount,)
    )
    db.commit()
    balance = db.execute('SELECT amount FROM balance WHERE id = ?', (1,)).fetchone()[0]
    return {
        "balance": balance
    }

@bp.route('/play', methods=('POST', 'PUT'))
def play():
    rand = random.randint(0, 49)
    amount = int(request.json['amount'])
    guess = int(request.json['guess'])
    db = get_db()
    if guess == rand:
        db.execute(
            'UPDATE balance SET amount = amount + ? WHERE id = 1',
            (amount * 3,)
        )
        db.commit()

        message = f"Vous gagnez {amount * 3}$"
        
    elif guess % 2 == rand % 2:
        db.execute(
                'UPDATE balance SET amount = amount + ? WHERE id = 1',
                (math.ceil(amount * 0.5),)
            )
        db.commit()

        message = f"Vous gagnez {math.ceil(amount * 0.5)}$"

    else:
        db.execute(
                'UPDATE balance SET amount = amount - ? WHERE id = 1',
                (amount,)
            )
        db.commit()
        message = "Vous perdez votre mise."
    balance = db.execute('SELECT amount FROM balance WHERE id = ?', (1,)).fetchone()[0]
    return {
            "message" : message,
            "balance": balance
        }
    
    


