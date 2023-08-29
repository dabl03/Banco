import colorama;
from colorama import Fore as c_fore;
from colorama import Style as c_style;
from resource import *;
import os;
import re;
import sys;
import hashlib;
class Person():
    def __init__(self,CI,password,name='',last_name='',monto='0'):
        self.CI=Person.verify_ci(CI);
        self.password=encode_str(self.CI,password);
        self.name=name.capitalize();
        self.last_name=last_name.capitalize();
        self.monto=Person.verify_ci(Person.get_money(monto));#Para asegurarnos que no tenga letras solo numeros y su separador correspondiente.
    def verify_ci(CI):
        """No pases la cedula con puntos o abra error."""
        if type(CI)==int: CI=str(CI);
        elif type(CI)==float: CI=str(int(CI));
        elif type(CI)!=str:
            print(f"Interno de app en la funcion verify_ci({CI}).\nPorfavor contactar con el desarrollador.");
            exit(-3);
        CI=CI[::-1].replace('.','');
        #Primero quitamos los numeros negativos.
        negative='';
        if CI[-1]=='-':
            negative='-';
            CI=CI.replace('-','');
        unidad=0;
        l=len(CI);
        out="";
        for i in range(l):
            #Si es igual a 3 se coloca punto para: 1.000bs
            if unidad==3 and i!=l:
                out+='.';
                unidad=0;
            out+=CI[i];
            unidad+=1;
        return negative+out[::-1];
    def get_money(money):
        #Si no consigue numero entonces retorna '0'
        out='';
        negative='-' if money[0]=='-' else '';
        for c in money:
            if not c.isdigit():
                continue;
            out+=c;
        return int(negative+out) if out!='' else 0;
    def get_user_c(l_str):
        return Person(l_str[2],l_str[6],l_str[0],l_str[1],l_str[4]);
    def get_FIuser(user):
        """Aqui buscamos el usuario.
Si el archivo esta vacio se retorna None.
Si se consigue el usuario retorna {"file":str,"location":int ubicacion del usuario en "file":str}
Sino retorna lo mismo al anterior pero "location" se establece en None.
Si la contraseña no coincide retorna lo mismo pero ahora "location" vale Person.INVALID_PASSWORD=-1."""
        str_f=Dir.get_str_client();
        if str_f==None: return None;
        location=None;
        for i in range(len(str_f)):
            st=get_str_ncomment(str_f[i]);
            if st=='' or st=='\n': continue;
            st=st.split();
            if len(st)<7 or user.CI!=Person.verify_ci(st[2]): continue;#No es el usuario o falta parametro.
            if user.password!=st[6]:
                location=Dir.INVALID_PASSWORD;
                break;
            location=i;
        return {"file":str_f,"location":location};
    def get_TDC(user):
        location=[];
        if not os.path.exists(Dir.ALL["TDC"]): return None;
        str_f=[];
        coincidence=0;
        with open(Dir.ALL["TDC"],'r') as f: str_f=f.readlines();
        if len(str_f)==0 or str_f[0]=='': return None;
        for i in range(len(str_f)):
            st=str_f[i].split();
            if len(st)<3 or Person.verify_ci(st[0])!=user.CI: continue;
            location.append(i);
        return {"file":str_f,"location":location if len(location)!=0 else None};
