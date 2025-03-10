import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime
import xml.etree.ElementTree as ET

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def get_exchange_rate(session):
    # Получаем курс доллара к рублю от Центробанка РФ через XML
    date_req = datetime.now().strftime("%d/%m/%Y")
    url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date_req}"
    xml_text = await fetch(session, url)
    root = ET.fromstring(xml_text)
    rate = None
    for valute in root.findall("Valute"):
        char_code = valute.find("CharCode")
        if char_code is not None and char_code.text == "USD":
            # Значение курса может иметь запятую вместо точки
            value_str = valute.find("Value").text
            rate = float(value_str.replace(',', '.'))
            break
    if rate is None:
        raise Exception("Курс USD не найден")
    return rate

async def parse_company_page(session, url):
    """
    Парсит страницу компании и извлекает:
      - текущую цену (в долларах),
      - P/E,
      - 52 Week Low и 52 Week High.
    """
    html = await fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    
    # Попытка извлечь текущую цену. Здесь могут потребоваться корректировки селекторов.
    current_price = None
    price_tag = soup.find("span", class_="price-section__current-value")
    if price_tag:
        try:
            # Убираем лишние символы (например, '$' или запятые)
            current_price = float(price_tag.text.strip().replace(',', '').replace('$',''))
        except Exception as e:
            print(f"Ошибка преобразования цены на {url}: {e}")
    
    # Извлекаем P/E. Предполагаем, что ищем текст "P/E" в элементах, рядом с которым находится значение.
    pe_ratio = None
    pe_label = soup.find(lambda tag: tag.name in ["div", "span", "td"] and "P/E" in tag.text)
    if pe_label:
        sibling = pe_label.find_next_sibling(text=True)
        if sibling:
            try:
                pe_ratio = float(sibling.strip())
            except Exception as e:
                print(f"Ошибка преобразования P/E на {url}: {e}")

    # Извлекаем 52 Week Low и 52 Week High.
    week_low = None
    week_high = None
    low_label = soup.find(lambda tag: tag.name in ["div", "span", "td"] and "52 Week Low" in tag.text)
    if low_label:
        sibling = low_label.find_next_sibling(text=True)
        if sibling:
            try:
                week_low = float(sibling.strip().replace(',', '').replace('$',''))
            except Exception as e:
                print(f"Ошибка преобразования 52 Week Low на {url}: {e}")
    high_label = soup.find(lambda tag: tag.name in ["div", "span", "td"] and "52 Week High" in tag.text)
    if high_label:
        sibling = high_label.find_next_sibling(text=True)
        if sibling:
            try:
                week_high = float(sibling.strip().replace(',', '').replace('$',''))
            except Exception as e:
                print(f"Ошибка преобразования 52 Week High на {url}: {e}")

    return current_price, pe_ratio, week_low, week_high

async def main():
    async with aiohttp.ClientSession() as session:
        # Получаем текущий курс USD к RUB
        try:
            exchange_rate = await get_exchange_rate(session)
            print("Курс USD к RUB:", exchange_rate)
        except Exception as e:
            print("Ошибка при получении курса валют:", e)
            return

        # Загружаем страницу индекса S&P 500
        index_url = "https://markets.businessinsider.com/index/components/s&p_500"
        index_html = await fetch(session, index_url)
        soup = BeautifulSoup(index_html, 'html.parser')
        
        companies = []
        # Поиск таблицы со списком компаний
        table = soup.find("table")
        if not table:
            print("Не удалось найти таблицу с компаниями")
            return

        rows = table.find_all("tr")
        # Пропускаем заголовок таблицы (первую строку)
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue
            # Извлекаем название компании и ссылку на страницу
            name_tag = cols[0].find("a")
            if not name_tag:
                continue
            name = name_tag.text.strip()
            link = name_tag.get("href")
            if link.startswith("/"):
                link = "https://markets.businessinsider.com" + link
            # Извлекаем код компании (предполагается, что он находится в span рядом с названием)
            code_tag = cols[0].find("span")
            code = code_tag.text.strip() if code_tag else ""
            # Извлекаем годовой рост. Предполагаем, что он находится в 5-ом столбце.
            try:
                growth_text = cols[4].text.strip().replace('%','').replace(',', '.')
                growth = float(growth_text)
            except Exception as e:
                print(f"Ошибка преобразования роста для {name}: {e}")
                growth = None

            companies.append({
                "name": name,
                "link": link,
                "code": code,
                "growth": growth
            })

        # Асинхронно парсим страницы всех компаний
        tasks = [parse_company_page(session, comp["link"]) for comp in companies]
        results = await asyncio.gather(*tasks)
        for comp, res in zip(companies, results):
            current_price, pe_ratio, week_low, week_high = res
            # Конвертируем цену в рубли, если удалось получить цену
            comp["price"] = current_price * exchange_rate if current_price is not None else None
            comp["pe_ratio"] = pe_ratio
            comp["week_low"] = week_low
            comp["week_high"] = week_high
            # Вычисляем потенциальную прибыль в процентах
            if week_low and week_high and week_low != 0:
                comp["potential_profit"] = ((week_high / week_low) - 1) * 100
            else:
                comp["potential_profit"] = None

        # Формируем топ-10 списки
        expensive = sorted(
            [c for c in companies if c.get("price") is not None],
            key=lambda x: x["price"],
            reverse=True
        )[:10]

        low_pe = sorted(
            [c for c in companies if c.get("pe_ratio") is not None and c.get("pe_ratio") > 0],
            key=lambda x: x["pe_ratio"]
        )[:10]

        high_growth = sorted(
            [c for c in companies if c.get("growth") is not None],
            key=lambda x: x["growth"],
            reverse=True
        )[:10]

        high_profit = sorted(
            [c for c in companies if c.get("potential_profit") is not None],
            key=lambda x: x["potential_profit"],
            reverse=True
        )[:10]

        # Подготавливаем данные для записи (оставляем только необходимые поля)
        expensive_data = [{"code": c["code"], "name": c["name"], "price": c["price"]} for c in expensive]
        low_pe_data = [{"code": c["code"], "name": c["name"], "P/E": c["pe_ratio"]} for c in low_pe]
        high_growth_data = [{"code": c["code"], "name": c["name"], "growth": c["growth"]} for c in high_growth]
        high_profit_data = [{"code": c["code"], "name": c["name"], "potential profit": c["potential_profit"]} for c in high_profit]

        # Сохраняем в JSON-файлы
        with open("expensive_companies.json", "w", encoding="utf-8") as f:
            json.dump(expensive_data, f, ensure_ascii=False, indent=4)
        with open("low_pe_companies.json", "w", encoding="utf-8") as f:
            json.dump(low_pe_data, f, ensure_ascii=False, indent=4)
        with open("high_growth_companies.json", "w", encoding="utf-8") as f:
            json.dump(high_growth_data, f, ensure_ascii=False, indent=4)
        with open("high_profit_companies.json", "w", encoding="utf-8") as f:
            json.dump(high_profit_data, f, ensure_ascii=False, indent=4)

        print("JSON-файлы успешно сохранены.")

if __name__ == "__main__":
    asyncio.run(main())
