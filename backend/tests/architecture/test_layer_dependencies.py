import ast
from dataclasses import dataclass
from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[2] / "app"


@dataclass(frozen=True, order=True)
class Dependency:
    file: str
    module: str


def python_files(root: Path):
    return sorted(
        path for path in root.rglob("*.py") if "__pycache__" not in path.parts
    )


def imports_in(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imports.add(node.module)
        elif isinstance(node, ast.Import):
            imports.update(alias.name for alias in node.names)
    return imports


def dependencies_under(root: Path, prefix: str) -> set[Dependency]:
    dependencies: set[Dependency] = set()
    for path in python_files(root):
        relative = path.relative_to(APP_ROOT).as_posix()
        dependencies.update(
            Dependency(relative, module)
            for module in imports_in(path)
            if module.startswith(prefix)
        )
    return dependencies


def format_dependencies(dependencies: set[Dependency]) -> str:
    return "\n".join(
        f"- {dependency.file} -> {dependency.module}"
        for dependency in sorted(dependencies)
    )


def test_domain_is_free_of_frameworks_and_outer_layers():
    forbidden_prefixes = (
        "fastapi",
        "pydantic",
        "sqlalchemy",
        "app.presentation",
        "app.infrastructure",
        "app.shared.infrastructure",
    )
    violations: set[Dependency] = set()
    domain_roots = [APP_ROOT / "shared" / "domain"]
    domain_roots.extend((APP_ROOT / "modules").glob("*/domain"))

    for root in domain_roots:
        for path in python_files(root):
            relative = path.relative_to(APP_ROOT).as_posix()
            for module in imports_in(path):
                if (
                    module.startswith(forbidden_prefixes)
                    or ".application" in module
                    or ".infrastructure" in module
                ):
                    violations.add(Dependency(relative, module))

    assert not violations, (
        "Domain dependencies must point inward:\n"
        + format_dependencies(violations)
    )


def test_domain_does_not_import_another_bounded_context():
    violations: set[Dependency] = set()
    for domain_root in (APP_ROOT / "modules").glob("*/domain"):
        own_context = domain_root.parent.name
        for path in python_files(domain_root):
            relative = path.relative_to(APP_ROOT).as_posix()
            for module in imports_in(path):
                if not module.startswith("app.modules."):
                    continue
                imported_context = module.split(".")[2]
                if imported_context != own_context:
                    violations.add(Dependency(relative, module))

    assert not violations, (
        "Cross-context domain imports are forbidden:\n"
        + format_dependencies(violations)
    )


def test_bounded_contexts_and_aggregate_roots_are_explicit():
    contexts = {
        path.name
        for path in (APP_ROOT / "modules").iterdir()
        if path.is_dir() and not path.name.startswith("__")
    }
    assert contexts == {"health", "inventory"}

    aggregate_roots: set[tuple[str, str]] = set()
    for path in (APP_ROOT / "modules").glob("*/domain/*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue
            base_names = {
                base.id
                for base in node.bases
                if isinstance(base, ast.Name)
            }
            if "AggregateRoot" in base_names:
                aggregate_roots.add((path.relative_to(APP_ROOT).as_posix(), node.name))

    assert aggregate_roots == {("modules/inventory/domain/entity.py", "Animal")}


def test_no_new_application_to_presentation_dependencies():
    allowed = {
        Dependency(
            "modules/health/application/health_service.py",
            "app.presentation.schemas.health.health_create",
        ),
        Dependency(
            "modules/health/application/health_service.py",
            "app.presentation.schemas.health.health_update",
        ),
        Dependency(
            "modules/health/application/health_service_legacy.py",
            "app.presentation.schemas.health.health_create",
        ),
        Dependency(
            "modules/health/application/health_service_legacy.py",
            "app.presentation.schemas.health.health_update",
        ),
        Dependency(
            "modules/inventory/application/paddock_service.py",
            "app.presentation.schemas.paddock_schema",
        ),
        Dependency(
            "modules/inventory/application/pasture_service.py",
            "app.presentation.schemas.pasture_schema",
        ),
        Dependency(
            "shared/application/auth/auth_service.py",
            "app.presentation.schemas.auth_schema",
        ),
        Dependency(
            "shared/application/auth/auth_service.py",
            "app.presentation.schemas.user.user_create",
        ),
        Dependency(
            "shared/application/property/property_service.py",
            "app.presentation.schemas.property_schema",
        ),
    }
    actual: set[Dependency] = set()
    roots = [APP_ROOT / "shared" / "application"]
    roots.extend((APP_ROOT / "modules").glob("*/application"))
    for root in roots:
        actual |= dependencies_under(root, "app.presentation")

    unexpected = actual - allowed
    assert not unexpected, (
        "New application -> presentation debt:\n"
        + format_dependencies(unexpected)
    )


def test_no_new_infrastructure_to_presentation_dependencies():
    allowed = {
        Dependency(
            "shared/infrastructure/persistence/paddock_repository.py",
            "app.presentation.schemas.paddock_schema",
        ),
        Dependency(
            "shared/infrastructure/persistence/pasture_repository.py",
            "app.presentation.schemas.pasture_schema",
        ),
    }
    actual: set[Dependency] = set()
    roots = [APP_ROOT / "shared" / "infrastructure", APP_ROOT / "infrastructure"]
    roots.extend((APP_ROOT / "modules").glob("*/infrastructure"))
    for root in roots:
        actual |= dependencies_under(root, "app.presentation")

    unexpected = actual - allowed
    assert not unexpected, (
        "New infrastructure -> presentation debt:\n"
        + format_dependencies(unexpected)
    )


def test_routers_do_not_add_persistence_or_sql_dependencies():
    routers = APP_ROOT / "presentation" / "api" / "v1"
    allowed: set[Dependency] = set()
    actual: set[Dependency] = set()
    direct_query_calls: dict[str, int] = {}
    for path in routers.glob("*_router.py"):
        relative = path.relative_to(APP_ROOT).as_posix()
        actual.update(
            Dependency(relative, module)
            for module in imports_in(path)
            if ".infrastructure.persistence" in module
        )
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        direct_query_calls[relative] = sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "query"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "db"
        )

    unexpected = actual - allowed
    assert not unexpected, (
        "New router -> persistence debt:\n" + format_dependencies(unexpected)
    )
    assert {file: count for file, count in direct_query_calls.items() if count} == {}