def open_account(user):
    """Abre una cuenta y almacena el deposito.
    Retorna True si se abrio la cuenta, sino False, puede retornar Dir.INVALID_PASSWORD si la contraseña es invalida.
    """
    #Client.txt: [NOMBRE] [APELLIDO]    [CI]    [ESTADO_DE_CUENTA]    [MONTO_DISPONIBLE]    [MONTO_DEUDOR]    [CONTRASEÑA]#Opcional: Comentarios.
    money=Person.get_money(user.monto);
    active=1;
    is_open=True;
    #Abrimos la cuenta.
    str_f=Person.get_FIuser(user);
    # #Existe el registro hay que buscar al usuario sino esta se crea, si esta se comprueba y se ve si se abre o no.
    if str_f!=None:
        i=str_f["location"];
        if str_f["location"]==Dir.INVALID_PASSWORD:
            print(c_fore.RED+"**Usuario ya existe**"+c_style.RESET_ALL);
            print("No se ha podido depositar ni crear cuenta por:");
            return Dir.INVALID_PASSWORD;
        elif str_f["location"]==None:
            #No se existe por lo que se crea.
            debe=0;
            active=0 if money<MIN_MONEY else 1;
            if money<MIN_MONEY:
                debe=0;
                print(f"{c_fore.RED}ERROR:{c_style.RESET_ALL} Monto insuficiente para abrir cuenta.\nAlmacenaremos la cantidad para que no se pierda.\nPero con cuenta inactiva ir al banco para retirar.");
                is_open=False;
            money=Person.verify_ci(money);
            str_f["file"].append(f"\n    {user.name} {user.last_name}    {user.CI}    {active}    {money}    {debe}    {user.password}");
        else:
            #El usuario existe.
            st=str_f["file"][i].split();
            m=Person.get_money(st[4])+money;#Nuevo monto.
            st[4]=Person.verify_ci(m);
                #Conseguimos al usuario:)
            if st[3]=='0':
                #Vemos si ha depositado lo suficiente para activar la cuenta.
                if m<0:
                    #Todavia debe.
                    debe=Person.get_money(st[5])-money;
                    st[5]=Person.verify_ci(debe);
                    print(f"{c_fore.RED}Error:{c_style.RESET_ALL} Todavia no es suficiente para abrir cuenta. \nMonto: {c_fore.GREEN}{money}{c_style.RESET_ALL}\nDebe: {c_fore.RED}{st[5]}{c_style.RESET_ALL}");
                    is_open=False;
                else:
                    if not m<MIN_MONEY:
                        #Cuenta ya activada.
                        st[3]='1';
                        st[5]=0;
                        print("Se ha activado la cuenta.");
                    else:
                        print(f"Todavia no se ha podido activar cuenta.\nMonto minimo: {Person.verify_ci(MIN_MONEY)}\nMonto actual: {Person.verify_ci(m)}");
                        is_open=False;
            else:
                print(f"{c_fore.GREEN}Error:{c_style.RESET_ALL} Cuenta ya existe y ya activa.\nSe almacenara el monto.");
                is_open=False;
                m_d=Person.get_money(st[5])-money;
                st[5]=Person.verify_ci(m_d) if m_d>=0 else '0';
            #No usamos el nuevo o st porque este no tiene comentarios.
            str_f["file"][i]=str_f["file"][i].split();
            str_f["file"][i][3]=st[3];#Activamos la cuenta.
            str_f["file"][i][4]=st[4];#Guardamos el monto.
            str_f["file"][i][5]=st[5];#Guardamos cuanto debe.
            active=int(st[5]);
            #Concatenamos todo.
            out=f"    {st[0]} {st[1]}";
            for x in range(2,len(str_f["file"][i])):
                out+="    "+str(str_f["file"][i][x]);
            str_f["file"][i]=out;
        str_f=str_f["file"];
    else:
        #No existe registro previo sobre ningun asi que se crea
        str_f=[
            "#Comentario generado por app.\n",
            "#Las informacion se almacenara de esta forma en el archivo:\n",
            "#[NOMBRE] [APELLIDO]    [CI]    [ESTADO_DE_CUENTA]    [MONTO_DISPONIBLE]    [MONTO_DEUDOR]    [CONTRASEÑA]#Opcional: Comentarios.\n",
            "#Ejemplo:\n",
            "#Jhon Doe    30.212.321    1    500.000    100.000    is_digit__#Ejemplo de un usuario.\n"
        ];
        if money<MIN_MONEY:
            print(f"{c_fore.RED}ERROR:{c_style.RESET_ALL} No es suficiente para abrir cuenta.\nAlmacenaremos la cantidad para que no se pierda.\nPero con cuenta inactiva ir al banco para retirar.");
            active=0;
            is_open=False;
        money=Person.verify_ci(money);
        str_f.append(f"\n    {user.name} {user.last_name}    {user.CI}    {active}    {money}    0    {user.password}");
    #Para guardar lo que ya tenia y lo modificado si hay.
    with open(Dir.ALL["CLIENT"],'w') as f:
        f.writelines(str_f);
    #Almacenamos el deposito.
    str_f="    Cedula:    Monto:\n" if not os.path.exists(Dir.ALL["DEPOSITO"]) else '';
    with open(Dir.ALL["DEPOSITO"],'a') as f:
        f.write(f"{str_f}    {user.CI}    {user.monto}\n");
    return is_open;
