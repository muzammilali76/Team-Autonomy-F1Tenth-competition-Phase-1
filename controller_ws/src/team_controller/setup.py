from setuptools import setup

setup(
    name='team_controller', version='0.1.0', packages=['team_controller'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/team_controller']),
        ('share/team_controller', ['package.xml']),
    ],
    install_requires=['setuptools'],
    entry_points={'console_scripts': ['controller = team_controller.controller_node:main']},
    license='MIT', description='Known-track Levine Pure Pursuit practice controller',
    maintainer='khubaib', maintainer_email='khubaib@example.com',
)
