# buildozer.spec file
[app]
title = Object Detection App
package.name = object_detection_app
package.domain = org.test
source.dir = .
source.include_patterns = coco.txt
source.include_exts = py,png,jpg,kv,atlas
#source.exclude_exts = spec

version = 0.1
requirements = python3==3.11.9,kivy==2.3.0,pyjnius==1.6.1,opencv-python==4.10.0.84,ultralytics==8.2.48,cvzone==1.6.1,pyproject-toml==0.0.10,libffi,pyOpenSSL==24.1.0,thread6,pandas,Cython==3.0.10

orientation = portrait
osx.kivy_version = 1.11.1
fullscreen = 1
android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b
android.gradle_dependencies = com.google.firebase:firebase-ml-modeldownloader::25.0.0
#android.enable_androidx = True
android.gradle_version = 8.8

# (str) Java version to use
android.java_version = 11