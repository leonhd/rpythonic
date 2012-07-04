#!/usr/bin/python
import os, sys
sys.path.append('..')
import rpythonic

if sys.argv[-1].startswith('--output='):
	rpythonic.set_cache( sys.argv[-1].split('=')[-1] )
else:
	rpythonic.set_cache('../examples' )


GINCLUDE = [
	'/usr/include/glib-2.0/',
	'/usr/lib/glib-2.0/include/',
	'/usr/include/cairo/',
	'/usr/include/pango-1.0/',
	'/usr/include/atk-1.0/',
	'/usr/include/gdk-pixbuf-2.0/',
	'/usr/lib/i386-linux-gnu/glib-2.0/include/',		# glibconfig.h
	'/usr/lib/x86_64-linux-gnu/glib-2.0/include/',	# 64bits
]

glibfooter = open( 'glibfooter.py', 'rb' ).read()
gtkfooter = open( 'gtkfooter.py', 'rb' ).read()

if '--gtk3' in sys.argv:
	rpythonic.wrap(
		'gtk3',		# do not use "gtk" (already used by old pygtk)
		header='/usr/include/gtk-3.0/gtk/gtk.h', 
		library='/usr/lib/libgtk-3.so',
		includes=['/usr/include/gtk-3.0/'] + GINCLUDE,
		#defines=['__G_THREAD_H__', '__G_ASYNCQUEUE_H__'],
		ctypes_footer= glibfooter + gtkfooter,
		strip_prefixes = ['GTK_', 'gtk_'],
		insert_headers = ['/usr/include/gtk-3.0/gtk/gtkx.h'],	# required with gtk3 
	)


if '--clutter' in sys.argv:
	# yum install clutter-gtk-devel		# this also gets gtk-devel
	rpythonic.wrap(
		'libclutter-gtk',
		header='/usr/include/clutter-gtk-1.0/clutter-gtk/clutter-gtk.h', 
		library_name='libclutter-gtk-1.0',
		includes=[
			'/usr/include/gtk-3.0/',
			 '/usr/include/clutter-1.0/',
			 '/usr/include/cogl/',	# required
			'/usr/include/json-glib-1.0/',	
			] + GINCLUDE,
		ctypes_footer= glibfooter + gtkfooter,
		strip_prefixes = ['GTK_', 'gtk_', 'clutter_'],
	)


###############################

GTK2INCLUDE = [
	'/usr/include/gtk-2.0/',
	'/usr/lib/gtk-2.0/include/',						# gdkconfig.h
]

if '--gtk2' in sys.argv:
	rpythonic.wrap( 
		'gtk2', 
		header='/usr/include/gtk-2.0/gtk/gtk.h', 
		includes=GTK2INCLUDE + GINCLUDE, ctypes_footer=glibfooter + gtkfooter,
		library= '/usr/lib/libgtk-x11-2.0.so',
		strip_prefixes = ['GTK_', 'gtk_'],
	)



if '--wnck' in sys.argv:
	#sudo apt-get install libwnck-dev
	rpythonic.wrap( 'wnck', 
		defines = ['WNCK_I_KNOW_THIS_IS_UNSTABLE'],
		#includes=[ '/usr/include/libwnck-1.0'] + GTK2INCLUDE + GINCLUDE,
		includes=[ '/usr/include/libwnck-1.0', '/usr/include/gtk-3.0/'] + GINCLUDE,
		header='/usr/include/libwnck-1.0/libwnck/libwnck.h',
		library = '/usr/lib/libwnck-1.so',
		strip_prefixes = ['wnck_'],
	)


if '--gimp' in sys.argv:
	rpythonic.wrap( 'libgimp', 
		header='/usr/include/gimp-2.0/libgimp/gimp.h',
		library = '/usr/lib/libgimp-2.0.so',
		includes = ['/usr/include/gimp-2.0/'] + GINCLUDE,
		strip_prefixes = ['gimp_', 'Gimp', 'GIMP'],
	)

if '--gstreamer' in sys.argv:
	# apt-get install libgstreamer0.10-dev

	## TODO glib connect in footer - get from magicheader.py
	footer = '''
_RETURNS_CHARP_ = (
	gst_version_string,
	gst_structure_get_name,
	gst_format_get_name,
	gst_message_type_get_name,
	gst_element_state_get_name,
)

for func in _RETURNS_CHARP_:
	func.return_wrapper = lambda pointer=None: _CHARP2STRING(pointer)
'''

	rpythonic.wrap( 'libgstreamer', 
		header='/usr/include/gstreamer-0.10/gst/gst.h',
		library = 'libgstreamer-0.10.so',
		includes = ['/usr/include/gstreamer-0.10/', '/usr/include/libxml2'] + GINCLUDE,
		ctypes_footer = glibfooter + footer,
		strip_prefixes = ['gst_'],
	)


if '--nautilus' in sys.argv:
	# sudo yum install eel2-devel nautilus-devel
	# and get source code from git #
	# sudo yum install libxml2-devel

	headers = []
	for path in ('../../nautilus/src', '../../nautilus/libnautilus-private','../../nautilus/libnautilus-extension'):
		for name in os.listdir( path ):
			if name.endswith('.h'):
				if name == 'nautilus-undo-private.h': continue
				if name == 'nautilus-extension-i18n.h': continue
				if name == 'nautilus-window.h': continue
				if name == 'nautilus-list-view-private.h': continue
				if name == 'nautilus-debug.h': continue

				headers.append( os.path.join(path,name) )
	print('---------------------NAUTILUS HEADERS------------------------')
	headers.sort()
	for name in headers: print(name)

	includes = ['/usr/include/libxml2', '../../nautilus', '../../nautilus/src', '../../nautilus/libnautilus-extension', '../../nautilus/libnautilus-private']

	rpythonic.wrap( 'libnautilus', 
		header='../../nautilus/src/nautilus-window.h',
		insert_headers = headers,
		includes=[
			'/usr/include/gtk-3.0/',
			] + GINCLUDE + includes,
		ctypes_footer= glibfooter + gtkfooter,
		strip_prefixes = ['GTK_', 'gtk_'],
	)

if '--gio' in sys.argv:
	rpythonic.wrap( 'libgio', 
		header='/usr/include/glib-2.0/gio/gio.h',
		includes = GINCLUDE,
		ctypes_footer= glibfooter,
		strip_prefixes = ['g_'],
		library_names = ['/usr/lib/x86_64-linux-gnu/libgio-2.0.so', '/usr/lib/i386-linux-gnu/libgio-2.0.so'],
	)

if '--gvfs' in sys.argv:	# not working
	rpythonic.wrap( 'libgvfs', 
		header='/usr/include/glib-2.0/gio/gvfs.h',
		includes = GINCLUDE,
		ctypes_footer= glibfooter,
		strip_prefixes = ['g_'],
		library_names = ['/usr/lib/x86_64-linux-gnu/gvfs/libgvfscommon.so', '/usr/lib/x86_64-linux-gnu/gvfs/libgvfscommon-dnssd.so'],
	)


