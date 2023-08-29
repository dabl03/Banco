# Banco

[MIT License](./license)

## Como usar:

Se puede usar por consola, solo debes usar el archivo query.py para solo parametros, y interprete.py para parametro o interprete(depende de si le pasas parametro o no).
<pre>
	<codes>
		echo activamos la consola.
		py interprete.py
		echo usamos las opciones por parametros.
		py interprete.py --abrir-cuenta Nombre Apellido Cedula contraseña 1000000monto
	</codes>
</pre>

> Para mas informacion sobre la lista de parametro usar query.py --help
> Notas: Todos los archivos python lo conseguiras en la carpeta source.
## Dependencias:

Para el color uso <codes>colorama</codes> y para la compilación uso <codes>py2exe</codes>.
Para descargarlo recomiendo usar la utilidad <codes>pip</codes> de python.

## ¿Como compilarlo?

Para compilarlo yo uso el siguiente comando dentro de la carpeta source: <codes>py setup.py py2exe --bundle 1</codes>
> Nota: Los ejecutables se colocan en la carpeta dist no se como cambiarlo.
## Objetivo:
<p>
	Cree este programa con solucion a una tarea que me pusieron donde requeria lo siguiente(Resumi lo que dice la tarea):
	> Crear un programa para administrar cuentas bancarias de la manera mas intuitiva, ofreciendo las opciones basicas:
	<ul>
	<li>Crear cuenta.</li>
	<li>Cerrar cuenta.</li>
	<li>Depositar.</li>
	<li>Retirar.</li>
	<li>Solicitar TDC(Tarjeta de Credito).</li>
	<li>Asignar TDC.</li>
	<li>Reporte de Cuenta.</li>
	<li>Reporte General(Donde se enseña informacion basica de todas las cuentas).</li>
	</ul>
</p>
## Registros:
<p>
	Todas la informacion se almacena en la carpeta ./query/ en la ubicacion que se encuentra el programa.<br/>
	Se almacena en la carpeta archivos de texto plano para que los administradores puedan verificar todo facilmente.
</p>