def reembozo(name,last_name,CI,monto):
    print(f"Usuario: {c_fore.YELLOW}{name} {last_name}{c_style.RESET_ALL}. CI: {c_fore.YELLOW}{CI}{c_style.RESET_ALL}\nSe le entrega monto por {c_fore.GREEN}{Person.verify_ci(monto)}{c_style.RESET_ALL}.");
    msg="    CI:    MONTO:" if not os.path.exists(Dir.ALL["RETIRO"]) else '';
    with open(Dir.ALL["RETIRO"],'a') as f:
        f.write(f"{msg}\n    {CI}    {monto}");
def close_account(user):
    #client.txt: [NOMBRE] [APELLIDO]    [CI]    [ESTADO_DE_CUENTA]    [MONTO_DISPONIBLE]    [MONTO_DEUDOR]    [CONTRASEÑA]
    #Retorna None si el usuario no existe, Dir.INVALID_PASSWORD si la contraseña no es valida, retorna True si funciono, sino False.
    #Validamos.
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    i=user_f["location"];
    st=get_str_ncomment( user_f["file"][i] ).split();
    #Almacenamos los datos.
    user.name=st[0];
    user.last_name=st[1];
    money=Person.get_money(st[4]);
    if money<0:
        print(f"No se puede eliminar cuenta porque todavia no se ha pagado lo que debe.\nPara cerrar cuenta tienes que pagar: {c_fore.RED}{Person.verify_ci(st[5])}{c_style.RESET_ALL}");
        return False;
    del user_f["file"][i];#Quitamos el usuario.
    #Almacenamos.
    with open(Dir.ALL["CLIENT"],'w') as f:
        f.writelines(user_f["file"]);
    reembozo(user.name,user.last_name,user.CI,money);
    msg="    CI:    Nombre y Apellido:\n" if not os.path.exists(Dir.ALL["CUENTA_CERRADA"]) else '';
    #Deposito.
    with open(Dir.ALL["CUENTA_CERRADA"],'a') as f:
        f.write(f"{msg}    {user.CI}    {user.name} {user.last_name}\n");
    #Si existe tarjeta la eliminamos.
    if os.path.exists(Dir.ALL["TDC"]):
        tdc_f=[];
        change=True;
        with open(Dir.ALL["TDC"],'r') as f: tdc_f=f.readlines();
        #Eliminamos todas las tarjetas.
        while change:
            change=False;
            for i in range(len(tdc_f)):
                st=tdc_f[i].split();
                if len(st)<3 or Person.verify_ci(st[0])!=user.CI: continue;
                del tdc_f[i];
                change=True;
                break;
        with open(Dir.ALL["TDC"],'w') as f: f.writelines(tdc_f);
        print("Se ha eliminado la tarjeta afiliadas.")
    return True;
def request_card(user, type_card):
    #solicitudesTDC.txt: [CI] [TIPO_TARJETA] [APPROVED]
    #Retorna None si el usuario no existe, Dir.INVALID_PASSWORD si la contraseña no es valida, retorna True si funciono, sino False.
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    type_card=type_card.capitalize();
    if not type_card in ["Visa","Mastercard"]:
        print(f"Tarjeta {c_fore.RED}\"{type_card}\"{c_style.RESET_ALL} no valida.");
        return False;
    i=user_f["location"];
    st=get_str_ncomment( user_f["file"][i] ).split();
    if st[3]=='0':
        print("La cuenta no esta activa para solicitar TDC.");
        return False;
    del user_f;
    money=Person.get_money(st[4]);
    approved=True;
    #Verificamos si existe la tarjeta.
    if os.path.exists(Dir.ALL["TDC"]):
        str_f=[];
        with open(Dir.ALL["TDC"],'r') as f: str_f=f.readlines();
        for i in range(len(str_f)):
            st=str_f[i].split();
            if len(st)<3 or Person.verify_ci(st[0])!=user.CI: continue;
            if type_card==st[1]:
                print(f"{c_fore.RED}Error:{c_style.RESET_ALL} Tarjeta ya existe.");
                return False;
    if money<MIN_MONEY_FTDC:
        print(f"No tienes suficiente dinero para solicitar TDC.\nMonto minimo: {Person.verify_ci(MIN_MONEY_FTDC)}\nMonto actual: {Person.verify_ci(money)}");
        approved=False;
    approved_str="SI" if approved else "NO";
    if not os.path.exists(Dir.ALL["SOLICITUDES"]):
        with open(Dir.ALL["SOLICITUDES"],'w') as f: f.write(f"    CI:    TIPO DE TARJETA:    APROVADO:\n    {user.CI}    {type_card}    {approved_str}\n");
    else:
        str_f=[];
        change=False;
        with open(Dir.ALL["SOLICITUDES"],'r') as f: str_f=f.readlines();
        for i in range(len(str_f)):
            st=str_f[i].split();
            if len(st)<3 or Person.verify_ci(st[0])!=user.CI: continue;
            if type_card!=st[1]: continue;
            str_f[i]=f"    {st[0]}    {st[1]}    {approved_str}\n";
            change=True;
            break;
        if not change: str_f.append(f"    {user.CI}    {type_card}    {approved_str}\n");
        with open(Dir.ALL["SOLICITUDES"],'w') as f: f.writelines(str_f);
    return approved;
