"""
    Sitio Administrador de Empresas
"""
import os
import pickle


class Empleado():
    def __init__(self, nombre, edad, salario, dinero, usuario, contraseña, empresa):
        self.nombre = nombre
        self.edad = int(edad)
        self.salario = float(salario)
        self.dinero = float(dinero)
        self.usuario = usuario
        self.contraseña = contraseña
        self.empresa = empresa
        self.tipo = 'Empleado'
        self.porcent_impuestos = 0.1

    def Trabajar(self):
        os.system('clear')
        self.dinero += self.salario
        print(f'{self.nombre} trabajó un periodo completo',
              f'y ha ganado ${self.salario} y ahora posee ${self.dinero}.\n')
        with open('empresas.data', 'wb') as file:
            pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    
    def Pagar_Impuestos(self):
        os.system('clear')
        self.dinero -= self.salario*self.porcent_impuestos
        print(f"""{self.nombre} ha pagado {self.salario*self.porcent_impuestos} en impuestos.""")
        with open('empresas.data', 'wb') as file:
            pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)
    


class Administrador(Empleado):
    def __init__(self, *args):
        super().__init__(*args)
        self.tipo = 'Administrador'
        self.porcent_impuestos = 0.2
    
    def Despedir(self):
        os.system('clear')
        print('Éstos empleados pueden ser despedidos: ')
        lst_emp = empresas_completas[self.empresa]['Lista de Empleados']
        listado = [emp.nombre for emp in lst_emp if emp.tipo != 'Jefe']
        for empleado in listado:
            print('- ', empleado)
        print('Intoduzca el nombre exacto del individuo.')
        while True:
            nombre = input('> ')
            if nombre not in listado:
                print('- Ese nombre no es válido, pruebe denuevo.')
                continue
            break
        for ind, emp in enumerate(lst_emp):
            if emp.nombre == nombre:
                del empresas_completas[self.empresa]['Lista de Empleados'][ind]
        empresas_completas[self.empresa]['Numero de Empleados'] -= 1
        with open('empresas.data', 'wb') as file:
            pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)
        print(f' - El empleado {nombre} ya no trabaja para {self.empresa}')
    
    def VerDatos(self):
        os.system('clear')
        empresa = empresas_completas[self.empresa]
        print(f"""
              Nombre de la Empresa: {self.empresa}
              Año de creación: {empresa['Año de creación']}
              Capital: ${empresa['Capital']}
              Número de empleados: {empresa['Numero de Empleados']}
              """)


class Jefe(Administrador):
    def __init__(self, *args):
        super().__init__(*args)
        self.tipo = 'Jefe'
        self.porcent_impuestos = 0.3

    def Personal(self):
        os.system('clear')
        print(f'Empleados trabajando para {self.empresa}')
        empresa = empresas_completas[self.empresa]
        for emp in empresa['Lista de Empleados']:
            print(f'<{emp.tipo}>  {emp.nombre}')

    def Contratar(self):
        os.system('clear')
        lst_empleados = empresas_completas[self.empresa]['Lista de Empleados']
        while True:
            print("""
        Elija el tipo de empleado a contratar(num):
            1.- Empleado Normal
            2.- Administrador""")
            tipo = input('> ')
            if tipo not in ['1', '2']:
                os.system('clear')
                print('> Elección Inválida, pruebe denuevo.')
                continue
            break
        nombre_emp = input('\t\nIntroduzca el nombre del empleado:')
        edad = input('\nIntroduzca la edad:')
        salario = input('\nIntroduzca su salario: ')
        dinero = input('\nIntroduzca su Dinero: ')
        usuarios = [empleado.usuario for empleado in lst_empleados]
        while True:
            usuario = input('\n\nEscriba usuario:')
            if usuario in usuarios:
                print('\t<Usuario ya seleccionado, pruebe otro>')
                continue
            break
        contraseña = input('Escriba contraseña: ')
        tipo_empleado = {'1': Empleado, '2': Administrador}
        lst_empleados.append(tipo_empleado[tipo](nombre_emp, edad, salario,
                                                 dinero, usuario, contraseña,
                                                 self.empresa))
        empresas_completas[self.empresa]['Lista de Empleados'] = lst_empleados
        empresas_completas[self.empresa]['Numero de Empleados'] += 1
        with open('empresas.data', 'wb') as file:
            pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)
        os.system('clear')
        print(f'{nombre_emp} fue contratado por {self.empresa} correctamente.')


# Configuración Inicial
try:
    os.system('clear')
    empresas_completas = pickle.load(open('empresas.data', 'rb'))
    print(' - Archivo previo encontrado, datos cargados al Administrador -')
except (FileNotFoundError, EOFError):
    print(' - Archivo previo no encontrado, el Administrador está en blanco -')
    empresas_completas = dict()


