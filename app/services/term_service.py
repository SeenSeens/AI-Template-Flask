from app.repositories import TermRepository


class TermService:
    def __init__(self, termRepository: TermRepository):
        self.termRepository = termRepository

    def get_term(self, term_id):
        return self.termRepository.get_term_by_id(term_id)

    def create_term_with_taxonomy(self, name, slug, description, taxonomy_type):
        term = self.termRepository.create_term(name, slug, description)
        self.termRepository.create_term_taxonomy(term.id, taxonomy_type)
        return term

    def get_terms_by_taxonomy(self, taxonomy_type):
        return self.termRepository.get_terms_by_taxonomy(taxonomy_type)

    def update_term(self, term_id, name=None, slug=None, description=None):
        return self.termRepository.update_term(term_id, name, slug, description)

    def delete_term(self, term_id):
        return self.termRepository.delete_term(term_id)