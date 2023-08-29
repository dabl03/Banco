from distutils.core import setup
import py2exe
import resource as res;
setup(name="banco-seguro",
      version="0.1",
      author="Daniel Briceño",
      author_email=res.AUTHOR,
      license=res.LICENSE,
      copyright=res.LICENSE,
      scripts=["./interpreter.py"],
      description="Interprete del banco. Aqui se puede hacer diversas operaciones para manejar una cuenta bancaria.",
      console=[{
            "script": "./interpreter.py",
            "icon_resources": [(1, "../img/banco_seguro.ico")]
        }],
      options={"py2exe": {"bundle_files": 1}},
      zipfile=None,
      dist="../"
)