import logging
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from requests import RequestException

from constants import PEP_URL
from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
        return response
    except RequestException:
        logging.exception(
            f"Возникла ошибка при загрузке страницы {url}", stack_info=True
        )


# Перехват ошибки поиска тегов.
def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f"Не найден тег {tag} {attrs}"
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def fetch_and_parse(session, url):
    response = get_response(session, url)
    if response is None:
        raise RuntimeError(f"Не удалось получить данные по адресу: {url}")
    return BeautifulSoup(response.text, features="lxml")


def parse_pep_list(session):
    response = get_response(session, PEP_URL)
    if response is None:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="pep-zero-table")

    pep_data = set()
    for table in tables:
        rows = table.find_all("tr")
        for row in rows[1:]:
            columns = row.find_all("td")
            if len(columns) < 2:
                continue
            number = columns[1].text.strip()
            title = columns[2].text.strip()
            status = columns[0].text.strip() if len(columns) > 2 else "Unknown"
            link = columns[1].find("a")["href"]
            pep_data.add((number, title, status, link))

    return list(pep_data)


def parse_pep_details(session, pep_data):
    status_counts = {}
    mismatched_statuses = []

    for number, title, table_status, link in pep_data:
        pep_page_url = urljoin(PEP_URL, link)
        pep_page_response = get_response(session, pep_page_url)
        if pep_page_response is None:
            continue

        soup = BeautifulSoup(pep_page_response.text, "html.parser")
        try:
            dl = find_tag(soup, "dl")
            dt_tags = dl.find_all("dt")
            for dt in dt_tags:
                if dt.text.strip() == "Status:":
                    page_status = dt.find_next_sibling("dd").text.strip()
                    break
            else:
                page_status = "Unknown"
        except Exception as e:
            logging.error(f"Ошибка при парсинге страницы {pep_page_url}: {e}")
            page_status = "Unknown"

        if page_status not in status_counts:
            status_counts[page_status] = 0
        status_counts[page_status] += 1

        if page_status != table_status:
            mismatched_statuses.append(
                (pep_page_url, page_status, table_status))

    return status_counts, mismatched_statuses
