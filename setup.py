from setuptools import setup

setup(
    name='zhanglyLabTools',
    version='0.1',
    packages=['zhanglyLabTools'],
    entry_points={
    'console_scripts': [
        'zhanglyLabTools=zhanglyLabTools.zhanglyLabTools:main'
    ]
})
