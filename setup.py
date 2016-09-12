import distutils.command
import distutils.command.build_ext
import distutils.core
import distutils.errors

SRCS = '''Source/zbar/decoder.c
Source/zbar/decoder/code128.c
Source/zbar/decoder/code39.c
Source/zbar/decoder/ean.c
Source/zbar/decoder/i25.c
Source/zbar/decoder/pdf417.c
Source/zbar/decoder/qr_finder.c
Source/zbar/error.c
Source/zbar/img_scanner.c
Source/zbar/qrcode/bch15_5.c
Source/zbar/qrcode/binarize.c
Source/zbar/qrcode/isaac.c
Source/zbar/qrcode/qrdec.c
Source/zbar/qrcode/qrdectxt.c
Source/zbar/qrcode/rs.c
Source/zbar/qrcode/util.c
Source/zbar/refcnt.c
Source/zbar/scanner.c
Source/zbar/symbol.c'''.split('\n')

INCLUDE = 'Source', 'Source/zbar'

zbar = distutils.core.Extension('zbar._zbar',
    sources = ['zbar/_zbar.c'] + SRCS,
    include_dirs = INCLUDE,
    define_macros = [
        ('ENABLE_QRCODE', None),
        ('ENABLE_EAN', None),
        ('ENABLE_I25', None),
        ('ENABLE_CODE39', None),
        ('ENABLE_CODE128', None),
        ('ENABLE_PDF417', None),
        ('HAVE_INTTYPES_H', None),
        ('ZBAR_VERSION_MAJOR', 0),
        ('ZBAR_VERSION_MINOR', 10),
        ('NO_STATS', None)]
)

class BuildExt(distutils.command.build_ext.build_ext):
    @staticmethod
    def has_lib(compiler, libname):
        """Return a boolean indicating whether a linker flag name is supported on
        the specified compiler.
        """
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.cpp') as f:
            f.write('int main (int argc, char **argv) { return 0; }')
            try:
                compiler.link_executable(compiler.compile([f.name]), "aksdfjhawkdjlfhkasdjhfkljasdhfkjahsdf", libraries=[libname])
            except (distutils.errors.CompileError, distutils.errors.LinkError):
                return False
        return True

    """A custom build extension for adding compiler-specific options."""
    def build_extensions(self):
        ldflags = []
        if self.has_lib(self.compiler, 'iconv'):
            ldflags.append('-liconv')
        for ext in self.extensions:
            ext.extra_link_args = ldflags
            distutils.command.build_ext.build_ext.build_extensions(self)

distutils.core.setup(
    name = 'zbar',
    version = '1.0',
    description = 'zbar package',
    ext_modules = [zbar],
    packages = ['zbar'],
    cmdclass={'build_ext': BuildExt}
 )
