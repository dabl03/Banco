import os;
from colorama import Fore as c_fore;
from colorama import Style as c_style;
import hashlib;
from binascii import hexlify as bin_hexlify;
LICENSE="MIT License: Copyright (c) 2023 Daniel Alexander";
AUTHOR="dabl03@outlook.com";
MIN_MONEY=100000;
MAX_MONEY_TDC=int(MIN_MONEY/1.4);
MIN_MONEY_FTDC=MIN_MONEY/3;
MAX_MONEY_RETIRE=int(MIN_MONEY/2.5);
NAME_BANK="Ahorro Seguro";
MAX_WIDTH=50;
class Mode():
    OPEN=0;
    CLOSE=1;
    REQUEST_CARD=3;
    CARD_ASSIGNMENT=9;
    DEPOSIT=4;
    WITHDRAWAL=10;
    CONSULT=11;
    REPORT_GENERAL=12;
    CONSOLE_MODE=5;
    HELP=2;
    EXIT=6;
    ERROR=7;
    NULL=8;
    PROGRAM_NAME="query.py";
    get_mode_String={
        "--abrir-cuenta":OPEN,
        "--cerrar-cuenta":CLOSE,
        "--solicitar-tdc":REQUEST_CARD,
        "--asignacion-tdc":CARD_ASSIGNMENT,
        "--deposito":DEPOSIT,
        "--retiro":WITHDRAWAL,
        "--consulta":CONSULT,
        "--reporte-general":REPORT_GENERAL,
        "--help":HELP,
        "--NULL":NULL
    };
    get_mode_help={
        "--abrir-cuenta":f"""Abre una cuenta. Se necesita pasar como parametro el nombre, apellido, cedula, contraseña y el saldo inicial.
Ejemplo de uso:
    {PROGRAM_NAME} --abrir-cuenta Jhon Doe 39.213.412 calamardo_no_es_un_pulpo 193bs.ss
    {PROGRAM_NAME} --abrir-cuenta Khan Consquitador 9123321 Ant-Man-sera_destruidoooooo 200bs.ss
    {PROGRAM_NAME} --abrir-cuenta Goku San 30.432 Peleaaa^_^ 302bs.ss
Nota: Como minimo para abrir cuenta debes depositar {MIN_MONEY}bs.ss.
""",
        "--cerrar-cuenta":f"""Cierra una cuenta. Se necesita pasar como parametro la cedula y contraseña.
Ejemplo de uso:
    {PROGRAM_NAME} --cerrar-cuenta 39.213.412 calamardo_no_es_un_pulpo
    {PROGRAM_NAME} --cerrar-cuenta 9123321 Ant-Man-sera_destruidoooooo
    {PROGRAM_NAME} --cerrar-cuenta 30.432 Peleaaa^_^
Nota: No se elimina la cuenta si el usuario no existe o debe al banco.
""",
        "--solicitar-tdc":f"""Solicita una tarjeta. Se necesita pasar como parametro la cedula, contraseña y tipo de tarjeta.
Ejemplo de uso:
    {PROGRAM_NAME} --solicitar-tdc 39.213.412 calamardo_no_es_un_pulpo Visa
    {PROGRAM_NAME} --solicitar-tdc 9123321 Ant-Man-sera_destruidoooooo Mastercard
    {PROGRAM_NAME} --solicitar-tdc 30.432 Peleaaa^_^ Mastercard
""",
        "--asignacion-tdc":f"""Asigna una tarjeta si se aprobo la solicitud. Solo se necesita [CI] [PASSWORD].
Ejemplo e uso:
    {PROGRAM_NAME} --asignacion-tdc 39.213.412 calamardo_no_es_un_pulpo
    {PROGRAM_NAME} --asignacion-tdc 9123321 Ant-Man-sera_destruidoooooo
    {PROGRAM_NAME} --asignacion-tdc 30.432 Peleaaa^_^
""",
        "--deposito":f"""Deposita una cantidad a la cuenta. Se necesita [CI] [PASSWORD] [MONTO]
Ejemplo:
    {PROGRAM_NAME} --deposito 39.213.412 calamardo_no_es_un_pulpo 20bs.ss
    {PROGRAM_NAME} --deposito 9123321 Ant-Man-sera_destruidoooooo 30bs.ss
    {PROGRAM_NAME} --deposito 30.432 Peleaaa^_^ 30bs.ss
""",
        "--retiro":f"""Retira una cantidad de la cuenta. Se necesita [CI] [PASSWORD] [MONTO]
Ejemplo:
    {PROGRAM_NAME} --retiro 39.213.412 calamardo_no_es_un_pulpo 20bs.ss
    {PROGRAM_NAME} --retiro 9123321 Ant-Man-sera_destruidoooooo 30bs.ss
    {PROGRAM_NAME} --retiro 30.432 Peleaaa^_^ 30bs.ss
""",
        "--consulta":f"""Consulta el estado de la cuenta. Se necesita [CI] [PASSWORD]
Ejemplo:
    {PROGRAM_NAME} --consulta 39.213.412 calamardo_no_es_un_pulpo
    {PROGRAM_NAME} --consulta 9123321 Ant-Man-sera_destruidoooooo
    {PROGRAM_NAME} --consulta 30.432 Peleaaa^_^""",
        "--reporte-general":"Consulta un reporte general donde se enseña un resumen de cuentas",
        "--help":"Abre el menu de ayuda o muestra ayuda de los diferentes comandos.",
        "--NULL":"No hay nada interesante no lo uses."
    };
