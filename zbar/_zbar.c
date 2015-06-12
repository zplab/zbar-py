#include <Python.h>

static PyMethodDef NoMethods[] =
{
     {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION < 3

PyMODINIT_FUNC
init_freeimage(void)
{
    Py_InitModule("_zbar", NoMethods);
}

#else

static struct PyModuleDef freeimagemodule = {
   PyModuleDef_HEAD_INIT,
   "_zbar",
   NULL,
   -1,
   NoMethods
};

PyMODINIT_FUNC
PyInit__freeimage(void)
{
    return PyModule_Create(&freeimagemodule);
}
#endif