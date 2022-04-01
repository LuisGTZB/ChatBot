def get_user_email(user_profile, user_number):
    if user_profile == "Empleado":
        for Empleado in Empleados:
            if Empleado['Nue'] == user_number:
                print(Empleado['Correo'])
    elif user_profile == "Alumno":
        for Alumno in Alumnos:
            print(Alumno)
            if Alumno['Nua'] == user_number:
                print(Alumno['Correo'])

if __name__ == "__main__":

    Alumnos = [{'Nombre':'Luis','Nua':345805, 'Correo': 'jl.gutierrezbecerra@ugto.mx'},{ 
    'Nombre':'Adrian', 'Nua':345807, 'Correo':'ad.lopezgarcia@ugto..x'}]

    Empleados = [{'Nombre':'Enrique','Nue':475816, 'Correo': 'ae.martinezhernandez@ugto.mx'},{
    'Nombre':'Jorge', 'Nue':475809, 'Correo': 'ja.torresmejia@ugto.mx'}]

    #print(Empleados[0]['Nombre'])
    user_profile = input("ingrese el tipo de usuario")
    User_number = int(input("ingrese el numero de usuario")) 

    print(user_profile,User_number)

    get_user_email(user_profile,User_number)


