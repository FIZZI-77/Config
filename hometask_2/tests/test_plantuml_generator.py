from src.plantuml_generator import generate_plantuml_content

from src.plantuml_generator import generate_plantuml_content

def test_generate_complex_plantuml():
    graph = {
        "express": ["accepts", "array-flatten", "body-parser", "content-disposition"],
        "accepts": ["mime-types", "negotiator"],
        "mime-types": ["mime-db"],
        "mime-db": [],
        "negotiator": [],
        "array-flatten": [],
        "body-parser": ["debug", "iconv-lite", "raw-body"],
        "debug": ["ms"],
        "ms": [],
        "iconv-lite": [],
        "raw-body": ["unpipe"],
        "unpipe": [],
        "content-disposition": ["safe-buffer"],
        "safe-buffer": []
    }

    plantuml_content = generate_plantuml_content(graph)

    # Проверка структуры PlantUML
    assert "@startuml" in plantuml_content
    assert "@enduml" in plantuml_content

    # Проверка ключевых связей
    assert '"express" --> "accepts"' in plantuml_content
    assert '"accepts" --> "mime-types"' in plantuml_content
    assert '"mime-types" --> "mime-db"' in plantuml_content
    assert '"body-parser" --> "raw-body"' in plantuml_content
    assert '"raw-body" --> "unpipe"' in plantuml_content
    assert '"content-disposition" --> "safe-buffer"' in plantuml_content
