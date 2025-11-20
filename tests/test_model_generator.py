"""Tests for model generator."""
import pytest
from pyrails.generators.model_generator import ModelGenerator


def test_parse_fields():
    """Test field parsing."""
    generator = ModelGenerator(["Article", "title:str", "body:text", "count:int"])

    assert len(generator.fields) == 3
    assert generator.fields[0]["name"] == "title"
    assert generator.fields[0]["type"] == "String(255)"
    assert generator.fields[1]["name"] == "body"
    assert generator.fields[1]["type"] == "Text"
    assert generator.fields[2]["name"] == "count"
    assert generator.fields[2]["type"] == "Integer"


def test_parse_references():
    """Test foreign key field parsing."""
    generator = ModelGenerator(["Comment", "article:references", "user:references"])

    # Should have 2 reference fields
    assert len(generator.fields) == 2
    assert generator.fields[0]["name"] == "article_id"
    assert generator.fields[0]["type"] == "Integer"
    assert "reference" in generator.fields[0]
    assert generator.fields[0]["reference"]["model"] == "Article"

    # Check references list
    assert len(generator.references) == 2
    assert generator.references[0]["model"] == "Article"


def test_model_naming():
    """Test model naming conventions."""
    generator = ModelGenerator(["Article", "title:str"])

    assert generator.model_name == "Article"
    assert generator.table_name == "articles"
