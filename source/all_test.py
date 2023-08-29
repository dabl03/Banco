import unittest
import query as quer;
import resource as res;
import interpreter as inter;
import os;

user_test={
    "name":"Daniel",
    "last_name":"Briceño",
    "ci":"29.820.949",
    "monto":"500.000",
    "debe":"0",
    "password":"is_digit",
    
};
user_test["password_encripter"]=res.encode_str(user_test["ci"],user_test["password"]);
open_account_text=f"""#Comentario generado por app.
#Las informacion se almacenara de esta forma en el archivo:
#[NOMBRE] [APELLIDO]    [CI]    [ESTADO_DE_CUENTA]    [MONTO_DISPONIBLE]    [MONTO_DEUDOR]    [CONTRASEÑA]#Opcional: Comentarios.
#Ejemplo:
#Jhon Doe    30.212.321    1    500.000    100.000    is_digit__#Ejemplo de un usuario.

    {user_test["name"]} {user_test["last_name"]}    {user_test["ci"]}    1    {user_test["monto"]}    {user_test["debe"]}    {user_test["password"]}
""";
def delete_all():
    if not os.path.exists(res.Dir.BASE):
        return;
    for name in res.Dir.ALL:
        if os.path.exists(res.Dir.ALL[name]):
            os.remove(res.Dir.ALL[name]);
    return;
def get_str_file(url):
    if not os.path.exists(url):
        return None;
    with open(url,'r') as f:
        return ''.join(f.readlines());
class TestUtils(unittest.TestCase):
    def test_is_prime(self):
        res.Dir.BASE="./test/query";
        self.assertEqual(quer.Person.verify_ci(1000000),"1.000.000");
        self.assertEqual(quer.Person.verify_ci("1000000"),"1.000.000");
        self.assertEqual(quer.Person.verify_ci("1.0.0.0000"),"1.000.000");
        self.assertEqual(quer.Person.get_money("1000000"),1000000);
        self.assertEqual(quer.Person.get_money("100asdasd0000"),1000000);
        #Debes verificar las ultimas funciones de Person
        #despues de realizar las operaciones de abrir cuentas.
        #self.assertEqual(quer.Person.get_user_c);
        #Verificamos las funciones de resource:{
        delete_all();##Borramos el registro para hacer el test.
        this_user=quer.Person(
            user_test["ci"],user_test["password"],
            user_test["name"],user_test["last_name"],
            user_test["monto"]
        );
        self.assertTrue(quer.open_account(this_user));
    
        self.assertTrue(get_str_file(res.Dir.ALL["CLIENT"])==open_account_text);
        #}
if __name__=="__main__":
    res.Dir.verify_dir();
    unittest.main();