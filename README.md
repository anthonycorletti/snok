<p align="center">
  <a href="https://snok.corletti.xyz"><img src="https://github.com/anthonycorletti/snok/blob/main/docs/img/logo.png?raw=true" alt="Snok"></a>
</p>
<p align="center">
    <em>🚀 A simple, modern, full-stack toolkit for Python 🐍</em>
</p>
<p align="center">
<a href="https://github.com/anthonycorletti/snok/actions?query=workflow%3Atest" target="_blank">
    <img src="https://github.com/anthonycorletti/snok/workflows/test/badge.svg" alt="Test">
</a>
<a href="https://github.com/anthonycorletti/snok/actions?query=workflow%3Apublish" target="_blank">
    <img src="https://github.com/anthonycorletti/snok/workflows/publish/badge.svg" alt="publish">
</a>
<a href="https://codecov.io/gh/anthonycorletti/snok" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/anthonycorletti/snok?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/snok/" target="_blank">
    <img alt="PyPI" src="https://img.shields.io/pypi/v/snok?color=blue">
</a>
</p>

---

**Documentation**: <a href="https://snok.corletti.xyz" target="_blank">https://snok.corletti.xyz</a>

**Source Code**: <a href="https://github.com/anthonycorletti/snok" target="_blank">https://github.com/anthonycorletti/snok</a>

---

Snok is a simple, modern, full-stack toolkit for Python.

Snok is in it's earliest stages, so feedback and ideas are very welcome and encouraged. Please open an [issue](https://github.com/anthonycorletti/snok/issues/new/choose) if you have a question, comment, feature request, idea, etc, and/or connect with Anthony directly on [Twitter](https://twitter.com/anthonycorletti) if you'd like to get in touch about the project.

## 🙋 Why?

The Python tooling ecosystem has plenty of options, and often times, it's not clear whether or not you're following the "right" way to do things, especially when those ways are changing week to week.

With this in mind, snok is a Python toolkit for developers that focuses on making it simple and easy to build modern, full-stack applications, across web and AI frameworks.

Snok is designed to leverage the best tools and packages that exist in the Python ecosystem in simple and easy to use workflows that accelerate development.

## 🎉 Featuring

- Package generation
- Task management with `invoke`
- Packaging with `setuptools`
- Linting with `ruff` and `black`
- Type checking with `mypy`
- Testing with `pytest`

## 🤩 Coming Soon

- Web application generation with `fastapi` and `htmx`
- Database integration with `pydantic` and `sqlmodel`
- Production ready deployment stacks with `nix`, `docker`, `skaffold` and `kustomize`
- AI framework integrations with `pytorch` and `langchain`

Check out the latest [issues](https://github.com/anthonycorletti/snok/issues) and [pull requests](https://github.com/anthonycorletti/snok/pulls) to see what's coming soon!

## 📝 Requirements

- Python 3.11+
- `pip`

## ⚙️ Installation

After you've created your Python 3.11+ virtual environment, install Snok with:

```sh
pip install snok
```

## 🐍 Getting Started

Create a new package with:

```sh
snok new mypackage && cd mypackage
```

Snok uses `invoke` to manage tasks, like installing dependencies, running tests, and more.

```sh
inv --list
```

To install dependencies:

```sh
inv add fastapi
```

To uninstall dependencies:

```sh
inv remove fastapi
```

## 🫶 How can I help?

- [⭐️ Star snok on GitHub! ⭐️](https://github.com/anthonycorletti/snok)
- Open an [issue](https://github.com/anthonycorletti/snok/issues/new/choose) if you have a question, comment, feature request, or bug report.
- Open a [pull request](https://github.com/anthonycorletti/snok/compare) on GitHub. Contributions are encouraged and welcome!

## 📲 Contact

Reach out on [Twitter](https://twitter.com/anthonycorletti) if you'd like to get in touch!

&nbsp;
