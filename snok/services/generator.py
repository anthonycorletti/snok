from typing import Any


class _BaseContentGenerator:
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Subclasses must implement this method.")


class _ModelContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Generating model...")
        print(args, kwargs)


class _RouterContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Generating router...")
        print(args, kwargs)


class _ViewContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Generating view...")
        print(args, kwargs)


class _ScaffoldContentGenerator(_BaseContentGenerator):
    def generate(self, *args: Any, **kwargs: Any) -> Any:
        print("Scaffolding...")
        print(args, kwargs)
