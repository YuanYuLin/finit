import ops
import iopc

TARBALL_FILE="finit-2.4.tar.xz"
TARBALL_DIR="finit-2.4"
INSTALL_DIR="finit-bin"
pkg_path = ""
output_dir = ""
tarball_pkg = ""
tarball_dir = ""
install_dir = ""

def set_global(args):
    global pkg_path
    global output_dir
    global tarball_pkg
    global install_dir
    global tarball_dir
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    tarball_pkg = ops.path_join(pkg_path, TARBALL_FILE)
    install_dir = ops.path_join(output_dir, INSTALL_DIR)
    tarball_dir = ops.path_join(output_dir, TARBALL_DIR)

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("CC", ops.getEnv("CROSS_COMPILE") + "gcc"))
    ops.exportEnv(ops.setEnv("CROSS", ops.getEnv("CROSS_COMPILE")))
    ops.exportEnv(ops.setEnv("DESTDIR", install_dir))

    return False

def MAIN_EXTRACT(args):
    set_global(args)

    ops.unTarXz(tarball_pkg, output_dir)
    ops.copyto(ops.path_join(pkg_path, "finit.conf"), output_dir)

    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(tarball_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    extra_conf = []
    #extra_conf.append("--with-runlevel=3")
    extra_conf.append("--enable-embedded")
    #extra_conf.append("--enable-rw-rootfs")
    extra_conf.append("--disable-inetd")
    extra_conf.append("--enable-debug")
    #extra_conf.append("--with-plugins=bootmisc netlink time urandom initctl zram dropbear")
    extra_conf.append("--with-plugins=bootmisc netlink time urandom initctl")
    iopc.configure(tarball_dir, extra_conf)

    return True

def MAIN_BUILD(args):
    set_global(args)

    iopc.make(tarball_dir)
    iopc.make_install(tarball_dir)
    return False

def MAIN_INSTALL(args):
    set_global(args)

    ops.ln(install_dir, "/sbin/finit", "init")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "etc/."), "etc")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "lib/libite.so.2"), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "lib/libite.so"), "lib")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "lib/finit/."), "lib/finit")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "sbin/."), "sbin")
    iopc.installBin(args["pkg_name"], ops.path_join(install_dir, "init"), "")
    iopc.installBin(args["pkg_name"], ops.path_join(output_dir, "finit.conf"), "etc")

    #tarball_dir = ops.path_join(output_dir, TARBALL_DIR)
    #ops.mkdir(ops.path_join(iopc.getBinPkgPath(args["pkg_name"]), "sbin"))

    #iopc.make_install(tarball_dir)
    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)