def card_assignment(user):
    #TDC.txt: [CI] [TIPO_TARJETA] [MONTO_DISPONIBLE]
    #Verificamos sobre los datos pasados:
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    #Como ya no necesitamos mas el registro de usuario, lo eliminamos.
    st_user=get_str_ncomment( user_f["file"][ user_f["location"] ] ).split();
    del user_f;
    asigne=False;
    type_card=[];
    if not os.path.exists(Dir.ALL["SOLICITUDES"]):
        print("No se ha solicitado una tarjeta.");
        return False;
    str_f="";
    with open(Dir.ALL["SOLICITUDES"],'r') as f: str_f=f.readlines();
    change=True;
    #Verificamos si hay algunas solicitudes
    while change:
        change=False;
        for i in range(len(str_f)):
            st=str_f[i].split();
            if len(st)<3 or Person.verify_ci(st[0])!=user.CI: continue;
            if st[2].lower()=="si":
                type_card.append(st[1].capitalize());
                asigne=True;
                del str_f[i];
                change=True;
                break;
            elif st[2].lower()=="no":
                print("Tarjeta no aprovada.");
                del str_f[i];
                change=True;
                break;
    #Actualizamos el archivo solicitudes.
    with open(Dir.ALL["SOLICITUDES"],'w') as f: f.writelines(str_f);
    str_f=[];
    #Guardamos los cambios si es aprovada la tarjeta.
    if not asigne: return False;
    monto=Person.get_money(st_user[4]);
    monto=MAX_MONEY_TDC if monto>=MAX_MONEY_TDC else monto;
    out='';
    if not os.path.exists(Dir.ALL["TDC"]):
        str_f=[
            "    CI:    Tipo de tarjeta:    Monto diponible:\n"
        ];
        for i in range(len(type_card)):
            out+=f"    {user.CI}    {type_card[i]}    {monto}\n";
    else:
        with open(Dir.ALL["TDC"],'r') as f: str_f=f.readlines();
        for i in range(len(str_f)):
            st=str_f[i].split();
            if len(st)<3 or st[0]!=user.CI: continue;
            if st[1].capitalize() in type_card:
                print("Tarjeta \""+st[1].capitalize()+"\" ya existe.");
                for i in range(len(type_card)):
                    if type_card[i]==st[1].capitalize():
                        del type_card[i];
                        break;
                continue;
        for i in range(len(type_card)):
            out+=f"    {user.CI}    {type_card[i]}    {monto}\n";
    str_f.append(out);
    with open(Dir.ALL["TDC"],'w') as f: f.writelines(str_f);
    return asigne;
