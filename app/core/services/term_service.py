from app.core.repositories import TermRepository
from .base_service import BaseService

class TermService(BaseService):
    def __init__(self, termRepository: TermRepository):
        super().__init__(termRepository)
        self.termRepository = termRepository

    def create_term_with_taxonomy(self, name, slug, description, taxonomy_type):
        term = self.repository.create(name=name, slug=slug, description=description)
        self.repository.create_term_taxonomy(term.id, taxonomy_type)
        return term

    def get_terms_by_taxonomy(self, taxonomy_type):
        return self.repository.get_terms_by_taxonomy(taxonomy_type)

    def delete(self, term_id):
        return self.termRepository.delete_term(term_id)