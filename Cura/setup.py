import sys, os, zipfile

try:
    import cx_Freeze
    freezeVersion = map(int, cx_Freeze.version.split('.'))
    if freezeVersion[0] < 4 or freezeVersion[0] == 4 and freezeVersion[1] < 2:
            print "ERROR: Your cx-Freeze version is too old to use with Cura."
            sys.exit(1)

    sys.path.append(os.path.abspath('cura_sf'))

    # Dependencies are automatically detected, but it might need fine tuning.
    build_exe_options = {
    "silent": True,
    "packages": [
            'encodings.utf_8',
            "OpenGL", "OpenGL.arrays", "OpenGL.platform", "OpenGL.GLU",
    ], "excludes": [
            'Tkinter', 'tcl', 'cura_sf', 'fabmetheus_utilities', 'skeinforge_application', 'numpy',
    ], "include_files": [
            ('images', 'images'),
    ], "build_exe": 'freeze_build'}

    # GUI applications require a different base on Windows (the default is for a
    # console application).
    base = None
    if sys.platform == "win32":
        base = "Win32GUI"

    cx_Freeze.setup(  name = "Cura",
                    version = "RC5",
                    description = "Cura",
                    options = {"build_exe": build_exe_options},
                    executables = [cx_Freeze.Executable("cura.py", base=base)])

    m = cx_Freeze.ModuleFinder(excludes=["gui"])
    m.IncludeFile(os.path.abspath("cura.py"))
    m.IncludeFile(os.path.abspath("cura_sf/skeinforge_application/skeinforge_plugins/profile_plugins/extrusion.py"))
    m.IncludeFile(os.path.abspath("cura_sf/fabmetheus_utilities/fabmetheus_tools/interpret_plugins/stl.py"))
    m.IncludeFile(os.path.abspath("cura_sf/skeinforge_application/skeinforge_plugins/craft_plugins/export_plugins/static_plugins/gcode_small.py"))
    for name in os.listdir("cura_sf/skeinforge_application/skeinforge_plugins/craft_plugins"):
            if name.endswith('.py'):
                    m.IncludeFile(os.path.abspath("cura_sf/skeinforge_application/skeinforge_plugins/craft_plugins/" + name))
    m.ReportMissingModules()
    cwd = os.path.abspath(".")

    with zipfile.ZipFile("freeze_build/cura_sf.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for mod in m.modules:
                if mod.file != None and mod.file.startswith(cwd):
                        if mod.file[len(cwd)+1:] == "cura.py":
                                z.write(mod.file[len(cwd)+1:], "__main__.py")
                        else:
                                z.write(mod.file[len(cwd)+1:])
        z.write('cura_sf/fabmetheus_utilities/templates/layer_template.svg')
        z.write('cura_sf/fabmetheus_utilities/version.txt')
        z.write('__init__.py')
except ImportError:
    import setuptools
    from setuptools import setup

    packages = setuptools.find_packages()

    setup(name='Cura',
          version='RC5',
          packages=packages,
          scripts=['cura.py']
          )
