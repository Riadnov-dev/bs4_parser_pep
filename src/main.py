import logging
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from constants import (
    BASE_DIR,
    MAIN_DOC_URL,
    PYTHON_VERSION_PATTERN,
    PDF_A4_ZIP_PATTERN
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import (
    find_tag,
    fetch_and_parse,
    parse_pep_details,
    parse_pep_list,
)


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    soup = fetch_and_parse(session, whats_new_url)

    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        "li", attrs={"class": "toctree-l1"})
    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]

    for section in tqdm(sections_by_python):
        version_link = urljoin(whats_new_url, section.find("a")["href"])
        soup = fetch_and_parse(session, version_link)
        header = find_tag(soup, "h1")
        editor_author = find_tag(soup, "dl").text.replace("\n", " ").strip()
        results.append(
            (version_link, header.text if header else "No header found",
             editor_author)
        )

    return results


def latest_versions(session):
    soup = fetch_and_parse(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")

    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise RuntimeError("Не найден список c версиями Python")

    results = [("Ссылка на документацию", "Версия", "Статус")]

    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = PYTHON_VERSION_PATTERN.search(a_tag.text)
        if text_match:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    soup = fetch_and_parse(session, downloads_url)
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag, "a", {"href": PDF_A4_ZIP_PATTERN})
    archive_url = urljoin(downloads_url, pdf_a4_tag["href"])
    filename = archive_url.split("/")[-1]

    downloads_dir = BASE_DIR / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename

    response = session.get(archive_url)

    with open(archive_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Архив был загружен и сохранён: {archive_path}")


def pep(session):
    pep_data = parse_pep_list(session)
    status_counts, mismatched_statuses = parse_pep_details(
        session, tqdm(pep_data, desc="Parsing PEPs")
    )

    logging.info("Результаты парсинга: %s", status_counts)
    if mismatched_statuses:
        logging.warning("Несовпадающие статусы:")
        for url, page_status, table_status in mismatched_statuses:
            logging.warning(
                "%s\nСтатус в карточке: %s\nОжидаемые статусы: %s",
                url,
                table_status,
                page_status,
            )

    results = [("Статус", "Количество")]
    results.extend(status_counts.items())
    total_count = sum(status_counts.values())
    results.append(("Total", total_count))

    return results


MODE_TO_FUNCTION = {
    "whats-new": whats_new,
    "latest-versions": latest_versions,
    "download": download,
    "pep": pep,
}


def main():
    configure_logging()
    logging.info("Парсер запущен!")

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f"Аргументы командной строки: {args}")

    session = requests_cache.CachedSession()
    if args.clear_cache:
        logging.info("Очищение кэша сессии.")
        session.cache.clear()

    parser_mode = args.mode
    logging.info(f"Выбран режим парсинга: {parser_mode}")
    results = MODE_TO_FUNCTION[parser_mode](session)

    if results:
        logging.info("Обработка результатов парсинга.")
        control_output(results, args)

    logging.info("Парсер завершил работу.")


if __name__ == "__main__":
    main()