def deposit(user):
    #depositos.txt: [CI] [MONTO]
    #Verificamos sobre los datos pasados:
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    #Se intenta depositar un numero negativo.
    if Person.get_money(user.monto)<0: return False;
    i=user_f["location"];
    st_user=user_f["file"][i].split();
    monto=Person.get_money(user.monto)+Person.get_money(st_user[4]);
    debe=Person.get_money(st_user[5])-Person.get_money(user.monto);
    #Ya no se debe.
    if monto>0:
        debe=0;
        if st_user[3]=='0' and monto>=MIN_MONEY:
            st_user[3]='1';
            print("Se ha activado la cuenta");
    st_user[4]=Person.verify_ci(monto);
    st_user[5]=Person.verify_ci(debe);
    end_line='' if len(user_f["file"])-1==i or user_f["file"][i+1]=='\n' else '\n';
    user_f["file"][i]=f"    {st_user[0]} {st_user[1]}    {st_user[2]}    {st_user[3]}    {st_user[4]}    {st_user[5]}    {st_user[6]}{end_line}";
    with open(Dir.ALL["CLIENT"],'w') as f: f.writelines(user_f["file"]);
    #Guardamos el registro:
    user_f="    CI:    Monto:" if not os.path.exists(Dir.ALL["DEPOSITO"]) else '';
    with open(Dir.ALL["DEPOSITO"],'a') as f: f.write(user_f+f"\n    {user.CI}    {user.monto}");
    return True;
def withdrawal(user):
    #retiros.txt: [CI] [MONTO]
    #Verificamos sobre los datos pasados:
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    #Se intenta depositar un numero negativo.
    if Person.get_money(user.monto)<0: return False;
    i=user_f["location"];
    st_user=user_f["file"][i].split();
    if st_user[3]=='0':
        print("Cuenta desactivada.")
        return False;
    #Hacemos los calculos:
    user_monto=Person.get_money(st_user[4]);
    monto=user_monto-Person.get_money(user.monto);
    debe=Person.get_money(st_user[5])+Person.get_money(user.monto);
    #Pide mas de lo que deberia
    if monto<(-MAX_MONEY_RETIRE):
        print(f"No se puede deber mas de {c_fore.YELLOW}{Person.verify_ci(MAX_MONEY_RETIRE)}{c_style.RESET_ALL}\nMonto solicitado: {c_fore.YELLOW}{Person.verify_ci(user.monto)}{c_style.RESET_ALL}\nMonto disponible: {c_fore.BLUE}{Person.verify_ci(st_user[4])}{c_style.RESET_ALL}\n"
        +f"Despues de retiro: {c_fore.RED}{Person.verify_ci(monto)}{c_style.RESET_ALL}");
        return False;
    #Ahora se debe.
    if monto<0:
        st_user[5]=Person.verify_ci(debe);
        if debe==MAX_MONEY_RETIRE and st_user[3]=='1':
            st_user[3]='0';
            print("Has alcanzado el limite de deuda.\nSe ha desactivado la cuenta");
        elif st_user[3]=='0':
            print("Cuenta desactivada no se puede retirar.");
            return False;
    st_user[4]=Person.verify_ci(monto);
    end_line='' if len(user_f["file"])-1==i or user_f["file"][i+1]=='\n' else '\n';
    #Guardamos el usuario:
    user_f["file"][i]=f"    {st_user[0]} {st_user[1]}    {st_user[2]}    {st_user[3]}    {st_user[4]}    {st_user[5]}    {st_user[6]}{end_line}";
    with open(Dir.ALL["CLIENT"],'w') as f: f.writelines(user_f["file"]);
    #Guardamos el registro:
    user_f="    CI:    Monto:" if not os.path.exists(Dir.ALL["RETIRO"]) else '';
    with open(Dir.ALL["RETIRO"],'a') as f: f.write(user_f+f"\n    {user.CI}    {user.monto}");
    return True;
def consult(user):
    ##Consulta los datos del usuario y retorna un resumen con esos datos.
    #Verificamos sobre los datos pasados:
    user_f=Person.get_FIuser(user);
    if user_f==None or user_f["location"]==None: return None;
    if user_f["location"]==Dir.INVALID_PASSWORD: return Dir.INVALID_PASSWORD;
    TDC=Person.get_TDC(user);
    user_f=user_f["file"][user_f["location"]].split();
    out=[
        [('-'*MAX_WIDTH)+'\n'],
        [str_center(NAME_BANK,MAX_WIDTH,'|','|')+'\n'],
        [('-'*MAX_WIDTH)+'\n'],
        ["Nombre del cliente:",user_f[0]+' '+user_f[1]],
        ["Cedula del cliente:",Person.verify_ci(user_f[2])],
        [('-'*MAX_WIDTH)+'\n'],
        ["Monto Disponible:", Person.verify_ci(user_f[4])+"Bs"],
        ["Deudas:",Person.verify_ci(user_f[5])+"Bs"]
    ];
    if TDC!=None and TDC["location"]!=None:
        out.append(
            ["TDC:","Monto Asignados:"]
        );
        for i in TDC["location"]:
            t=TDC["file"][i].split();
            out.append(
                [t[1].capitalize(),Person.verify_ci(t[2])+'Bs']
            );
    out.append(['-'*MAX_WIDTH]);
    out=get_snamevalue_center(out,MAX_WIDTH);
    return out;
