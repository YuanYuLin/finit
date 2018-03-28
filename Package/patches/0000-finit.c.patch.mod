--- finit.c.orig	2015-12-02 05:32:30.000000000 +0800
+++ finit.c	2018-01-30 22:11:43.371332265 +0800
@@ -100,10 +100,23 @@
 	mount("none", "/proc", "proc", 0, NULL);
 	mount("none", "/proc/bus/usb", "usbfs", 0, NULL);
 	mount("none", "/sys", "sysfs", 0, NULL);
+	mount("none", "/tmp", "tmpfs", 0, NULL);
+	mkdir("/tmp/var", 0755);
+	mkdir("/tmp/hdd", 0755);
+	touch("/tmp/resolv.conf");
+	mount("none", "/dev", "devtmpfs", 0, NULL);
+        makedir("/cgroup", 0755);
+        mount("none", "/sys/fs/cgroup", "cgroup", 0, NULL);
 	makedir("/dev/pts", 0755);
 	makedir("/dev/shm", 0755);
+	makedir("/dev/mqueue", 0755);
+        mount("none", "/dev/mqueue", "mqueue", 0, NULL);
 	mount("none", "/dev/pts", "devpts", 0, "gid=5,mode=620");
 	mount("none", "/dev/shm", "tmpfs", 0, NULL);
+	makedir("/var/run", 0755);
+	makedir("/var/spool", 0755);
+	makedir("/var/spool/cron", 0755);
+	makedir("/var/spool/cron/crontabs", 0755);
 	umask(022);
 
 	/*
