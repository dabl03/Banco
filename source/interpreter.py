import colorama;
from colorama import Fore as c_fore;
from colorama import Style as c_style;
import resource as res;
from resource import Mode as m;
import query;
import sys;
class Interprete():
    MENU_OPTIONS=13;
    opcion_d={
        '0':MENU_OPTIONS,
        '1':m.OPEN,
        '2':m.CLOSE,
        '3':m.REQUEST_CARD,
        '4':m.CARD_ASSIGNMENT,
        '5':m.DEPOSIT,
        '6':m.WITHDRAWAL,
        '7':m.CONSULT,
        '8':m.REPORT_GENERAL,
        '9':m.EXIT,
        '10':m.HELP
    };
    opcion_word={
        "menu":MENU_OPTIONS,
        "abrir":m.OPEN,
        "cerrar":m.CLOSE,
        'solicitar-tdc':m.REQUEST_CARD,
        'asignar-tdc':m.CARD_ASSIGNMENT,
        'depositar':m.DEPOSIT,
        'retirar':m.WITHDRAWAL,
        'consultar':m.CONSULT,
        'greporte':m.REPORT_GENERAL,
        'quit':m.EXIT,
        "salir":m.EXIT,
        'help':m.HELP
    };
    vars_={
    };
    out_menu=[[res.str_center("Lista de opciones:",res.MAX_WIDTH)+'\n'],
        [" 0 o menu :","Esta lista"],
        [" 1 o abrir :","Apertura de Cuenta"],
        [" 2 o cerrar :","Cierre de Cuenta"],
        [" 3 o solicitar-tdc :","Solicitud de TDC"],
        [" 4 o asignar-tdc :","Asignación de TDC"],
        [" 5 o depositar :","Depósitar monto a cuenta"],
        [" 6 o retirar :","Retira un monto de la cuenta"],
        [" 7 o consultar :","Consulta de Cuenta"],
        [" 8 o greporte :","general Reporte(o greporte)"],
        [" 9 o Salir :","Para terminar de este programa"],
        ["10 o help :","Explicación detallada de esta lista"]
    ];
    out_mncolor=[[res.str_center("Lista de opciones:",res.MAX_WIDTH)+'\n'],
        [" 0 o menu :","Esta lista"],
        [" 1 o abrir :","Apertura de Cuenta"],
        [" 2 o cerrar :","Cierre de Cuenta"],
        [" 3 o solicitar-tdc :","Solicitud de TDC"],
        [" 4 o asignar-tdc :","Asignación de TDC"],
        [" 5 o depositar :","Depósitar monto a cuenta"],
        [" 6 o retirar :","Retira un monto de la cuenta"],
        [" 7 o consultar :","Consulta de Cuenta"],
        [" 8 o greporte :","general Reporte(o greporte)"],
        [" 9 o Salir :","Para terminar de este programa"],
        ["10 o help :","Explicación detallada de esta lista"]
    ];
    signos=(
        ':',
        ',',
        '.',
        '-',
        '_',
        '^',
        '@',
        '#',
        '+',
        '\\',
        '/',
        '*'
    );
    init_end_block=(
        (#Aqui se pondra los inicios.
            '[',
            '"',
            '\'',
            '{',
            '('
        ),
        (#Aqui se pondran los finales.
            ']',
            '"',
            '\'',
            '}',
            ')'
        ),
        (#Aqui los colores.
            c_fore.CYAN,
            c_fore.GREEN,
            c_fore.GREEN,
            c_fore.MAGENTA,
            c_fore.BLUE
        )
    );
    out_menu=res.get_snamevalue_center(out_menu,res.MAX_WIDTH);
    help_msg={
        MENU_OPTIONS:" 0 o menu  :  Este comando muestra un resumen de esta lista. Si se le pasa un comando de la lista da una breve descripción",
        m.OPEN:f" 1 o abrir  :  Este comando crea una nueva cuenta o activa una ya existente. Requiere que le pase [NOMBRE], [APELLIDO], [CI], [PASSWORD] y el [MONTO A DEPOSITAR]. Nota: Debe tener como minimo {query.Person.verify_ci(int(res.MIN_MONEY))}.",
        m.CLOSE:f" 2 o cerrar : Este comando elimina una cuenta y elimina todas tarjetas vinculada a ella. Requiere la [CI] y el [PASSWORD]. Nota: Si debe o entonces debera pagar para poder cerrarla.",
        m.REQUEST_CARD:f" 3 o solicitar-tdc : Este comando solicita una tarjeta. Se requiere la [CI], [PASSWORD] y [TIPO DE TDC]. Nota: Debe tener como minimo {query.Person.verify_ci(int(res.MIN_MONEY_FTDC))} para que sea aprovada la solicitud.",
        m.CARD_ASSIGNMENT:f" 4 o asignar-tdc  : Este comando asigna las tarjetas fueron previamente solicitadas. Solo requiere la [CI] y el [PASSWORD].",
        m.DEPOSIT:f" 5 o depositar  : Este comando deposita a la cuenta. Se requiere [CI], [PASSWORD] y el [MONTO A DEPOSITAR]. Si no esta activa la cuenta, lo activa si supera el monto minimo o llega al monto minimo({query.Person.verify_ci(int(res.MIN_MONEY))}).",
        m.WITHDRAWAL:f" 6 o retirar  : Este comando retira una cantidad de la cuenta. Se requiere [CI], [PASSWORD] y el [MONTO A RETIRAR]. No se puede deber mas de {query.Person.verify_ci(int(res.MAX_MONEY_RETIRE))}. Si debes esa cantidad se desactivara la cuenta.",
        m.CONSULT:" 7 o consultar  : Este comando enseña un resumen de tu cuenta. Se requiere [CI] y [PASSWORD].",
        m.REPORT_GENERAL:" 8 o Greporte  : Abreviacion de General Report(Reporte General) enseña un reporte o resumen de todas las cuentas. No se requiere parametro.",
        m.EXIT:" 9 o salir o quit  : Solo sale de esta APP.",
        m.HELP:"10 o help  : Enseña este menu de ayuda."
    };