def report_general():
    #clientes.txt: [NOMBRE] [APELLIDO]    [CI]    [ESTADO_DE_CUENTA]    [MONTO_DISPONIBLE]    [MONTO_DEUDOR]    [CONTRASEÑA]
    #TDC.txt: [CI] [Tipo de tarjeta] [Monto diponible]
    cuentas_activas=0;
    cuentas_inactivas=0;
    monto=0;
    debe=0;
    cant_tdc=0;
    monto_tdc_t=0;
    #Vemos si hay usuario, sino se deja todo en 0.
    users=Dir.get_str_client();
    if users==None: users=[];
    for i in users:
        if i=='' or i=='\n': continue;
        st=get_str_ncomment(i).split();
        if len(st)<7: continue;
        if st[3]=='0': cuentas_inactivas+=1;
        else: cuentas_activas+=1;
        monto+=Person.get_money(st[4]);
        debe+=Person.get_money(st[5]);
    f_tdc=[];
    if os.path.exists(Dir.ALL["TDC"]) and len(users)!=0:
        with open(Dir.ALL["TDC"],'r') as f: f_tdc=f.readlines();
    for i in f_tdc:
        if i=='' or i=='\n': continue;
        st=get_str_ncomment(i).split();
        if len(st)<3: continue;
        cant_tdc+=1;
        monto_tdc_t+=Person.get_money(st[2]);
    out=[
        [str_center("Reporte General del Banco \""+NAME_BANK+"\"",MAX_WIDTH)+'\n'],
        [('-'*MAX_WIDTH)+'\n'],
        [str_center("Resumen de cuentas:\n",MAX_WIDTH)+'\n'],
        ["Cantidad Cuentas Activas:",Person.verify_ci(cuentas_activas)],
        ["Cantidad Cuentas Inactivas:",Person.verify_ci(cuentas_inactivas)],
        ["Total Monto Disponible:",Person.verify_ci(monto)+"Bs"],
        ["Total Monto Deudas:",Person.verify_ci(debe)+"Bs"],
        [str_center("Resumen Tarjetas:\n",MAX_WIDTH)+'\n'],
        ["Cantidad de TDC Asignadas:",Person.verify_ci(cant_tdc)],
        ["Total Monto Asignado:",Person.verify_ci(monto_tdc_t)+'Bs']
    ];
    return get_snamevalue_center(out,MAX_WIDTH);
def err_print(msg,*all):
    print(f"{c_fore.RED}Error:{c_style.RESET_ALL} "+color_command_block(msg),*all);
    exit(-1);
def perr_param(len_,min,name, msg):
    if len_<min: err_print(f"Argumentos insuficientes para {msg}.\nVer {Mode.PROGRAM_NAME} --help {name} para mas informacion.");
