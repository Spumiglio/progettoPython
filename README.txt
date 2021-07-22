Autori: Burati Mattia, Gugole Luca, Enrico Zorzi
Nome del progetto: Escape the bomb!

Descrizione del progetto:
Il progetto si occupa di caricare lo shapefile del Comune di Verona e produrre una mappa esplicativa. Si suppone che nell'area del Comune sia stata trovata una bomba della seconda guerra mondiale. Il programma calcola casualmente una coordinata all'interno del confine e produce un'area (buffer) del raggio di 1 km che sarà segnata sulla mappa.
In quell'area verranno caricati sulla mappa gli edifici (sottoforma di shapefile) in modo da poter visualizzare e quantificare gli edifici da evacuare.
Il risultato prodotto consiste in due mappe rispettivamente della zona di Verona e uno zoom sulla zona da evacuare.

Input: comune_verona.shp, edifici_verona.shp
Output: map.html, area_map.html

Invocazione del codice: di seguito è riportato il codice che descrive le funzioni che abbiamo creato e chiamato.
    verona, building = read_data()
    verona_map = create_map(verona)
    bomb_point = generate_random_point(verona)
    buffer_around_point(verona_map, building, bomb_point)

    save_map(verona_map, bomb_point)
