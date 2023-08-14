from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flashcard.auth import login_required
from flashcard.db import get_db
from flashcard.study_set import get_study_set

bp = Blueprint('flashcard', __name__, url_prefix="/flashcard")

def get_flashcard(id, check_author=True):
    flashcard = get_db().execute(
        'SELECT f.id, term, definition, image_url, study_set_id, f.created_at, author_id, username'
        ' FROM flashcard f JOIN study_set st ON f.study_set_id = st.id JOIN user u ON st.author_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

    if flashcard is None:
        abort(404, f"Flashcard id {id} doesn't exist.")

    if check_author and flashcard['author_id'] != g.user['id']:
        abort(403)

    return flashcard

@bp.route('/<int:study_set_id>/')
def index(study_set_id):
    study_set = get_study_set(study_set_id)
    db = get_db()
    flashcards = db.execute(
        'SELECT f.id, term, definition, image_url, study_set_id, f.created_at, author_id, username'
        ' FROM flashcard f JOIN study_set st ON f.study_set_id = st.id JOIN user u ON st.author_id = u.id'
        ' WHERE study_set_id = ? ORDER BY f.created_at DESC', (study_set['id'],)
    ).fetchall()
    return render_template('flashcard/index.html', flashcards=flashcards, study_set=study_set )

@bp.route('/<int:study_set_id>/create', methods=('GET', 'POST'))
@login_required
def create(study_set_id):
    study_set = get_study_set(study_set_id)

    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']
        image_url = request.form['image_url']
        error = None

        if not term:
            error = 'Term is required.'
        if not definition:
            error = 'Definition is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO flashcard (study_set_id, term, definition, image_url)'
                ' VALUES (?, ?, ?, ?)',
                (study_set['id'], term, definition, image_url)
            )
            db.commit()
            return redirect(url_for('flashcard.index', study_set_id=study_set_id))

    return render_template('flashcard/create.html')

@bp.route('/<int:study_set_id>/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(study_set_id, id):
    study_set = get_study_set(study_set_id)
    flashcard = get_flashcard(id)

    if request.method == 'POST':
        term = request.form['term']
        definition = request.form['definition']
        image_url = request.form['image_url']
        error = None

        if not term:
            error = 'Term is required.'
        if not definition:
            error = 'Definition is required.'


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE flashcard SET term = ?, definition = ?, image_url = ?'
                ' WHERE id = ?',
                (term, definition, image_url, id)
            )
            db.commit()
            return redirect(url_for('flashcard.index', study_set_id=study_set_id))

    return render_template('flashcard/update.html', flashcard=flashcard)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    flashcard = get_flashcard(id)
    db = get_db()
    db.execute('DELETE FROM flashcard WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('flashcard.index', study_set_id=flashcard['study_set_id']))