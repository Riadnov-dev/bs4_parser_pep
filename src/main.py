import logging
import re
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import BASE_DIR, MAIN_DOC_URL
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import (
    get_response,
    find_tag,
    parse_pep_details,
    parse_pep_list,
    save_pep_results,
)


def whats_new(session):
    whats_new_url = urljoin(MAIN_DOC_URL, "whatsnew/")
    response = get_response(session, whats_new_url)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, features="lxml")
    main_div = find_tag(soup, "section", attrs={"id": "what-s-new-in-python"})
    div_with_ul = find_tag(main_div, "div", attrs={"class": "toctree-wrapper"})
    sections_by_python = div_with_ul.find_all(
        "li", attrs={"class": "toctree-l1"})
    results = [("Ссылка на статью", "Заголовок", "Редактор, Автор")]

    for section in tqdm(sections_by_python):
        version_a_tag = section.find("a")
        href = version_a_tag["href"]
        version_link = urljoin(whats_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features="lxml")
        h1 = find_tag(soup, "h1")
        dl = find_tag(soup, "dl")
        dl_text = dl.text.replace("\n", " ")
        results.append(
            (version_link, h1.text if h1 else "No h1 found", dl_text))

    return results


def latest_versions(session):
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return []
    soup = BeautifulSoup(response.text, "lxml")
    sidebar = find_tag(soup, "div", {"class": "sphinxsidebarwrapper"})
    ul_tags = sidebar.find_all("ul")
    for ul in ul_tags:
        if "All versions" in ul.text:
            a_tags = ul.find_all("a")
            break
    else:
        raise Exception("Не найден список c версиями Python")

    results = [("Ссылка на документацию", "Версия", "Статус")]
    pattern = r"Python (?P<version>\d\.\d+) \((?P<status>.*)\)"
    for a_tag in a_tags:
        link = a_tag["href"]
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ""
        results.append((link, version, status))

    return results


def download(session):
    downloads_url = urljoin(MAIN_DOC_URL, "download.html")
    response = get_response(session, downloads_url)
    if response is None:
        return

    soup = BeautifulSoup(response.text, features="lxml")
    main_tag = find_tag(soup, "div", {"role": "main"})
    table_tag = find_tag(main_tag, "table", {"class": "docutils"})
    pdf_a4_tag = find_tag(
        table_tag, "a", {"href": re.compile(r".+pdf-a4\.zip$")})
    pdf_a4_link = pdf_a4_tag["href"]
    archive_url = urljoin(downloads_url, pdf_a4_link)
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
    status_counts, mismatched_statuses = parse_pep_details(session, pep_data)
    save_pep_results(status_counts)
    logging.info("Результаты парсинга: %s", status_counts)
    if mismatched_statuses:
        logging.warning("Несовпадающие статусы:")
        for url, page_status, table_status in mismatched_statuses:
            logging.warning("%s\nСтатус в карточке: %s\nОжидаемые статусы: %s",
                            url, table_status, page_status)


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
    logging.info(f"Результаты парсинга: {results}")

    if results is not None:
        logging.info("Обработка результатов парсинга.")
        control_output(results, args)

    logging.info("Парсер завершил работу.")


if __name__ == '__main__':
    main()
