# pdf2name
ABSTRACT: Extracts some _word_ from _inside_ pdf file, and rename that file including _that word_. 

Processes all pdf files contained in a folder.

---

Este pequeño código permite modificar el nombre de una serie de ficheros usando alguna palabra (distintiva) del interior de cada fichero. Ejemplos de uso:
- una serie de certificados de asistencia, otorgados a distintas personas: para distinguirlos en una carpeta, se modifican los nombres de los ficheros usando en cada uno de ellos el número DNI de cada persona;
- una serie de facturas, con nombres similares: se modifican para incluir la fecha en el nombre de cada fichero.
- ...

Escrito en Python, utiliza los siguientes módulos:
- PyPDF2: tratamiento y manipulación de ficheros pdf.
- PySimpleGUI: construcción de GUI.

Versión ejecutable: basada en la versión embebida de Python, única solución después de probar varias (py2exe, pyinstaller, niutka) que acaban en una alerta antivirus. Disponible en la sección 'Release'.

Aún en desarrollo.
