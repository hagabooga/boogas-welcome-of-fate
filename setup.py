import cx_Freeze

executables = [cx_Freeze.Executable("welcome-of-fate.py")]

cx_Freeze.setup(
    name="Booga's Welcome of Fate",
    options={"build_exe":\
             {"packages":["pygame",'random','math','time','shelve','os.path',\
                          'actions','colors','images','items',\
                          'jobs','player','potions','sounds',\
                          'utilities','weapons']}},
    executables = executables

    )
