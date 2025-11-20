"""Tests for inflector utility."""
import pytest
from pyrails.utils.inflector import (
    pluralize,
    singularize,
    camelize,
    underscore,
    tableize,
    classify,
)


def test_pluralize():
    assert pluralize("user") == "users"
    assert pluralize("article") == "articles"
    assert pluralize("person") == "people"


def test_singularize():
    assert singularize("users") == "user"
    assert singularize("articles") == "article"
    assert singularize("people") == "person"


def test_camelize():
    assert camelize("user_profile") == "UserProfile"
    assert camelize("article") == "Article"
    assert camelize("my_model_name") == "MyModelName"


def test_underscore():
    assert underscore("UserProfile") == "user_profile"
    assert underscore("Article") == "article"
    assert underscore("MyModelName") == "my_model_name"


def test_tableize():
    assert tableize("User") == "users"
    assert tableize("Article") == "articles"
    assert tableize("UserProfile") == "user_profiles"


def test_classify():
    assert classify("users") == "User"
    assert classify("articles") == "Article"
    assert classify("user_profiles") == "UserProfile"
