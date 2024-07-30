import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from logger import get_json_logger
from notify import send_pushbullet_message

HERE = Path(__file__).resolve().parent

DATA_DIR = HERE / "data"
DIFFS_DIR = HERE / "diffs"

if not DATA_DIR.exists():
    DATA_DIR.mkdir()
if not DIFFS_DIR.exists():
    DIFFS_DIR.mkdir()

URL_TEMPLATE = "https://www.deltahagibor.cz/seznam-bytu?1699092a_page={}"

logger = get_json_logger(HERE / "get_flats.log")


@dataclass
class Flat:
    id: str
    building: str
    floor: int
    disposition: str
    price: float
    size: float
    balcony_size: float
    furnished: bool
    reserved: bool

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Flat):
            return False
        return asdict(self) == asdict(value)


@dataclass
class FlatDifference:
    old: Flat | None
    new: Flat | None


def save_new_file(flats: list[Flat]) -> None:
    now_ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = DATA_DIR / f"{now_ts}.json"
    file_path.write_text(json.dumps([asdict(flat) for flat in flats], indent=2))


def save_last_differences(differences: list[FlatDifference]) -> None:
    if not differences:
        return
    now_ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = DIFFS_DIR / f"{now_ts}.json"
    file_path.write_text(json.dumps([asdict(diff) for diff in differences], indent=2))


def get_last_flats() -> list[Flat]:
    files = sorted(DATA_DIR.glob("*.json"))
    if not files:
        return []
    last_file = files[-1]
    return [Flat(**flat) for flat in json.loads(last_file.read_text())]


def get_difference_from_last_two_data() -> list[FlatDifference]:
    files = sorted(DATA_DIR.glob("*.json"))
    if len(files) < 2:
        return []
    old_flats = [Flat(**flat) for flat in json.loads(files[-2].read_text())]
    new_flats = [Flat(**flat) for flat in json.loads(files[-1].read_text())]
    return get_flats_differences(old_flats, new_flats)


def get_flats_differences(
    old_flats: list[Flat], new_flats: list[Flat]
) -> list[FlatDifference]:
    old_flats_dict = {flat.id: flat for flat in old_flats}
    new_flats_dict = {flat.id: flat for flat in new_flats}

    all_flats_ids = set(old_flats_dict.keys()) | set(new_flats_dict.keys())

    differences = []
    for flat_id in all_flats_ids:
        old_flat = old_flats_dict.get(flat_id)
        new_flat = new_flats_dict.get(flat_id)
        if old_flat != new_flat:
            differences.append(FlatDifference(old=old_flat, new=new_flat))
    return differences


def get_flat_from_html(flat_html: str) -> Flat:
    invisible_class = "w-condition-invisible"

    soup = BeautifulSoup(flat_html, "html.parser")

    divs = soup.find_all("div")

    divs_without_div_children = [div for div in divs if not div.find_all("div")]

    visible_divs = [
        div
        for div in divs_without_div_children
        if invisible_class not in div.get("class", [])
    ]

    div_texts = [div.text for div in visible_divs]

    def get_value_after_label(label: str) -> str | None:
        try:
            return div_texts[div_texts.index(label) + 1]
        except ValueError:
            return None

    def try_number_or_zero(text: str) -> float:
        try:
            return float(text)
        except ValueError:
            return 0

    # div_texts ['QA-01-01', 'budova', 'A', 'podlaží', '1.NP', 'dispozice', '1+kk', 'plocha (m2)', '28.2', 'terasa/balkón/předzahrádka (m2)', '14.0', 'vybavený', 'ANO', 'ANO', 'cena', '24 000', ' Kč', '', '', 'detail', 'detail', '', 'poptat', 'stav', 'Volný od ', 'Volný od ', '1.1.2025', 'Volný od ']

    return Flat(
        id=div_texts[0],
        building=get_value_after_label("budova") or "",
        floor=take_numbers_from_beginning(get_value_after_label("podlaží") or "0") or 0,
        disposition=get_value_after_label("dispozice") or "",
        price=try_number_or_zero(
            (get_value_after_label("cena") or "0").replace(" ", "")
        ),
        size=try_number_or_zero(get_value_after_label("plocha (m2)") or ""),
        balcony_size=try_number_or_zero(
            get_value_after_label("terasa/balkón/předzahrádka (m2)") or ""
        ),
        furnished=get_value_after_label("vybavený") == "ANO",
        reserved=get_value_after_label("stav") == "Rezervováno",
    )


def take_numbers_from_beginning(text: str) -> int | None:
    result = re.match(r"\d+", text)
    if result is None:
        return None
    return int(result.group())


def get_flats() -> list[Flat]:
    parent_div_name = "seznam-bytu-grid"
    flats_data = []
    for index in range(1, 9):
        url = URL_TEMPLATE.format(index)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        flats = soup.find_all("div", class_=parent_div_name)

        for flat_html in flats[1:]:
            flat = get_flat_from_html(str(flat_html))
            flats_data.append(flat)
    return flats_data


def main():
    logger.info({"event": "Start"})
    flats = get_flats()
    logger.info({"event": "NewFlats", "flats": len(flats)})
    save_new_file(flats)
    differences = get_difference_from_last_two_data()
    logger.info(
        {
            "event": "Differences",
            "differences": [asdict(diff) for diff in differences],
        }
    )
    if differences:
        save_last_differences(differences)
        send_pushbullet_message(
            "FlatDifferences", f"There are {len(differences)} diffs in flats."
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error({"event": "Error", "exception": str(e)})
        send_pushbullet_message("FlatsError", str(e))