def agregar_empresa():
    # Etapa de Configuración de la empresa
    while True:
        nombre = input('Introduzca un nombre para la empresa:')
        if nombre in empresas_completas.keys():
            print('\t<Una empresa con ese nombre ya existe>')
            continue
        break
    ano_crea = int(input('Introduzca el año de creación: '))
    capital = float(input('Introduzca el capital de la empresa: '))
    n_empleados = int(input('Introduzca el número de empleados: '))

    # Etapa de registro de empleados
    tipo_empleado = {'1': Empleado,
                     '2': Administrador,
                     '3': Jefe}
    lst_empleados = list()
    add_jefe = True
    os.system('clear')
    for n in range(n_empleados):
        while True:
            print("""
        Elija el tipo de empleado a agregar(num):
            1.- Empleado Normal
            2.- Administrador""")
            if add_jefe:
                print("""\t    3.- Jefe""")
            tipo = input('> ')
            if tipo not in ['1', '2', '3']:
                os.system('clear')
                print('> Elección Inválida, pruebe denuevo.')
                continue
            if tipo == '3' and not add_jefe:
                os.system('clear')
                print('> Ya no puede agregar Jefe a la nómina.')
                continue
            elif tipo == '3' and add_jefe:
                add_jefe = False
            break
        nombre_emp = input('\t\nIntroduzca el nombre del empleado:')
        edad = input('\nIntroduzca la edad:')
        salario = input('\nIntroduzca su salario: ')
        dinero = input('\nIntroduzca su Dinero: ')
        usuarios = [empleado.usuario for empleado in lst_empleados]
        while True:
            usuario = input('\n\nEscriba usuario:')
            if usuario in usuarios:
                print('\t<Usuario ya seleccionado, pruebe otro>')
                continue
            break
        contraseña = input('Escriba contraseña: ')
        lst_empleados.append(tipo_empleado[tipo](nombre_emp, edad, salario,
                                                 dinero, usuario, contraseña,
                                                 nombre))
        os.system('clear')

    empresas_completas[nombre] = {'Año de creación': ano_crea,
                                  'Capital': capital,
                                  'Numero de Empleados': n_empleados,
                                  'Lista de Empleados': lst_empleados}

    with open('empresas.data', 'wb') as file:
        pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)
    os.system('clear')
    print(f'Empresa {nombre} agregada correctamente.')


def listar_empresas():
    os.system('clear')
    print('Listado de Empresas en el registro:')
    if not empresas_completas.keys():
        print('\tNo hay empresas registradas aún.')
        return
    for name in empresas_completas.keys():
        print(f'\n - {name}')


def eliminar_empresa():
    print('Escriba el nombre exacto de la empresa a borrar:')
    for name in empresas_completas.keys():
        print(f'\n - {name}')
    while True:
        nombre = input('> ')
        if nombre == 'q':
            return
        if nombre not in empresas_completas.keys():
            print(' - El nombre introducido no es correcto, pruebe denuevo')
            continue
        break
    del empresas_completas[nombre]
    with open('empresas.data', 'wb') as file:
        pickle.dump(empresas_completas, file, protocol=pickle.HIGHEST_PROTOCOL)    
    os.system('clear')
    print(f'La empresa {nombre} fue eliminada.')


def acceder_empresa():
    os.system('clear')
    print('Entre el nombre de la empresa a la que accederá:')
    for nombre in empresas_completas.keys():
        print(f'\n - {nombre}')
    while True:
        nombre = input('> ')
        if nombre not in empresas_completas.keys():
            print('> Empresa no encontrada, trata denuevo.')
            continue
        break
    lst_emp = empresas_completas[nombre]['Lista de Empleados']
    lst_usuarios = [emp.usuario for emp in lst_emp]
    while True:
        usuario = input('    Usuario: ')
        if usuario not in lst_usuarios:
            print('>Usuario no encontrado en base de datos de la empresa.<')
            continue
        empleado = [emp for emp in lst_emp if emp.usuario == usuario][0]
        break
    while True:
        contraseña = input('    Contraseña: ')
        if contraseña != empleado.contraseña:
            print('>Contraseña Incorrecta<')
            continue
        break
    os.system('clear')
    opciones = {'1': empleado.Trabajar, '2': empleado.Pagar_Impuestos}
    if empleado.tipo == 'Administrador' or empleado.tipo == 'Jefe':
        opciones['3'] = empleado.Despedir
        opciones['4'] = empleado.VerDatos
    if empleado.tipo == 'Jefe':
        opciones['5'] = empleado.Personal
        opciones['6'] = empleado.Contratar
    while True:
        print('\t\tOpciones:',
              '\n\t1.- Trabajar',
              '\n\t2.- Pagar Impuestos',
              '\n\t3.- Despedir Gente',
              '\n\t4.- Visualizar Datos de la Empresa',
              '\n\t5.- Mostrar Listado de Empleados'
              '\n\t6.- Contratar Gente',
              '\n\t7.- Salir')
        opcion = input('> ')
        if opcion in ['3', '4'] and empleado.tipo == 'Empleado':
            os.system('clear')
            print('<Ésta opción sólo esta disponible para Administradores y Jefes>')
            continue
        if opcion in ['5', '6'] and empleado.tipo != 'Jefe':
            os.system('clear')
            print('<Ésta opción solo esta disponible para Jefes>')
            continue
        if opcion == '7':
            os.system('clear')
            break
        opciones[opcion]()


def main_menu():
    menu_dict = {'1': agregar_empresa,
                 '2': listar_empresas,
                 '3': eliminar_empresa,
                 '4': acceder_empresa}
    while True:
        print("""
                    Administrador de Empresas
              Opciones:
                1.- Agregar una nueva Empresa
                2.- Listar Empresas registradas
                3.- Eliminar una Empresa registrada
                4.- Acceder como empleado a una Empresa
                5.- Salir del Administrador
              A continuación entre el número de su elección:
              """)
        instr = input('> ')
        if instr not in ['1', '2', '3', '4', '5']:
            os.system('clear')
            print('<<Intoduzca una opción válida>>')
            continue
        if instr == '5':
            print('Finalizando Administrador')
            break
        menu_dict[instr]()


if __name__ == '__main__':
    main_menu()
