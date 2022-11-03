## Version: 0.7
## 20221007
## Tercera versión completamente funcional, ya no tan fea.
## Es un PMV
## ¿Que si habrá mejoras? No lo sé.
## Dependerá de su utilidad real en el trabajo
## Al haber aprendido a usar Mail Merge correctamente, nos interesa
## que los nombres de los ficheros sean similares, sólo separados por el DNI

## La versión 0.7 incorpora:
##      - selección del directorio a través de un botón, con la función popup_get_folder

## La versión 0.6 incorpora: - selección de cualquier texto como 'texto de corte', y funciona
##                           - selección de texto de corte a través de una ventana emergente, pop-up



import PySimpleGUI as sg
import PyPDF2
import os
import shutil


def renombrar_un_fichero(carpeta_de_trabajo, nombre_antiguo, texto_corte = "DNI "):
    """Modifica el nombre de un pdf (certificado de un curso) usando el DNI contenido en ese mismo fichero pdf. """
    # Variables: objeto, y 4 palabras elegidas

    # contendrá el texto del PDF
    text = ''
    # el nuevo nombre del fichero
    #nuevo_nombre = ''
    nombre_antiguo_completo: str = carpeta_de_trabajo + '/' + nombre_antiguo
    pdfFileObj = open(nombre_antiguo_completo, 'rb')

    # La variable pdfReader es un objeto legible que será parseado
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Averiguar el nº de páginas permite extraer de cualquier parte del documento
    num_pages = pdfReader.numPages
    count = 0

    # Leemos el contenido de todas las páginas y las carga en la variable text.
    while count < num_pages:
        pageObj = pdfReader.getPage(count)
        count += 1
        text += pageObj.extractText()

    # Comprobación para evitar errores. It's done because PyPDF2 cannot read scanned files.
    if text != "":
        text = text
    # Por si hay error
    else:
        text = "Hubo algún error."
    # 'Text' contiene todo el texto del PDF. Partimos en el punto donde se sitúa el DNI: [0] es anterior, [1] el nº y
    #  lo siguiente
    palabras = text.split(texto_corte)
    # Separamos todas las palabras que nos sobran, a partir del espacio. La primera palabra es el nº DNI
    dni0 = palabras[1].split(" ")[0]
    if len(dni0) < 3:
        dni0 = palabras[1].split(" ")[1]

    # eliminamos /n si lo hay
    dni = dni0[:9]

    # Ahora, renombrar el fichero
    ## Versión para mantener el nombre antiguo COMPLETO:
    #nuevo_nombre = dni + " " + nombre_antiguo.split('.')[0] + ".pdf"

    ## Versión para recortar el nº final del nombre antiguo:
    nuevo_nombre = dni + " " + nombre_antiguo.split('.')[0][:-4] + ".pdf"

    nuevo_nombre_completo = carpeta_de_trabajo + "/" + nuevo_nombre
    print(nuevo_nombre_completo)
    # Se cambia el nombre antiguo por el nuevo
    #os.rename(nombre_antiguo_completo, nuevo_nombre_completo)
    shutil.copy2(nombre_antiguo_completo, nuevo_nombre_completo)
    # Si todo ha ido bien, imprime los dos nombres
    print(nombre_antiguo, " --> ", nuevo_nombre)

def mostrarListaFicheros(carpeta_de_trabajo):
    return os.listdir(carpeta_de_trabajo)


    # Verificar la Carpeta de trabajo
    # Esta es la carpeta donde debes situar los ficheros que quieres renombrar, y su contenido actual:
carpeta_de_trabajo = ''
print(carpeta_de_trabajo)
print('Contenido:' )
#os.listdir(carpeta_de_trabajo)


def func_pral(dir_de_trabajo):
    # Bucle principal
    lista_ficheros = os.listdir(dir_de_trabajo)
    print("Nº de ficheros a procesar: ", len(lista_ficheros))

    for fichero in lista_ficheros:
      renombrar_un_fichero(dir_de_trabajo, fichero, txtCorte)

    print ("FIN.")


# =================== GUI =============================
sg.theme('BluePurple')

layout_l = [[sg.Text('Contenido inicial:')],
           [sg.Output(size=(50, 10), key='-IN_OUTPUT-')]]


layout_i = [[sg.Button('Transformar')]]

layout_r = [[sg.Text('Contenido final:')],
            [sg.Output(size=(60, 10), key='-IN_OUTPUT2-')]]


layout =    [[sg.Text('Texto de corte: '), sg.Text('DNI ', background_color= 'white', key = '-TXT_CORTE-'), sg.Button('Cambiar')],
            [sg.Text('Elegir directorio:', key ='-TX_F-'), sg.Button('Elegir dir')],
#            [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(enable_events=True, key='-FOLDERNAME-'), sg.Text(carpeta_de_trabajo), sg.Button('Cargar')],
            [sg.Text('Directorio elegido:'), sg.Text(size=(100,2), key='-DIR_OUTPUT-')],
            [sg.Col(layout_l, p=0), sg.Col(layout_i, p=0), sg.Col(layout_r, p=0)],
            [sg.Button('Exit')]]

window = sg.Window('Añadir DNI al nombre de pdf', layout)
txtCorte = 'DNI '
while True:  # Event Loop
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Elegir dir':
        eleg_dir = sg.popup_get_folder('Mensaje')
        window['-DIR_OUTPUT-'].update(eleg_dir)
        window['-IN_OUTPUT-'].update(mostrarListaFicheros(eleg_dir))


    if event == 'Cambiar':
        #sg.popup("Cancel", "No filename supplied")
        txtCorte = sg.popup_get_text('Mensaje')
        window['-TXT_CORTE-'].update(txtCorte)

    if event == 'Cargar':
        # Update the "output" text element to be the value of "input" element
        #dir_elegido = values['-FOLDERNAME-']
        window['-DIR_OUTPUT-'].update(values['-FOLDERNAME-'])
        window['-IN_OUTPUT-'].update(mostrarListaFicheros(values['-FOLDERNAME-']))
    #    window['-IN_OUTPUT2-'].update("Aquí vendrá el nuevo nombre")

    if event == 'Transformar':
        window['-IN_OUTPUT2-'].update("Aquí vendrá el nuevo nombre")
        func_pral(eleg_dir)
        window['-IN_OUTPUT2-'].update(mostrarListaFicheros(eleg_dir))


window.close()



## Revisar: Recipe - Get Filename With No Input Display. Returns when file selected
## Revisar: popup_get_folder, en Call Reference: https://www.pysimplegui.org/en/latest/call%20reference/#popups-pep8-versions