class Dir():
    BASE="./query";
    ALL={
        "CLIENT":BASE+"/clientes.txt",
        "DEPOSITO":BASE+"/depositos.txt",
        "CUENTA_CERRADA":BASE+"/cuentasCerradas.txt",
        "SOLICITUDES":BASE+"/solicitudesTDC.txt",
        "TDC":BASE+"/TDC.txt",
        "RETIRO":BASE+"/retiros.txt"
    };
    INVALID_PASSWORD=-1;
    def verify_dir():
        """Verificamos que el directorio existe, sino lo creamos."""
        if not os.path.exists(Dir.BASE):
            os.makedirs(Dir.BASE);
    def get_str_client():
        """Retorna la cadena dentro del archivo client.
            si esta vacio retorna None.
            si no existe igual retorna None.
        """
        out=None;
        if not os.path.exists(Dir.ALL["CLIENT"]): return None;
        with open(Dir.ALL["CLIENT"],'r') as f:
            out=f.readlines();
        return out if len(out)>0 else None;
def help(name,param=None):
    DATOS="{DATOS}";#Para que format no de error.
    #No introduscas el color directo porque despues al reemplazar [] se rompera el color.
    HELP=f"""{name} [MODO] {DATOS}
{LICENSE}\nLos modos son:
    --abrir-cuenta  [NOMBRE] [APELLIDO] [CEDULA] [CONTRASENA] [SALDO_INICIAL]   : Abre una cuenta con los datos entregados
    --cerrar-cuenta [CEDULA] [CONTRASEÑA]   : Cierra una cuenta
    --solicitar-tdc  [CEDULA] [CONTRASEÑA] [TARJETA]  : Solicitud de TDC
    --asignacion-tdc [CEDULA] [CONTRASEÑA]  : Si la solicitud fue aprovada se asigna la tarjeta.
    --deposito [CEDULA] [CONTRASEÑA] [CANTIDAD]: Deposita.
    --retiro [CEDULA] [CONTRASEÑA] [CANTIDAD]: Retira.
    --consulta [CEDULA] [CONTRASEÑA]: Consulta de Cuenta
    --reporte-general [CEDULA] [CONTRASEÑA]: Reporte general.
    --modo-consola : Este comando activa el interprete de esta app.
    --help [MODO opcional]: Muestra este menu. [MODO]: Cualquiera de los comandos de este menu.
    --exit  : Sale del programa, solo disponible en modo consola.
Ejemplo:
    {name} --abrir-cuenta Jhon Doe 23.411.233 no_gato 100bs
Advertencia:
    Para evitar comportamientos inesperado solo procesamos la primera opcion y todo lo demas son Parametros, ejemplo:
    {name} --abrir-cuenta Jhon Doe 23.411.233 no_gato 100bs --help
Salida[ **Se creo la cuenta** ]. Pero no enseña el menu de ayuda.""";
    is_command=False;
    for p in param:
        if p in Mode.get_mode_help:
            print(color_block(
                color_command_block(Mode.get_mode_help[p])
            ,c_fore.GREEN,'"','"'));
            is_command=True;
    if not is_command:
        HELP=color_blocks(
            HELP,
            [
                c_fore.GREEN,
                c_fore.YELLOW
            ],
            [
                '[', #Asegurate de que este sea siempre el primero porque se rompe el coloreado si lo dejas despues.
                '{'
            ],
            [
                ']',
                '}'
            ]
        );
        print(color_command_block(HELP));
