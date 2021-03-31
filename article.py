"""
Abstract url: https://arxiv.org/abs/1711.02226
"""
import arxiv
import click

DEFAULT_DIR = "~/Downloads"


def parse_id(abstract_url: str) -> str:
    id = abstract_url.split("/")[-1]
    return id


def get_paper(abstract_url: str) -> dict:
    paper_id = parse_id(abstract_url)
    paper = arxiv.query(id_list=[paper_id])[0]
    return paper


@click.group()
def cli():
    pass


@cli.command()
@click.argument("abstract_url")
@click.option("--download_dir", default=DEFAULT_DIR, help="Directory to download pdf")
def download(abstract_url: str, download_dir: str) -> None:
    paper = get_paper(abstract_url)
    print(f"saving '{paper.get('title')}'")
    arxiv.download(
        paper, dirpath=download_dir, slugify=lambda paper: paper.get("title")
    )
    print(f"saved to {download_dir}")


def cite_mla(paper: dict) -> str:
    """Formats paper object into MLA"""
    citation = ", ".join(paper.authors) + "."
    citation += f' "{paper.title}" {paper.id}'
    citation += f" ({paper.date[:4]})."
    return citation


@cli.command()
@click.argument("abstract_url")
def cite(abstract_url: str) -> str:
    paper = get_paper(abstract_url)
    citation = cite_mla(paper)
    print(citation)
    return citation


if __name__ == "__main__":
    cli()
