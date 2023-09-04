#----------------------------------------------------------Librerias varias
import datetime
import json
import os
import sys
import time
#----------------------------------------------------------Librerias de Tkinter
import tkinter as tk
import tkinter.font as font
#----------------------------------------------------------Librerias Especificas de Tkinter
from tkinter import filedialog, messagebox, ttk, simpledialog
#----------------------------------------------------------Librerias para procesar Excel
import pandas
#----------------------------------------------------------Librerias Especificas varias
from PIL import Image, ImageTk
#----------------------------------------------------------Archivos de Lista
from ListaFilas import ListaFilas
from Mensaje import Mensaje
from Frutas import Frutas
#----------------------------------------------------------Componentes modificados

class Ventana(tk.Tk):
    def __init__(self):
        super().__init__()

        #----------------------------------------------------------Cambia al directorio actual
        os.chdir(os.getcwd())
        #----------------------------------------------------------Guarda la salida estándar original
        self.original_stdout = sys.stdout

        #----------------------------------------------------------Redirige la salida estándar al archivo 'output.txt'
        sys.stdout = open('Temp.txt', 'w')
        print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Incia Ejecucion de Programa\n')
        self.protocol('WM_DELETE_WINDOW', self.salir)
        #----------------------------------------------------------Declaracion de Obejetos dentro de la ventana
        self._listaPrecios = ListaFilas()
        self._dataframe = None
        self._mensaje = Mensaje()
        self._frutas = Frutas()
        #----------------------------------------------------------Opciones de Configuración de la Ventana(Semi Automatico pero distingue pantalla principal)
        self._anchoVentana = 1550
        self._altoVentana = 850

        self._xVentana = self.winfo_screenwidth() // 2 - self._anchoVentana // 2
        self._yVentana = self.winfo_screenheight() // 2 - self._altoVentana // 2

        self._posicion = f'{str(self._anchoVentana)}x{str(self._altoVentana)}+{str(self._xVentana)}+{str(self._yVentana-40)}'
        self.minsize(self._anchoVentana, self._altoVentana)
        self.geometry(self._posicion)
        #----------------------------------------------------------Opciones de Configuración de la Ventana (Automatico pero no distingue entra mas de 1 pantalla)
        # self.update()
        # self.minsize(self.winfo_width(), self.winfo_height())
        # self._x_cordinate = int((self.winfo_screenwidth()/2) - (self.winfo_width()/2))
        # self._y_cordinate = int((self.winfo_screenheight()/2) - (self.winfo_height()/2))
        # self.geometry("+{}+{}".format(self._x_cordinate, self._y_cordinate))
        #----------------------------------------------------------Configuracion Responsiva 
        self.columnconfigure(index=0, weight=1)
        self.rowconfigure(index=0, weight=1)
        #----------------------------------------------------------Configuracion de Estilo de la ventana
        self.title('Excel a WhatsApp con Python (Lista de Precios Power Bi)')
        self.iconbitmap('img/logo.ico')
        self.style = ttk.Style(self)
        #----------------------------------------------------------Metodo Call agrega los estilos de la carpeta raiz .tcl
        self.tk.call('source', 'forest-light.tcl')
        self.tk.call('source', 'forest-dark.tcl')
        #----------------------------------------------------------Activa el tema claro a todos los componentes compatibles con ttk
        self.style.theme_use('forest-light')
        #----------------------------------------------------------Declaracion de Notebook para ventanas en Tabs
        self._notebook = ttk.Notebook(self)
        self._notebook.grid(row=0, column=0, sticky=tk.NSEW)
        #----------------------------------------------------------Declaracion de barra de estado y asignacón de estado inicial
        self._barraEstado = tk.StringVar(value='Ventana Inicializada!!!')
        self._itemEditable = None
        self._columnaEditable = None
        self._entradaEditable = None
        self._esDobleClic = False
        self._tema = 'Tema Claro'
        #--------------------------------------------------------------Llama a la funcion que construye los Tabs
        self.principalTabs()

    #----------------------------------------------------------Metodo para cargar la info del layout de Excel hacia la lista de precios (Obj)
    def cargarExcel(self, excel):
        try:
            self._dataframe = pandas.read_excel(excel)
            self._listaPrecios.setElementos([])
            self._listaPrecios.xlsxToObject(self._dataframe)
        except Exception as error:
            print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Error al Cargar Excel: {error}')

    #----------------------------------------------------------Metodo para guardar en el portapapeles la fila seleccionada en el Treeview que se pase como argumento "Ctrl+C"
    def copyToClipBoard(self, event, treeview):
        selectedItem = treeview.focus() 
        if selectedItem:
            portaPapeles = ""
            for elemento in treeview.item(treeview.focus())['values']:
                portaPapeles += f'\t{elemento}'
            self.clipboard_clear()
            self.clipboard_append(portaPapeles.strip())

    #----------------------------------------------------------Metodo que llama el Switch Button para cambiar el tema
    def cambiarTema(self, switch):
        if(not switch):
            self.style.theme_use('forest-light')
            self._tema = 'Tema Claro'
        else:
            self.style.theme_use('forest-dark')
            self._tema = 'Tema Oscuro'
        


    #----------------------------------------------------------Metodo para agregar componenetes al Tab Principal
    def comListaPrecios(self, tabPrincipal):
        #---------------------------------------------------------------Generar Frames Superior para formulario
        superiorFrame = ttk.Frame(tabPrincipal)
        superiorFrame.columnconfigure(index=0, weight=1)
        superiorFrame.columnconfigure(index=1, weight=1)
        superiorFrame.columnconfigure(index=2, weight=1)
        superiorFrame.columnconfigure(index=3, weight=1)
        superiorFrame.columnconfigure(index=4, weight=1)
        superiorFrame.grid(row=0, column=0, sticky=tk.NSEW)
        #---------------------------------------------------------------Generar Frames Superior para formulario
        intraFrame = ttk.Frame(tabPrincipal)
        intraFrame.columnconfigure(index=0, weight=1)
        intraFrame.columnconfigure(index=1, weight=1)
        intraFrame.grid(row=1, column=0, sticky=tk.NSEW)
        #---------------------------------------------------------------Generar Frames inferior para tableApp
        inferiorFrame = ttk.Frame(tabPrincipal)
        inferiorFrame.columnconfigure(index=0, weight=1)
        inferiorFrame.columnconfigure(index=1, weight=1)
        inferiorFrame.grid(row=2, column=0, sticky=tk.NSEW)
        #----------------------------------------------------------Declaracion de SizeGrip
        sizegrip = ttk.Sizegrip(tabPrincipal)
        sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
        #---------------------------------------------------------------Declaración de variables Internas para el TAB
        general = tk.StringVar(value='')
        especie = tk.StringVar(value='')
        variedad = tk.StringVar(value='')
        etiqueta = tk.StringVar(value='')
        calidad = tk.StringVar(value='')
        calibre = tk.StringVar(value='')
        empaque = tk.StringVar(value='')
        presentacion = tk.StringVar(value='')
        articulo = tk.StringVar(value='')
        serieLote = tk.StringVar(value='')
        diasEntrada = tk.StringVar(value='')
        mayoreo = tk.StringVar(value='')
        menudeo = tk.StringVar(value='')
        transito = tk.StringVar(value='')
        costeo = tk.StringVar(value='')
        gdl = tk.IntVar(value=0)
        mex = tk.IntVar(value=0)
        mxl = tk.IntVar(value=0)
        estatus = tk.StringVar(value='')
        contacto = tk.StringVar(value='')

        #----------------------------------------------------------Asigna la fuente al estilo del Treeview, para reducirlo de su tamaño original
        def cambiarFuente(treeview, font_size):
            style = ttk.Style()
            style.configure("Treeview", font=(None, font_size))
            style.configure("Treeview.Heading", font=(None, font_size, "bold"))

        #----------------------------------------------------------Llama a la función principal para cambiar de tema
        #----------------------------------------------------------Esto por que los elementos de Tkinter se vinculan a las funciones pero no pasan parametros
        #----------------------------------------------------------La función principal recibe un bool para cambiar el tema principal
        def cambiarTema():
            if switchTema.instate(['selected']):
                self.cambiarTema(True)
                switchTema['text'] = self._tema
            else:
                self.cambiarTema(False)
                switchTema['text'] = self._tema

        #----------------------------------------------------------Llama a la funcion principal para cargar los datos del layout
        def cargarExcel():
            excel = filedialog.askopenfilename(filetypes=[("Archivos de Excel", "*.xlsx")])
            self.cargarExcel(excel)
            actualizarTreeView()

        #----------------------------------------------------------Al seleccionar una fila del treeview se actualizan las varibales locales
        def seleccionarItem(event):
            try:
                valores = treeView.item(treeView.focus())['values']
                especie.set(valores[0])
                variedad.set(valores[1])
                etiqueta.set(valores[2])
                calidad.set(valores[3])
                calibre.set(valores[4])
                empaque.set(valores[5])
                presentacion.set(valores[6])
                serieLote.set(valores[7])
                diasEntrada.set(valores[8])
                articulo.set(valores[9])
                mayoreo.set(valores[10])
                menudeo.set(valores[11])
                transito.set(valores[12])
                costeo.set(valores[13])
                gdl.set(valores[14])
                mex.set(valores[15])
                mxl.set(valores[16])
                estatus.set(valores[17])
            except Exception as error:
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Actualizacion TreeView en ListaPrecios || {error}')


        def identificarItem(event):
            itemId = treeView.identify('item', event.x, event.y)
            columna = treeView.identify('column', event.x, event.y)
            if(itemId and columna and columna != '#tree'):
                self._itemEditable = itemId
                self._columnaEditable = columna


        def onClic(event):
            identificarItem(event)
            general.set(treeView.set(self._itemEditable, self._columnaEditable))
            entradaGlobal.bind('<Return>', presionarEnter)
            entradaGlobal.bind('<FocusOut>', focusOut)


        def dobleClic(event):
            self._esDobleClic = True
            identificarItem(event)
            editarItem(self._itemEditable, self._columnaEditable)


        def editarItem(item, columna):
            x, y, _, _ = treeView.bbox(item, columna)
            self._entradaEditable = ttk.Entry(treeView, validate="key", textvariable=general)
            self._entradaEditable.place(x=x, y=y, relwidth=1, anchor='w')
            self._entradaEditable.focus_set()
            self._entradaEditable.icursor(tk.END)
            self._entradaEditable.select_range(0, tk.END)
            self._entradaEditable.bind('<Return>', presionarEnter)
            self._entradaEditable.bind('<FocusOut>', focusOut)


        def presionarEnter(event):
            editar(True)

        def focusOut(event):
            editar(False)

        def enter():
            editar(True)


        def editar(guardar=False):
            if (guardar):
                valor = general.get()
                if(self._columnaEditable == '#1'):
                    especie.set(valor)
                elif(self._columnaEditable == '#2'):
                    variedad.set(valor)
                elif(self._columnaEditable == '#3'):
                    etiqueta.set(valor)
                elif(self._columnaEditable == '#4'):
                    calidad.set(valor)
                elif(self._columnaEditable == '#5'):
                    calibre.set(valor)
                elif(self._columnaEditable == '#6'):
                    empaque.set(valor)
                elif(self._columnaEditable == '#7'):
                    presentacion.set(valor)
                elif(self._columnaEditable == '#8'):
                    serieLote.set(valor)
                elif(self._columnaEditable == '#9'):
                    diasEntrada.set(valor)
                elif(self._columnaEditable == '#10'):
                    articulo.set(valor)
                elif(self._columnaEditable == '#11'):
                    mayoreo.set(valor)
                elif(self._columnaEditable == '#12'):
                    menudeo.set(valor)
                elif(self._columnaEditable == '#13'):
                    transito.set(valor)
                elif(self._columnaEditable == '#14'):
                    costeo.set(valor)
                elif(self._columnaEditable == '#15'):
                    gdl.set(valor)
                elif(self._columnaEditable == '#16'):
                    mex.set(valor)
                elif(self._columnaEditable == '#17'):
                    mxl.set(valor)
                elif(self._columnaEditable == '#18'):
                    estatus.set(valor)
                actualizar()
                self._itemEditable = None
                self._columnaEditable = None
            if(self._esDobleClic):
                    self._entradaEditable.destroy()
                    self._esDobleClic = False
                    self._entradaEditable = None
            superiorFrame.focus()


        def limpiarVariables():
            general.set('')
            especie.set('')
            variedad.set('')
            etiqueta.set('')
            calidad.set('')
            calibre.set('')
            empaque.set('')
            presentacion.set('')
            serieLote.set('')
            diasEntrada.set('')
            articulo.set('')
            mayoreo.set('')
            menudeo.set('')
            transito.set('')
            costeo.set('')
            gdl.set(0)
            mex.set(0)
            mxl.set(0)
            estatus.set('')
            contacto.set('')
            actualizarTreeView()


        def copyToClipBoard(event):
            self.copyToClipBoard(event, treeView)


        def simpleDialogShortCode(default, variante):
            return simpledialog.askstring(
                'Agregar ShortCode', 
                f'La variante: {variante}\nNo tiene un ShortCode para emoji definido\n\nIngrese un ShortCode para dicha Variante',
                initialvalue=default
                )


        def agregarShortCode(noInJson):
            defaultShortCode = os.environ.get('SHORTCODE')
            if noInJson:
                for fila in noInJson:
                    variante = fila.getEmoji()[1:-1].strip()
                    newShortCode = simpleDialogShortCode(defaultShortCode, variante)
                    if (newShortCode == None):
                        newShortCode = defaultShortCode
                        filaReal = self._listaPrecios.recuperaFila(
                            fila.getSerieLote(), 
                            fila.getArticulo()
                            )
                        filaReal.setEmoji(':none:')
                    else:
                        self._frutas.__dict__[f'{variante}'] = f'{newShortCode}'
                self._frutas.dictToJson()
                self._frutas = Frutas()
                self._listaPrecios.setFrutas(self._frutas)
                self._mensaje.setFrutas(self._frutas)


        def actualizarTreeView():
            noInJson = []
            estaDentro = False
            #limpiamos el arbol de la vista
            treeView.delete(*treeView.get_children())
            for fila in self._listaPrecios.getElementos():
                treeView.insert(parent='', index='end', values=(
                    fila.getEspecie(),
                    fila.getVariedad(),
                    fila.getEtiqueta(),
                    fila.getCalidad(),
                    fila.getCalibre(),
                    fila.getEmpaque(),
                    fila.getPresentacion(),
                    fila.getSerieLote(),
                    fila.getDiasEntrada(),
                    fila.getArticulo(),
                    fila.getMayoreo(),
                    fila.getMenudeo(),
                    fila.getTransito(),
                    fila.getCosteo(),
                    fila.getGdl(),
                    fila.getMex(),
                    fila.getMxl(),
                    fila.getEstatus()
                ))
                #----------------------------------------------------------Valida si la Key para Emoji devuelve un shortcode o cadena vacia, agrega las filas al arreglo noInJson
                if(not self._listaPrecios.returnShortCode(fila.getEmoji())):
                    if noInJson:
                        for filaJ in noInJson:
                            estaDentro = False
                            if (filaJ.getEmoji() == fila.getEmoji()):
                                estaDentro = True
                    if not estaDentro:
                        noInJson.append(fila)
            #----------------------------------------------------------Llama a la función en cargada de revisar el arreglo de objetos fila y generar ventanas emergentes
            agregarShortCode(noInJson)



        def actualizar():
            if(serieLote.get() != ''  and articulo.get() != ''):
                fila = self._listaPrecios.recuperaFila(serieLote.get(), articulo.get())
                if(f'{menudeo.get()}' != f'{fila.getMenudeo()}'):
                    fila.setMenudeo(menudeo.get())
                else: 
                    fila.setMenudeo(float(mayoreo.get())+20)
                fila.setEspecie(especie.get())
                fila.setVariedad(variedad.get())
                fila.setEtiqueta(etiqueta.get())
                fila.setCalidad(calidad.get())
                fila.setCalibre(calibre.get())
                fila.setEmpaque(empaque.get())
                fila.setPresentacion(presentacion.get())
                fila.setSerieLote(serieLote.get())
                fila.setDiasEntrada(diasEntrada.get())
                fila.setArticulo(articulo.get())
                fila.setMayoreo(mayoreo.get())
                fila.setTransito(transito.get())
                fila.setCosteo(costeo.get())
                fila.setGdl(gdl.get())
                fila.setMex(mex.get())
                fila.setMxl(mxl.get())
                fila.setEstatus(estatus.get())
                actualizarTreeView()
                limpiarVariables()
            else:
                messagebox.showwarning(
                    "Advertencia", 
                    "No se puede Actualizar un registro sin antes seleccionarlo\n\nSeleccione algun registro de la tabla y vuelva a intentar"
                )
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Error al Actualizar ListaPrecios: No se puede Modificar un registro sin antes seleccionarlo')

        def enviarWhatsApp():
            if(contacto.get() != '' and self._listaPrecios.getElementos()):
                self._mensaje.setMensaje(self._listaPrecios.mensaje())
                self._mensaje.setContacto(contacto.get())
                if(not self._mensaje.getIsOpen()):
                    self._mensaje.openWhatssApp()
                    if(messagebox.askquestion('Validacion QR', '¿Logro Iniciar Sesion en WhatsApp?', icon='question') == 'yes'):
                        self._mensaje.enviarMensajeWp()
                    else: 
                        self._mensaje.delete()
                else:
                    self._mensaje.enviarMensajeWp()
            elif(contacto.get() == ''):
                messagebox.showwarning(
                    "Advertencia", 
                    "No se puede Enviar el Mensaje por WhatsApp sin un destinatario\n\nIngrese el Nombre de Algun Contacto o Grupo y vuelva a Intentar."
                )
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Error al Enviar WhatsApp: No se puede Enviar el Mensaje por WhatsApp sin un destinatario')
            else:
                messagebox.showwarning(
                    "Advertencia", 
                    "No se puede Enviar el Mensaje por WhatsApp sin Datos\n\nCargue un Archivo de Excel con la información y vuelva a Intentar."
                )
                print(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Error al Enviar WhatsApp: No se puede Enviar el Mensaje por WhatsApp sin Datos')


        def cerrarSesion():
            self._mensaje.cerrarSesion()


        #---------------------------------------------------------------Definicion de Propiedades visuales dentro de la Pestaña
        #---------------------------------------------------------------Logo de la Ventana
        logor = Image.open('img/logo.png')
        logor = logor.resize((150,55), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logor)
        labelImg = ttk.Label(superiorFrame, image=logo)
        labelImg.image = logo
        labelImg.grid(row=0, column=0, pady=10, sticky=tk.W)
        #---------------------------------------------------------------Boton Switch para Cambiar Tema
        switchTema = ttk.Checkbutton(superiorFrame, text=self._tema, style='Switch', command=cambiarTema)
        switchTema.grid(row=0, column=4, sticky=tk.E)
        #---------------------------------------------------------------Label y Entrada Contacto
        labelContacto = ttk.LabelFrame(superiorFrame, text='Contacto')
        labelContacto.grid(row=1, column=0, sticky=tk.W)

        entradaContacto = ttk.Entry(labelContacto, width=30, textvariable=contacto)
        entradaContacto.grid(row=0, column=0, sticky=tk.W)
        #---------------------------------------------------------------Boton Cargar Excel
        botonCargarArchivo = ttk.Button(superiorFrame, text='Cargar Excel', command=cargarExcel)
        botonCargarArchivo.grid(row=1, column=2, sticky=tk.W)
        #---------------------------------------------------------------Boton Enviar WhatsApp
        botonEnviarWP = ttk.Button(superiorFrame, text='Enviar WhatsApp', command=enviarWhatsApp)
        botonEnviarWP.grid(row=1, column=3, sticky=tk.E)
        #---------------------------------------------------------------Boton Cerrar Sesion
        botonCerrarSesion = ttk.Button(superiorFrame, text='Cerrar Sesion WhatsApp', command=cerrarSesion)
        botonCerrarSesion.grid(row=1, column=4, sticky=tk.E)
        #---------------------------------------------------------------Label y Entrada Global
        labelGlobal = ttk.LabelFrame(intraFrame, text='Editar')
        labelGlobal.grid(row=0, column=0, sticky=tk.W)

        entradaGlobal = ttk.Entry(labelGlobal, width=170, textvariable=general)
        entradaGlobal.grid(row=0, column=0, sticky=tk.W)
        #---------------------------------------------------------------Boton Actualizar
        botonActualizar = ttk.Button(intraFrame, text='>', command=enter)
        botonActualizar.grid(row=0, column=1, sticky=tk.E)
        #---------------------------------------------------------------Scrollbar
        treeScroll = ttk.Scrollbar(inferiorFrame)
        treeScroll.pack(side="right", fill="y")
        #---------------------------------------------------------------TableApp para visualizar registros dentro de la sesion
        treeView = ttk.Treeview(inferiorFrame, selectmode='extended', yscrollcommand=treeScroll.set)
        treeScroll.config(command=treeView.yview)
        treeView['columns'] = (
            'ESPECIE', 'VARIEDAD', 'ETIQUETA', 
            'CALIDAD', 'CALIBRE', 'EMPAQUE', 
            'PRESENTACION', 'SERIE LOTE', 
            'DIAS ENTRADA', 'ARTICULO', 'MAYOREO', 
            'MENUDEO', 'TRANSITO', 'COSTEO', 'GDL', 
            'MEX', 'MXL', 'ESTATUS'
        )
        columnWidth = [100, 90, 90, 80, 80, 80, 90, 90, 100, 70, 80, 60, 60, 70, 50, 50, 50, 70]
        treeView.column("#0", width=0,  stretch=tk.NO)
        treeView.heading("#0",text="",anchor=tk.CENTER)

        for heading in treeView['columns']:
            treeView.column(heading, anchor=tk.CENTER, width=columnWidth[treeView['columns'].index(heading)])
            treeView.heading(heading, text=heading, anchor=tk.CENTER)

        actualizarTreeView()

        cambiarFuente(treeView, 8)

        treeView.bind('<Control-c>', copyToClipBoard)  # Asociar evento Ctrl+C a la función
        treeView.bind('<<TreeviewSelect>>', seleccionarItem)
        treeView.bind('<Button-1>', onClic)
        treeView.bind('<Double-1>', dobleClic)
        treeView.pack(fill='both', expand=True)


    #---------------------------------------------------------------Funcion para Actualizar la Barra de estado
    def actualizarBarraEstado(self, mensaje):
        self.barraEstado.set(mensaje)


    #---------------------------------------------------------------Funcion para configurar Frames y Canvas dentro de Notebook
    def principalTabs(self):
        #---------------------------------------------------------------Declaración de Frame contenedor base del Tab Clientes
        tabListaPrecios = ttk.Frame(self._notebook)
        tabListaPrecios.columnconfigure(index=0, weight=1)
        tabListaPrecios.rowconfigure(index=0, weight=2)
        tabListaPrecios.rowconfigure(index=1, weight=1)
        tabListaPrecios.rowconfigure(index=2, weight=20)
        self._notebook.add(tabListaPrecios, text='Lista de Precios')
        #---------------------------------------------------------------Llamada a funciones constructoras de componentes para cada Frame en Notebook
        self.comListaPrecios(tabListaPrecios)


    def salir(self):
        if tk.messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            #----------------------------------------------------------Hacer cualquier tarea de limpieza o cierre necesaria aquí
            if(self._mensaje.getIsOpen()):
                self._mensaje.cerrarSesion()
            sys.stdout = self.original_stdout
            # Abrir el archivo origen en modo lectura
            with open('Temp.txt', 'r') as origen:
                # Leer el contenido del archivo origen
                contenido_origen = origen.read()

            # Abrir el archivo destino en modo anexar
            with open('Log.txt', 'a') as destino:
                # Escribir el contenido del archivo origen en el archivo destino
                destino.write(contenido_origen)
                destino.write(f'\n{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} || Finaliza Ejecucion de Programa\n')
            self.destroy()


if __name__ == '__main__':
    ventana = Ventana()
    ventana.mainloop()