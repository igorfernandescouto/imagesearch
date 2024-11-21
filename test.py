#pip install requests pillow opencv-python numpy

def search_images(query, count=10, offset=0):
    # Define os cabeçalhos da requisição, incluindo a chave de API do Bing
    headers = {"Ocp-Apim-Subscription-Key": BING_SEARCH_API_KEY}
    # Define os parâmetros da requisição, incluindo a consulta, contagem de resultados e offset
    params = {
        "q": query,
        "count": count,
        "offset": offset,
        "safeSearch": "Off"  # Desativa o SafeSearch
    }
    # Faz a requisição GET para a API de busca de imagens do Bing
    response = requests.get(BING_SEARCH_URL, headers=headers, params=params)
    # Verifica se a requisição foi bem-sucedida
    response.raise_for_status()
    # Converte a resposta JSON em um dicionário Python
    search_results = response.json()
    # Retorna uma lista de URLs das imagens encontradas
    return [img["contentUrl"] for img in search_results["value"]]

def load_images_from_urls(urls):
    images = []
    # Define os cabeçalhos da requisição para simular um navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.google.com/"
    }
    # Itera sobre cada URL fornecida
    for url in urls:
        try:
            # Faz a requisição GET para a URL da imagem
            response = requests.get(url, headers=headers)
            # Verifica se a requisição foi bem-sucedida
            response.raise_for_status()
            # Abre a imagem a partir do conteúdo da resposta
            img = Image.open(BytesIO(response.content))
            # Adiciona a URL e a imagem à lista de imagens
            images.append((url, img))
        except (requests.RequestException, UnidentifiedImageError):
            # Ignora erros de requisição ou de abertura de imagem
            continue
    # Retorna a lista de imagens carregadas
    return images

def filter_images(query, min_width, min_height, desired_count):
    # Busca URLs de imagens com base na consulta
    urls = search_images(query, count=desired_count)
    # Carrega as imagens a partir das URLs
    images = load_images_from_urls(urls)
    filtered_images = []
    # Itera sobre cada imagem carregada
    for url, img in images:
        # Verifica se a imagem atende aos critérios de largura e altura mínimas
        if (min_width == "x" or img.width >= int(min_width)) and (min_height == "x" or img.height >= int(min_height)):
            # Adiciona a imagem à lista de imagens filtradas
            filtered_images.append((url, img))
        # Verifica se já atingiu a contagem desejada de imagens
        if len(filtered_images) >= desired_count:
            break
    # Retorna a lista de imagens filtradas
    return filtered_images

def save_images(images, folder):
    # Cria a pasta de destino se ela não existir
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Itera sobre cada imagem a ser salva
    for url, img in images:
        # Define o nome do arquivo com base na URL da imagem
        img_name = os.path.join(folder, os.path.basename(url))
        # Salva a imagem no caminho especificado
        img.save(img_name)

if __name__ == "__main__":
    # Define a consulta de busca
    query = "Xiaomi Redmi Note 10 PRO"
    # Define a largura mínima (use "x" para qualquer largura)
    min_width = "x"
    # Define a altura mínima (use "x" para qualquer altura)
    min_height = "x"
    # Define o número desejado de imagens válidas
    desired_count = 10
    # Filtra as imagens com base nos critérios definidos
    selected_images = filter_images(query, min_width, min_height, desired_count)
    # Salva as imagens filtradas na pasta 'imagens'
    save_images(selected_images, 'imagens')
    # Imprime uma mensagem indicando que as imagens foram salvas
    print("Selected images saved in 'imagens' folder.")