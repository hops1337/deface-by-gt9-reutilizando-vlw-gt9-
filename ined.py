# This code is not mine. Im just hosting this.
# Code writter: ct4eiros> ayo.so/m2hcz

import requests
from bs4 import BeautifulSoup
import concurrent.futures
from urllib.parse import quote, urlparse, parse_qs, unquote

def print_banner():
    b = """
Searcher
██╗███╗░░██╗███████╗██████╗░
██║████╗░██║██╔════╝██╔══██╗
██║██╔██╗██║█████╗░░██║░░██║
██║██║╚████║██╔══╝░░██║░░██║
██║██║░╚███║███████╗██████╔╝
╚═╝╚═╝░░╚══╝╚══════╝╚═════╝░
    """
    print(b)

def extrair_url_duckduckgo(link):
    original = link.get('href')
    if original and "duckduckgo.com/l/?uddg=" in original:
        parsed = urlparse(original)
        qs = parse_qs(parsed.query)
        if 'uddg' in qs:
            return unquote(qs['uddg'][0])
    return original

def buscar(url, engine, max_res):
    print(f"\n[+] Buscando em: {url}\nEngine: {engine}")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        if engine == "bing":
            resultados = soup.find_all("li", class_="b_algo")[:max_res]
            for i, item in enumerate(resultados, 1):
                h2 = item.find("h2")
                if h2:
                    link = h2.find("a")
                    if link:
                        print(f"{i}. {link.get('href')}")

        elif engine == "duckduckgo":
            resultados = soup.find_all("a", {"class": "result__a"})[:max_res]
            for i, link in enumerate(resultados, 1):
                url_real = extrair_url_duckduckgo(link)
                print(f"{i}. {url_real}")

        elif engine == "yahoo":
            resultados = soup.find_all("div", class_="dd algo")[:max_res]
            for i, item in enumerate(resultados, 1):
                lk = item.find("a")
                if lk:
                    print(f"{i}. {lk.get('href')}")

    except:
        print("[!] Erro ou tempo excedido.")

def montar_consultas(q, site, advanced):
    consultas = []
    base = q
    if site:
        base = f"site:{site} {q}"
    consultas.append(base)
    if advanced:
        consultas.append(f"{advanced}:{q}")
    return consultas

def executar_busca(q, site, advanced, num=5):
    print_banner()
    engines = {
        "bing": "https://www.bing.com/search?q=",
        "duckduckgo": "https://html.duckduckgo.com/html?q=",
        "yahoo": "https://search.yahoo.com/search?p="
    }
    consultas = montar_consultas(q, site, advanced)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for engine, base in engines.items():
            for c in consultas:
                url = base + quote(c)
                executor.submit(buscar, url, engine, num)

def main():
    while True:
        q = input("Consulta: ")
        site = input("Site (opcional): ")
        advanced = input("Operador avançado (intitle, inurl, intext, etc. ou vazio): ")
        num = int(input("Número de resultados (padrão=5): ") or 5)
        executar_busca(q, site, advanced, num)
        if input("Nova consulta? (s/n): ").lower() != 's':
            break

if __name__ == "__main__":
    main()