def run(param):
    p=param["mode"];
    param=param["param"];
    NONE=-2;
    len_=len(param);
    Dir.verify_dir();
    r=NONE;#Nada.
    ci='';
    out="";
    if p==Mode.OPEN:
        #[NOMBRE] [APELLIDO] [CEDULA] [CONTRASENA] [SALDO_INICIAL]
        perr_param(len_,5,"--abrir-cuenta","abrir cuenta");
        r=open_account(
            Person(param[2],param[3],param[0],param[1],param[4])
        );
        ci=Person.verify_ci(param[3]);
        if type(r)==bool:
            out="**Cuenta creada**" if r else "**Cuenta no creada**";
    elif p==Mode.CLOSE:
        #[CI] [PASSWORD]
        perr_param(len_,2,"--cerrar-cuenta","cerrar cuenta");
        r=close_account( Person(param[0],param[1]) );
        ci=Person.verify_ci(param[0]);
        if type(r)==bool:
            out="**Se elimino la cuenta**" if r else "**No se elimino la cuenta**";
    elif p==Mode.REQUEST_CARD:
        #[CI] [PASSWORD] [TIPO_TARJETA]
        perr_param(len_,3,"--solicitar-tdc","solicitar tdc");
        r=request_card(Person(param[0], param[1]),param[2]);
        ci=Person.verify_ci(param[0]);
        if type(r)==bool:
            out="**Se ha solicitado TDC**" if r else "**No se ha podido solicitar tdc**";
    elif p==Mode.CARD_ASSIGNMENT:
        #[CEDULA] [CONTRASEÑA]
        perr_param(len_,2,"--asignacion-tdc","asignar tdc");
        r=card_assignment(Person(param[0],param[1]));
        ci=Person.verify_ci(param[0]);
        if type(r)==bool:
            out="**Se a asignado TDC**" if r else "**No se a asignado TDC**";
    elif p==Mode.DEPOSIT:
        #[CEDULA] [CONTRASEÑA]
        perr_param(len_,3,"--deposito","depositar");
        r=deposit(Person(param[0],param[1],monto=param[2]));
        ci=Person.verify_ci(param[0]);
        if type(r)==bool:
            out=f"**Se a depositado {Person.verify_ci(param[2])}**" if r else "**No se ha podido depositar**";
    elif p==Mode.WITHDRAWAL:
        #[CEDULA] [CONTRASEÑA]
        perr_param(len_,3,"--retiro","retirar");
        r=withdrawal(Person(param[0],param[1],monto=param[2]));
        ci=Person.verify_ci(param[0]);
        if type(r)==bool:
            out=f"**Se a retirado un monto por {c_fore.YELLOW}{Person.verify_ci(param[2])}{c_style.RESET_ALL}**" if r else "**No se ha podido retirar**";
    elif p==Mode.CONSULT:
        #[CEDULA] [CONTRASEÑA]
        perr_param(len_,2,"--consulta","la consulta");
        r=consult(Person(param[0],param[1]));
        ci=Person.verify_ci(param[0]);
        if type(r)==str:
            print(r);
            return True;
    elif p==Mode.REPORT_GENERAL:
        print(report_general());
        return True;
    elif p==Mode.HELP:
        help(Mode.PROGRAM_NAME,param);
        return True;
    elif p==Mode.NULL:
        r=True;
        frase="Mensaje oculto:";
        center=int(len("\"El amor por la programación es una relacion de amor, odio y masoquismo\" -- dabl03.")/2);
        print(' '*(center-len(frase))+f"{c_fore.BLUE}{frase}{c_style.RESET_ALL}");
        print(f"{c_fore.RED}\"{c_style.RESET_ALL}{c_fore.GREEN}El amor por la programación es una relacion de amor, odio y masoquismo{c_style.RESET_ALL}{c_fore.RED}\"{c_style.RESET_ALL} -- {c_fore.BLUE}dabl03{c_style.RESET_ALL}.");
    if r==None: out=f"{c_fore.RED}**Usuario \"{ci}\"no existe**{c_style.RESET_ALL}";
    elif r==Dir.INVALID_PASSWORD: out=f"{c_fore.RED}**Contraseña invalida**{c_style.RESET_ALL}";
    elif type(r)==bool:
        #Coloreamos con el color indicado:
        out=c_fore.GREEN+out if r else c_fore.RED+out;
        out+=c_style.RESET_ALL;
    print(out);
    return r==True;
def main(argv):
    #Establecemos el nombre del programa.
    Mode.PROGRAM_NAME=sys.argv[0].split('/')[-1] if '/' in sys.argv[0] else sys.argv[0].split('\\')[-1];
    param={
        "mode":Mode.ERROR,
        "param":[]
    };
    for i in argv:
        #Verificamos que el comando pasado.
        if param["mode"]==Mode.ERROR:
            i=i.lower();
            param["mode"]=Mode.get_mode_String[i] if i in Mode.get_mode_String else Mode.ERROR;
        else:
            #Agregamos los argumentos.
            param["param"].append(i);
    if param["mode"]==Mode.ERROR:
        err_print("Parametro "+argv[1]+" no reconocido.\nPrecione --help para mas información.");
    return run(param)==False;
if __name__=="__main__":
    #Activamos el interprete o procesamos los parametros.
    colorama.init();
    if len(sys.argv)==1:
        err_print(f"No se ha pasado parametros. Ver --help para mas información.");
    main(sys.argv);
    
