import asyncio
import json
import re
from playwright.async_api import async_playwright

async def get_pet_ids_from_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Загружаем страницу с картой
        print("Загрузка карты питомцев...")
        await page.goto("https://petsi.app/ru/petsi-map")
        
        # Ждем загрузку контента
        await page.wait_for_timeout(5000)
        
        # Извлекаем все ID из div с классом pet-data
        pet_data_divs = await page.query_selector_all("div.pet-data")
        
        pet_ids = []
        for div in pet_data_divs:
            div_id = await div.get_attribute("id")
            if div_id:
                # Извлекаем часть после подчеркивания (lost_ или found_)
                match = re.search(r"(?:lost|found)_([a-z0-9]+)", div_id)
                if match:
                    pet_id = match.group(1)
                    pet_ids.append(pet_id)
        
        await browser.close()
        print(f"Найдено {len(pet_ids)} питомцев на карте")
        return pet_ids

async def parse_pet_details(pet_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Загружаем страницу
        url = f"https://petsi.app/ru/pet-details/{pet_id}"
        print(f"Парсинг данных питомца: {url}")
        await page.goto(url)
        
        # Ждем загрузку страницы
        await page.wait_for_timeout(3000)
        
        # Инициализируем структуру данных
        pet_data = {
            "id": pet_id,
            "name": "",
            "gender": "",
            "descriptions": [],
            "images": [],
            "address": "",
            "owner_phone": ""
        }
        
        try:
            phone_element = await page.query_selector("div.pet-header__right a.btn.btn-primary")
            if phone_element:
                phone_href = await phone_element.get_attribute("href")
                if phone_href and phone_href.startswith("tel:"):
                    pet_data["owner_phone"] = phone_href.replace("tel:", "")
                    
        except Exception as e:
            print(f"Ошибка при извлечении номера телефона: {e}")
        # Извлекаем имя и пол
        name_element = await page.query_selector("p.pet-name")
        if name_element:
            name_html = await name_element.inner_html()
            name_text = await name_element.inner_text()
            pet_data["name"] = name_text.strip()
            
            # Определяем пол по svg
            if "#female" in name_html:
                pet_data["gender"] = "female"
            elif "#male" in name_html:
                pet_data["gender"] = "male"
        
        # Извлекаем описания
        descr_elements = await page.query_selector_all("p.pet-descr")
        for elem in descr_elements:
            text = await elem.inner_text()
            text = text.strip()
            if text:
                pet_data["descriptions"].append(text)
        
        # Извлекаем URL изображения из background-image
        bg_image = await page.evaluate("""
            () => {
                const img = document.querySelector('div.pet-img');
                if (img) {
                    const style = window.getComputedStyle(img);
                    const bg = style.backgroundImage;
                    return bg.replace(/^url\\(['"](.+)['"]\)$/, '$1');
                }
                return '';
            }
        """)
        if bg_image:
            pet_data["images"].append(bg_image)
        
        # Извлекаем адрес
        address_element = await page.query_selector("a.pet-address")
        if address_element:
            address = await address_element.inner_text()
            pet_data["address"] = address.strip()
        
        await browser.close()
        return pet_data
