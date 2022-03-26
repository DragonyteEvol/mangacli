from bs4 import BeautifulSoup
import threading
import requests
import os
import errno

# Genera un array de los capitulos a descargar
def generateCaps(num_1,num_2):
    caps=[num_1]
    num_variable=num_1
    while num_2>num_1:
        num_variable=num_variable+1
        caps.append(num_variable)
        num_1+=1
    return caps #Array de capitulos

# Genera el nombre del manga a apartir de la url
def generateMangaName(url):
    manga_name = str(url).replace("https://tumangaonline.site/manga/","")
    return manga_name


def scrapTumangaonline(url,arrayCaps):
    for cap in arrayCaps:
        folder = createMangaFolder(url,cap)
        # thread = threading.Thread(target=createMangaFolder,args=(url,cap))
        # folder = thread.start()
        for page_cap in range(505):
            url_cap_page=url + "/" + str(cap) + "/p/" + str(page_cap + 1) #Url con el capitulo y la pagina
            if(downloadCaps(url_cap_page,cap,page_cap+1,folder)==False):
                break
    return True

def requestImages(url):
    response = requests.get(url)
    soup=BeautifulSoup(response.content,'lxml')
    # wp-manga-chapter-img img-responsive effect-fade lazyloaded
    tags=soup.find_all('img',{'class','wp-manga-chapter-img'})
    return tags

def createMangaFolder(url,cap):
    try:
        folder_route = 'manga/' + generateMangaName(url) + str(cap) + '/'
        os.makedirs(folder_route)
        return folder_route
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

def saveImage(url,route):
    image = requests.get(url)
    open(route,'wb').write(image.content)


def downloadCaps(url,cap,page,folder_route):
    tags = requestImages(url)
    if(len(tags) > 0):
        data_source = tags[0].get('data-src')
        route_image = folder_route + str(page) + ".webp"
        print(route_image)
        # saveImage(data_source,route_image)
        thread = threading.Thread(target=saveImage,args=(data_source,route_image))
        thread.start()
        return True
    else:
        return False

