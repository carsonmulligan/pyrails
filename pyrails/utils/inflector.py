"""String inflection utilities for naming conventions."""
import re
import inflect

_inflect_engine = inflect.engine()


def pluralize(word: str) -> str:
    """Convert singular to plural (user -> users)."""
    return _inflect_engine.plural(word)


def singularize(word: str) -> str:
    """Convert plural to singular (users -> user)."""
    return _inflect_engine.singular_noun(word) or word


def camelize(string: str) -> str:
    """Convert snake_case to CamelCase (user_profile -> UserProfile)."""
    return "".join(word.capitalize() for word in string.split("_"))


def underscore(string: str) -> str:
    """Convert CamelCase to snake_case (UserProfile -> user_profile)."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", string)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def tableize(model_name: str) -> str:
    """Convert model name to table name (User -> users, Article -> articles)."""
    return pluralize(underscore(model_name))


def classify(table_name: str) -> str:
    """Convert table name to class name (users -> User, articles -> Article)."""
    return camelize(singularize(table_name))
