from app.core import db
from app.core.models import Term, TermTaxonomy



class TermRepository:
    def create_term(self, name, slug, description):
        term = Term(name=name, slug=slug, description=description)
        db.session.add(term)
        db.session.commit()
        return term

    def create_term_taxonomy(self, term_id, taxonomy, parent=None):
        term_taxonomy = TermTaxonomy(term_id=term_id, taxonomy=taxonomy, parent=None)
        db.session.add(term_taxonomy)
        db.session.commit()
        return term_taxonomy

    def get_terms_by_taxonomy(self, taxonomy):
        return db.session.query(Term).join(TermTaxonomy).filter(
            TermTaxonomy.taxonomy == taxonomy
        ).all()

    def get_term_by_id(self, term_id):
        return Term.query.get_or_404(term_id)

    def update_term(self, term_id, name=None, slug=None, description=None):
        term = self.get_term_by_id(term_id)
        if not term:
            return None
        if name is not None:
            term.name = name
        if slug is not None:
            term.slug = slug
        if description is not None:
            term.description = description
        db.session.commit()
        return term

    def delete_term(self, term_id):
        try:
            term = self.get_term_by_id(term_id)
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