## Version: 0.8
## 20221007 --> 202210XX
## Cuarta versión completamente funcional, ya no tan fea.
''' Objetivo 0.9: Versión casi Beta

La versión 0.9 debe incorporar:
  - Versión .exe sin alerta antivirus
  - Poder elegir entre:
        - mantener el nombre antiguo COMPLETO
        - recortar del nombre antiguo el número final (_00X)
  - GUI: listado de ficheros en formato texto, como el programa de ejemplo con los JPG
'''

## Objetivo 0.8: Pasar de un PMV a una versión tolerante a fallos

## La versión 0.8 debe incorporar:
##  ok - If name = main
##  ok - Generar versión .exe
##  ok - Proyecto en Github
##  ok - Error de selección de palabra de corte (texto vacío)
##  ok - Error de directorio vacío: No pasa nada, la lista está vacía.
##  ok - activar botón transformar después de la selección del directorio
##  ok - Error de directorio sin pdf (¿qué ocurre? Nada, no cambia nada.)
##  ok - Error de directorio con mezcla de ficheros pdf y otros



## La versión 0.7 incorpora:
##      - selección del directorio a través de un botón, con la función popup_get_folder

## La versión 0.6 incorpora: - selección de cualquier texto como 'texto de corte', y funciona
##                           - selección de texto de corte a través de una ventana emergente, pop-up


##
## Revisar: Recipe - Get Filename With No Input Display. Returns when file selected
## Revisar: popup_get_folder, en Call Reference: https://www.pysimplegui.org/en/latest/call%20reference/#popups-pep8-versions



import PySimpleGUI as sg
import PyPDF2
import os
import shutil

def funcMain():
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
        with os.scandir(carpeta_de_trabajo) as ficheros:
            ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.pdf')]

        return ficheros


    def func_pral(dir_de_trabajo):
        # Bucle principal
        try:
            with os.scandir(dir_de_trabajo) as ficheros:
                lista_ficheros = [fichero.name for fichero in ficheros if fichero.is_file() and fichero.name.endswith('.pdf')]

            print("Nº de ficheros a procesar: ", len(lista_ficheros))

            for fichero in lista_ficheros:
                renombrar_un_fichero(dir_de_trabajo, fichero, txtCorte)
        except:
            print("Hubo un error.")

        print ("FIN.")



    # :::::::::::::::::: Ciclo principal y GUI ::::::::::::::::::::::::::
    # Verificar la Carpeta de trabajo
    # Esta es la carpeta donde debes situar los ficheros que quieres renombrar, y su contenido actual:
    carpeta_de_trabajo = ''
    #print(carpeta_de_trabajo)
    #print('Contenido:' )
    #os.listdir(carpeta_de_trabajo)

    # =================== GUI =============================
    sg.theme('BluePurple')

    layout_l = [[sg.Text('Contenido inicial:')],
               [sg.Output(size=(50, 10), key='-IN_OUTPUT-')]]


    layout_i = [[sg.Button('Transformar', key ='Transformar')]]

    layout_r = [[sg.Text('Contenido final:')],
                [sg.Output(size=(60, 10), key='-IN_OUTPUT2-')]]


    layout =    [[sg.Text('Texto de corte: '), sg.Text('DNI ', background_color= 'white', key = '-TXT_CORTE-' , metadata = 'DNI '), sg.Button('Cambiar')],
                [sg.Text('Elegir directorio:', key ='-TX_F-'), sg.Button('Elegir dir')],
    #            [sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse(enable_events=True, key='-FOLDERNAME-'), sg.Text(carpeta_de_trabajo), sg.Button('Cargar')],
                [sg.Text('Directorio elegido:'), sg.Text('Antes de nada, elige un directorio.', size=(100,2), key='-DIR_OUTPUT-')],
                [sg.Col(layout_l, p=0), sg.Col(layout_i, p=0), sg.Col(layout_r, p=0)],
                [sg.Button('Exit')]]

    window = sg.Window('Añadir DNI al nombre de pdf', layout, finalize=True)
    txtCorte = 'DNI '
    window['Transformar'].update(disabled=True)

    while True:  # Event Loop
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Exit':
            break

        if event == 'Elegir dir':
            eleg_dir = sg.popup_get_folder('Mensaje')
            window['-DIR_OUTPUT-'].update(eleg_dir)
            window['-IN_OUTPUT-'].update(mostrarListaFicheros(eleg_dir))
            window['Transformar'].update(disabled=False)


        if event == 'Cambiar':
            # almacena el valor antiguo por si hay que volver a él
            txtAntiguo = window['-TXT_CORTE-'].metadata
            # pide un nuevo valor
            txtCorte = sg.popup_get_text('Mensaje')
            # gestión de error: si no elige ningún caracter o palabra
            if len(txtCorte) <1:
                sg.popup("Ok", "Elige al menos un caracter de corte.")
                # vuelve al valor anterior
                txtCorte = txtAntiguo
            # actualiza valores
            window['-TXT_CORTE-'].update(txtCorte)
            window['-TXT_CORTE-'].metadata = txtCorte


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


if __name__ == "__main__":
    funcMain()


'''
Obtener un .exe sin alerta anti-virus es una tortura

He probado: (py2exe), pyinstaller, niutka... y todos acaban en una alerta antivirus. ¿Cómo evitarlo?
Algunas ideas interesantes:
    - [método derivado de pyinstaller, dos posts]
    - Reflexión más interesante, y de la que se derivan dos caminos: https://stackoverflow.com/questions/69899867/python-script-distribution-on-windows-options-to-avoid-virus-false-positives
        - Interesante pero poco práctico: https://medium.com/@markhank/how-to-stop-your-python-programs-being-seen-as-malware-bfd7eb407a7
        - Python embebido, LA ÚNICA respuesta a ese post (¿sospechoso?) que voy a probar estos días:
            """This may be the best option: use the embeddable package as downloaded from python.org. The official docs spell it out in the second half of section 4.4.1 of 'Using Python on Windows'.
                In their downloads pages, after selecting a version, you can get to a page like this (for python 3.10):
                Download the 'Windows embeddable package' for 32 or 64 as needed. Let's say you extract the downloaded zip to $MYDIR. Then to run your python script, e.g. from a Windows batch file, you could just have a line like
                call $MYDIR\python.exe myscript.py
                Zero threats detected on virustotal.com for $MYDIR\python.exe, since it's known and signed and trusted and unmodified. Just to be sure, I did a Windows scan of the entire directory that contains the batch file, myscript.py, and $MYDIR - no threats detected.
                This flow appears to work for this application so far. Will wait to accept this answer until it's been working for a few days.
                The downloaded 32bit embeddable package is 7.1MB and unzips to 15.6MB - not huge, not tiny, but sufficiently small for this particular app.
                Does anyone have experience with this embeddable package solution, and might know of any caveats or pitfalls?"""
    Probaré a embeber el python, a ver.
    Referencia: cómo añadir Tkinker a un python embebido: https://stackoverflow.com/questions/37710205/python-embeddable-zip-install-tkinter#


'''
