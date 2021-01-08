# Reggie-JP
Reggie next アプリ自体の日本語化とインストーラー<br>
元のReggie→https://github.com/aboood40091/Reggie-Next-M3<br>
<del>buildができなかったのでPython要ります。</del><br>
buildできました。もしbuildできない人いたらwindows_build.pyをこれに置き換えてください。

<h2>PyQt5の不具合(2021年1月7日時点)</h2>
PyQt5で不具合があるみたいです。<br>
環境変数PATHでQT_QPA_PLATFORM_PLUGIN_PATHに"pythonのPATH"\Lib\site-packages\PyQt5\Qt\plugins\platformsを通さないといけないようです。
https://answers.ros.org/question/354707/qtqpaplugin-could-not-find-the-qt-platform-plugin-windows-in/