#Para colorear los comandos: --
def color_command_block(str_,color_i=c_fore.BLUE):
    s="";
    c=0;
    for i in str_:
        if i=='-':
            c+=1;
        if c>1 and (i.isalpha()==False and i!='-'):
            s+=c_style.RESET_ALL;
            c=0;
        s+=i;
    s=s.replace("--",color_i+"--");
    return s;
#Para colorear un bloque de algo. Ini=inicio del bloque, end=Final del bloque.
def color_block(str_,color,ini,end):
    s="";
    c=False;
    for i in str_:
        if i==ini and not c:
            s+=color;
            c=True;
        elif i==end:
            s+=end+c_style.RESET_ALL;
            c=False;
            continue;
        s+=i;
    return s;
#Para cuando hay mas de un bloque que colorear
def color_blocks(str_,color=[],ini=[],end=[]):
    s=str_;
    for c in range(len(color)):
        s=color_block(s,color[c],ini[c],end[c]);
    return s;
def encode_str(ci, str_):
    h = hashlib.pbkdf2_hmac('sha256', str_.encode("utf-8"), (ci.replace(".", "")[::-1]).encode("utf-8"), 100000) # Aplica 100000 iteraciones de SHA-256 a la contraseña con la sal
    return bin_hexlify(h).decode(); # Convierte el hash a hexadecimal

def compare_encode(ci, str_, encode_str_):
    return encode_str_ == encode_str(ci, str_);
def get_str_ncomment(str_):
    """Retorna una cadena sin comentario(elimina desde # hasta \n)."""
    out="";
    is_comment=False;
    for i in str_:
        if is_comment:
            if i=='\n': is_comment=False;
            continue;
        if i=='#':
            is_comment=True;
            continue;
        out+=i;
    return out;
def get_snamevalue_center(input_,MAX_WIDTH) -> str:
    """Coloca el texto ya sea normal [""] o un texto a la izquierda y su valor a la derecha ["name:","value"]
    El tamaño esta determinado por MAX_WIDTH.
    Ejemplo:
        get_snamevalue_center([["Banco:\n"],["Nombre:","Daniel"],["Comida:","Arepa"]],24);
        banco:
        Nombre:           Daniel
        Comida:            Arepa
    """
    out="";
    for i in input_:
        l=len(i);
        name=i[0];
        if l==1:
            out+=i[0];
        elif l==2:
            width_left=len(i[0]);
            width_right=len(i[1]);
            out+=i[0]+(' '*(MAX_WIDTH-(width_left+width_right)))+i[1]+'\n';
        else:
            width_left=len(i[0]);
            width_right=len(i[1]);
            out+=i[0]+(' '*(MAX_WIDTH-(width_left+width_right)))+i[1]+i[2];
    return out;
def str_center(str_,MAX_WIDTH,ini='',end='',separator=' '):
    MAX_WIDTH/=2;
    m_str=len(str_)/2;
    icenter=separator*(
        int((MAX_WIDTH-m_str)-len(ini))
    );
    ecenter=separator*(
        int((MAX_WIDTH-m_str)-len(end))
    );
    return ini+icenter+str_+ecenter+end;
def limit_str(str_,MAX_WIDTH=MAX_WIDTH,ident='',end_char='\n'):
    out="";
    if str_=="": return "";
    str_lines=str_.split('\n');
    is_change=True;
    for line in str_lines:
        str_len=len(line);
        init=0;
        end_str=0;#Necesitamos uno para la cadena.
        end_wident=len(ident);#Necesitamos tomar en cuenta el identado tambien.
        out+=('\n' if not is_change else '')+ident;
        while end_str<str_len:
            is_change=False;
            if end_wident==MAX_WIDTH:
                out+=line[init:end_str]+end_char;
                init=end_str;
                end_wident=-2+len(end_char);#Dos porque \n no cuenta.
                is_change=True;
            end_str+=1;
            end_wident+=1;
        out+=line[init:end_str];
    return out;