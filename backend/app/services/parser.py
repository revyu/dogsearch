import asyncio
import re
from playwright.async_api import async_playwright

async def get_pet_ids_from_map():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(
                "https://petsi.app/ru/petsi-map",
                timeout=180000,  
                wait_until="domcontentloaded"  
            )
            
            #дополнительное ожидание для загрузки контента
            await page.wait_for_selector("div.pet-data", 
                                       timeout=30000,
                                       state="attached")
            
            
            pet_data_divs = await page.query_selector_all("div.pet-data")
            
            pet_ids = []
            for div in pet_data_divs:
                div_id = await div.get_attribute("id")
                if div_id:
                    match = re.search(r"(?:lost|found)_([a-z0-9]+)", div_id)
                    if match:
                        pet_id = match.group(1)
                        pet_ids.append(pet_id)
            
            return pet_ids
            
        except Exception as e:
            print(f"Ошибка при загрузке карты: {e}")
            return []
        finally:
            await browser.close()

async def parse_pet_details(pet_id):
    # Инициализируем структуру данных в начале функции
    pet_data = {
        "id": pet_id,
        "name": "",
        "gender": "",
        "descriptions": [],
        "images": [],
        "address": "",
        "owner_phone": ""
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-dev-shm-usage', '--no-sandbox']
        )
        page = await browser.new_page()
        
        try:
            url = f"https://petsi.app/ru/pet-details/{pet_id}"
            print(f"Парсинг данных питомца: {url}")
            
            # Меняем параметры загрузки страницы
            await page.goto(
                url,
                wait_until="domcontentloaded",  # Менее строгое условие
                timeout=60000  # Уменьшаем таймаут
            )
            
            # Ждем появления основного контента
            await page.wait_for_selector("div.pet-header", 
                state="attached",  # Менее строгое условие
                timeout=30000
            )
            
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
                    # Поиск телефона в описании
                    phone_match = re.search(r'\+375\d{9}', text)
                    if phone_match:
                        pet_data["owner_phone"] = phone_match.group(0)
            
            # Извлекаем URL изображения из background-image
            bg_image = await page.evaluate("""
                () => {
                    const img = document.querySelector('div.pet-img');
                    if (img) {
                        const style = window.getComputedStyle(img);
                        const bg = style.backgroundImage;
                        return bg.replace(/^url\\(['"](.+)['"]\\)$/, '$1');
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
            
            return pet_data
            
        except Exception as e:
            print(f"Ошибка при парсинге питомца {pet_id}: {str(e)}")
            return pet_data  # Возвращаем пустую структуру в случае ошибки
        finally:
            await browser.close()
