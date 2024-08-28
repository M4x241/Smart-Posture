import pytz
from datetime import datetime
from time import sleep
import pandas as pd
# Obtener la zona horaria local de Windows


class Diagrama():

    def hora(self):
        local_timezone = pytz.timezone('America/La_Paz')  # Reemplaza 'America/Mexico_City' por tu zona horaria local
        # Obtener la fecha y hora actual en la zona horaria local
        dia = datetime.now(local_timezone)
        return dia.strftime('%H:%M:%S')



hor = Diagrama()
print(hor.hora())
print(hor.hora())


class Excel():
    col2 = [0]
    col1 = [0]
    col3 = [0]
    def h(self):
        return self.hor.hora()
    def ElementoApertura(self):
        self.col1.append(hor.hora())

    def ElementoCierre(self):
        self.col2.append(hor.hora())
        hora_inicio = datetime.strptime(self.col1[-1], "%H:%M:%S")
        hora_fin = datetime.strptime(self.col2[-1], "%H:%M:%S")
        diferencia = hora_fin - hora_inicio
        self.col3.append(diferencia.total_seconds())

    def guardarExcel(self):
        datos = pd.DataFrame(
            {
                'Columna1': self.col1,
                'Columna2': self.col2,
                'Tiempo': self.col3
            }
        )
        excel_writer = pd.ExcelWriter("reporte.xlsx")
        datos.to_excel(excel_writer, sheet_name='Hoja1', index=False)
        excel_writer._save()


## clase para el excel en tiempo real
#