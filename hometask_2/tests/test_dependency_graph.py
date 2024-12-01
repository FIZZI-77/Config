import pytest

from src.dependency_graph import flatten_dependencies

def test_flatten_dependencies():
    dependencies = {
        "accepts": {
            "mime-types": {
                "mime-db": {}
            },
            "negotiator": {}
        },
        "array-flatten": {},
        "body-parser": {
            "debug": {
                "ms": {}
            },
            "iconv-lite": {},
            "raw-body": {
                "unpipe": {}
            }
        },
        "content-disposition": {
            "safe-buffer": {}
        }
    }

    graph = flatten_dependencies("express", dependencies)
    expected_graph = {
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
    assert graph == expected_graph