def header():
    autor={
        "name":"Author:",
        "value":res.AUTHOR
    };
    space=' '*int((res.MAX_WIDTH-(len(autor["name"])+len(autor["value"])))-2);
    print(f"""{'-'*res.MAX_WIDTH}
{res.str_center(res.NAME_BANK,res.MAX_WIDTH,'|','|')}
{res.str_center(res.LICENSE,res.MAX_WIDTH,'|','|')}
|Author:{space}{c_fore.YELLOW}{res.AUTHOR}{c_style.RESET_ALL}|
{'-'*res.MAX_WIDTH}
    """);
def err_print(a,*all): print(f"{c_fore.RED}Error:{c_style.RESET_ALL} {a}",*all);
def colorear_str_help(str_s):
    out='';
    i=0;
    len_str=len(str_s);
    while i<len_str:
        if str_s[i].isdigit():
            #Le damos color a los numeros:
            end_number=i;
            while end_number<len_str and str_s[end_number].isdigit():
                end_number+=1;
            out+=c_fore.YELLOW+str_s[i:end_number]+c_style.RESET_ALL;
            i=end_number;
        elif str_s[i].isalpha():
            #A las palabras:
            end_word=i;
            while end_word<len_str and (str_s[end_word].isalpha() or str_s[end_word]=='-'):
                end_word+=1;
            out+=c_fore.BLUE+str_s[i:end_word]+c_style.RESET_ALL \
                if str_s[i:end_word].lower() in Interprete.opcion_word else \
                str_s[i:end_word];
            i=end_word;
        elif str_s[i] in Interprete.signos:
            #A los signos:
            out+=c_fore.RED+str_s[i]+c_style.RESET_ALL;
            i+=1;
        elif str_s[i] in Interprete.init_end_block[0]:
            #A los bloques:
            i_char=Interprete.init_end_block[0].index(str_s[i]);
            char_end=Interprete.init_end_block[1][i_char];
            end_block=i;
            end=False;
            while end_block<len_str and char_end!=str_s[end_block]:
                end_block+=1;
            end_block+=1 if end_block<len_str else 0;#Para que coloree el cierre.
            out+=Interprete.init_end_block[2][i_char]+str_s[i:end_block]+c_style.RESET_ALL;
            i=end_block;
        else:
            out+=str_s[i];
            i+=1;
    return out;
