from app.core.models import Term, TermTaxonomy
from .base_repository import BaseRepository
from app.core import db

class TermRepository(BaseRepository):
    def __init__(self):
        super().__init__(Term)

    def create_term_taxonomy(self, term_id, taxonomy, parent=None):
        taxonomy = TermTaxonomy(term_id=term_id, taxonomy=taxonomy, parent=parent)
        db.session.add(taxonomy)
        db.session.commit()
        return taxonomy

    def get_terms_by_taxonomy(self, taxonomy):
        return db.session.query(Term).join(TermTaxonomy).filter(
            TermTaxonomy.taxonomy == taxonomy
        ).all()

    def delete_term(self, term_id):
        try:
            term = self.get_by_id(term_id)
            if not term:
                return False
            # Xoá taxonomy liên quan (an toàn hơn khi load và delete thủ công)
            taxonomies = TermTaxonomy.query.filter_by(term_id=term_id).all()
            for t in taxonomies:
                db.session.delete(t)
            db.session.delete(term)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"[Repository] Error deleting term: {e}")
            return False