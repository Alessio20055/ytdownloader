from django.shortcuts import render, redirect, HttpResponse
from .pytubefix import YouTube
from .pytubefix.exceptions import RegexMatchError
from os import path, listdir, remove, rename, makedirs
from pathlib import Path
from django.http import FileResponse
from ytdownloader.settings import BASE_DIR

def index(request):
    return render(request, 'main/index.html')

def getAudio(request):
    if request.method == "POST":
        try:
            LINK = request.POST['link']
            cartella_tmp = path.join('/tmp')

            if not path.exists(cartella_tmp + '/audio'):
                # Crea la cartella
                makedirs(cartella_tmp + '/audio')

            cartella_audio = path.join('/tmp/audio')

            #Rimozione file audio esistenti (per non intasare il server)
            if listdir(cartella_audio) != []:
                for x in listdir(cartella_audio):
                    remove(cartella_audio + x)
            
            #Creazione oggetto del video YT
            yt = YouTube(LINK)

            #Selezione stream con abr=128kbps
            itag = None
            for x in yt.streams.filter(only_audio=True):
                if x.abr == "128kbps":
                    itag = x.itag

            #Download del video
            stream = yt.streams.get_by_itag(itag)
            downloaded_file = stream.download(output_path=cartella_audio).split('\\')[-1]

            #Rinominazione (cambio di formato) in .mp3
            vecchio_percorso = path.join(cartella_audio, f"{downloaded_file}")
            nuovo_percorso = path.join(cartella_audio, f"nuovo.mp3")

            rename(vecchio_percorso, nuovo_percorso)

            #Download file
            file_server = Path(nuovo_percorso)
            file_to_download = open(str(file_server), 'rb')
            response = FileResponse(file_to_download, content_type='application/force-download')
            response['Content-Disposition'] = f"inline; filename={title}.mp3"
            return response
            
        except RegexMatchError:
            return redirect('error')

        except Exception as e:
            print("ERRORE:", e)
            return HttpResponse("<h1>Errore</h1>")
    
    return redirect('index')

def errore(request):
    return render(request, 'main/error.html')
