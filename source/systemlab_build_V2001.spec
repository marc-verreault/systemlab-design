# -*- mode: python -*-
#import PyInstaller.config
#PyInstaller.config.CONF['distpath'] = "./systemlab-design-release-2/"

block_cipher = None
import sys
sys.setrecursionlimit(5000)

a = Analysis(['systemlab_main_v2001_r2.py'],
             pathex=['C:\\SystemLab_Dev\\systemlab-design-release-2\\'],
             binaries=[],
             datas=[('syslab_gui_files', 'syslab_gui_files'),
		    ('syslab_gui_icons', 'syslab_gui_icons'),
            ('syslab_fb_icons', 'syslab_fb_icons'),
            ('syslab_fb_scripts', 'syslab_fb_scripts'),
            ('syslab_fb_library', 'syslab_fb_library'),
		    ('syslab_documentation', 'syslab_documentation'),
		    ('systemlab_examples', 'systemlab_examples'),
            ('syslab_config_files', 'syslab_config_files'),
            ('wscite', 'wscite'),
		    ('SplashScreen_SystemLab.png', '.'),
            ('LICENSE.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['sphinx'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SystemLab-Design',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
	  icon='C:\\SystemLab_Dev\\systemlab-design-release-2\\syslab_app_icons\\SystemLabDesignAppIconBlue.ico',
          version = 'C:\\SystemLab_Dev\\systemlab-design-release-2\\file_version_info.rc' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='systemlab_design')
