from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import datetime


def obter_nomes_filmes(driver, contador):
    try:
        elemento = driver.find_element(By.XPATH, f"(//*[@class='month-movies-link'])[{contador}]")

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f"(//*[@class='month-movies-link'])[{contador}]")))
        elemento.click()

        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='xXx date blue-link']")))

        data_lancamento = driver.find_element(By.XPATH, "//*[@class='xXx date blue-link']").text
        nome_filme = driver.find_element(By.XPATH, "//*[contains(@class,'titlebar-title titlebar-title-xl')]").text

        try:
            sinapse = driver.find_element(By.XPATH, "//p[@class='bo-p']").text
        except:
            sinapse = "Sinopse não disponível"

        json = {
            "data_lancamento": data_lancamento,
            "nome_filme": nome_filme,
            "sinopse": sinapse
        }

        return json
    except Exception as e:
        return False

def obter_dados():
    options = Options()
    options.add_argument("--disable-logging")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--log-level=3")
    options.add_argument("--headless")  # Executar em modo headless (sem interface gráfica)

    driver = webdriver.Chrome(options=options)
    driver.get("https://www.adorocinema.com/filmes/agenda/mes/")

    driver.find_element(By.XPATH, "//div[@id='js-cookie-info']//span[text()='OK']").click() #Aceitar cookies

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//*[@class='dropdown-select']")))

    date = datetime.datetime.now().strftime("%Y-%m")

    driver.execute_script(f"""
        document.querySelector('.dropdown-select-inner.js-select-change').value = '/filmes/agenda/mes/mes-{date}/';
        document.querySelector('.dropdown-select-inner.js-select-change').dispatchEvent(new Event('change'));
    """)

    cont = 1
    validacao = True

    lista = []

    while validacao:
        valor = obter_nomes_filmes(driver, cont)
        if not valor is False:
            lista.append(valor)
            cont += 1
            driver.back()
        else:
            validacao = False
    
    return lista