def get_io_data(names,actual=[]):
    l=len(actual);
    i=0;
    data=[];
    for name in names:
        io_open='';
        if i<l: io_open=actual[i];
        else:
            while len(io_open.split())==0:
                print(c_fore.RED+"["+c_fore.YELLOW+name+c_fore.RED+"]"+c_style.RESET_ALL+"=",end='');
                io_open=input();
        data.append(io_open);
        i+=1;
    return data;
def help(param):
    header();
    is_change=False;
    out=f"{res.str_center('Lista detallada:',res.MAX_WIDTH)}\n";
    
    if len(param)>0:
        for p in param:
            if p in Interprete.opcion_d:
                p=Interprete.opcion_d[p];
            elif p.lower() in Interprete.opcion_word:
                p=Interprete.opcion_word[p];
            else: continue;
            is_change=True;
            out+=res.limit_str(Interprete.help_msg[p],res.MAX_WIDTH,'',"\n    ")+'\n'*2;
    if not is_change:
        for name in Interprete.help_msg:
            out+=res.limit_str(Interprete.help_msg[name],res.MAX_WIDTH,'',"\n    ")+'\n';
    print(colorear_str_help(out));
def menu_option_help(param):
    is_change=False;
    out="";
    if len(param)>0:
        for i in range(len(param)):
            for h in Interprete.out_mncolor:
                if param[i].lower() in h[0] and len(h)>1:
                    out+=res.get_snamevalue_center([[h[0],h[1]]],res.MAX_WIDTH);
                    is_change=True;
                    break;
        out=colorear_str_help(out);
    if not is_change:
        out=Interprete.out_menu;
    print(out);
if __name__=="__main__":
    colorama.init();
    if len(sys.argv)>1:
        query.main(sys.argv);
        exit(0);
    end=False;
    ##user=None;#TODO: Ver si un banco guardaria su seccion.
    header();
    print(colorear_str_help(
        res.str_center("Escribe help o 10 para obtener una ayuda.",res.MAX_WIDTH)
    ));
    Interprete.out_menu=colorear_str_help(Interprete.out_menu);
    print(Interprete.out_menu);
    io_msg="> ";
    while not end:
        try:
            io=input(io_msg).split();
        except KeyboardInterrupt:
            print(c_fore.RED+"["+c_fore.YELLOW+"Ctrl-break"+c_fore.RED+"]"+c_style.RESET_ALL);
            break;
        except EOFError:
            continue;
        command=None;
        #Predeterminado solo se necesita CI y PASSWORD
        name_data=["CI","password"];
        i_ci=0;#Predeterminado la cedula es el primer argumento.
        #No hay nada.
        if len(io)==0: continue;
        #Opcion por numero.
        if io[0] in Interprete.opcion_d:
            command=Interprete.opcion_d[io[0]];
            del io[0];
        #Opcion por palabras.
        elif io[0].lower() in Interprete.opcion_word:
            command=Interprete.opcion_word[io[0].lower()];
            del io[0];
        else:
            err_print("Comando desconocido.");#No se si colocar variable o pequeña calculadora.
            continue;
        if command==Interprete.MENU_OPTIONS:
            menu_option_help(io);
            continue;
        elif command==m.OPEN:
            #Abrir cuenta. Requiere 5 parametros.
            name_data=("Nombre","Apellido","CI","Password","Monto");
            i_ci=2;
        elif command==m.CLOSE: pass;#Realmente no hay nada que cambiar.
        elif command==m.REQUEST_CARD: name_data.append("Tipo TDC");
        elif command==m.CARD_ASSIGNMENT: pass;#Tampoco hay que cambiar algo.
        elif command==m.DEPOSIT or command==m.WITHDRAWAL: name_data.append("Monto");
        elif command==m.CONSULT: pass;
        elif command==m.REPORT_GENERAL:
            print(query.report_general());
            continue;
        elif command==m.EXIT:
            break;
        elif command==m.HELP:
            help(io);
            continue;
        #Interpretamos la entrada.
        if len(io)!=len(name_data):
            try:
                io=get_io_data(name_data,io);
            except KeyboardInterrupt:
                print(c_fore.RED+"["+c_fore.YELLOW+"Ctrl-break"+c_fore.RED+"]"+c_style.RESET_ALL);
                continue;
        if not io[i_ci].replace('.','').isdigit():
            err_print("Cedula invalida.");
            continue;
        query.run({"mode":command,"param":io});
    print("Gracias por venir.");
    input("[Presione enter para salir]");