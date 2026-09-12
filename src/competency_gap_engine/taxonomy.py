import json
from enum import Enum
from pathlib import Path
from pydantic import BaseModel

DEFAULT_TAXONOMY_PATH = Path(__file__).parent / "taxonomy.json"

# defining FRAC based competency categories
class CompetencyCategory(str, Enum):                    # using enum to make competency category names typo proof
    BEHAVIOURAL = "behavioural"
    FUNCTIONAL = "functional"
    DOMAIN = "domain"

class ProficiencyLevel(BaseModel):
    level: int                                  # 1-5 (refer to FRAC taxonomy of igot)
    name: str                                   # "Independent" for eg
    description: str 

class Competency(BaseModel):
    id: str
    name: str
    category: CompetencyCategory

class Taxonomy(BaseModel):
    proficiency_levels: list[ProficiencyLevel]
    competencies: list[Competency]

    def get_competency(self, competency_id: str) -> Competency | None:
        return next((c for c in self.competencies if c.id == competency_id), None)      # returns the first match or none if no match found

    # filters by category
    def by_category(self, category: CompetencyCategory | str) -> list[Competency]: 
        category = CompetencyCategory(category)                                     # normalizes whatever we get into valid enum or flashes an error if not matched
        return [c for c in self.competencies if c.category == category]             # returns all competencies in one of three FRAC categories

    def get_level(self, level: int) -> ProficiencyLevel | None:
        return next((l for l in self.proficiency_levels if l.level == level), None)

    def all_ids(self) -> list[str]:
        return [c.id for c in self.competencies]

def load_taxonomy(path: Path = DEFAULT_TAXONOMY_PATH) -> Taxonomy:
    with open(path, "r", encoding="utf-8") as f:            # opens json file safely
        raw = json.load(f)                                  # parsing json to python syntax
    return Taxonomy(**raw)                                  # validating data and handing back as Taxonomy


if __name__ == "__main__":
    tax = load_taxonomy()

    print(f"Loaded {len(tax.competencies)} competencies across "
          f"{len(set(c.category for c in tax.competencies))} categories, "
          f"{len(tax.proficiency_levels)} proficiency levels.")

    for cat in CompetencyCategory:
        names = [c.name for c in tax.by_category(cat)]
        print(f"\n{cat.value.upper()} ({len(names)}):")
        for n in names:
            print(f"  - {n}")

