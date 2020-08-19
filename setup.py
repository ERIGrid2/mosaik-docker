from setuptools import setup, find_packages


setup(
    name = 'mosaik-docker',
    maintainer = 'ERIGrid 2.0 development team',
    maintainer_email = 'edmund.widl@ait.ac.at',
    url = 'https://github.com/ERIGrid/mosaik-docker',
    version = '0.1',
    platforms = [ 'any' ],
    packages = find_packages(),
    package_data = {
        'mosaik_docker': [ 
            'sim_setup_template/cookiecutter.json',
            'sim_setup_template/{{cookiecutter.directory_name}}/mosaik-docker.json',
            'sim_setup_template/{{cookiecutter.directory_name}}/dockerfiles/*',
        ],
    },
    install_requires = [
        'cookiecutter',
        'mosaik'
    ],
    entry_points={
        'console_scripts': [
            'create_sim_setup = mosaik_docker.cli.create_sim_setup:main',
            'configure_sim_setup = mosaik_docker.cli.configure_sim_setup:main',
            'check_sim_setup = mosaik_docker.cli.check_sim_setup:main',
            'build_sim_setup = mosaik_docker.cli.build_sim_setup:main',
            'get_sim_setup_root = mosaik_docker.cli.get_sim_setup_root:main',
            'start_sim = mosaik_docker.cli.start_sim:main',
            'cancel_sim = mosaik_docker.cli.cancel_sim:main',
            'clear_sim = mosaik_docker.cli.clear_sim:main',
            'get_sim_status = mosaik_docker.cli.get_sim_status:main',
            'get_sim_results = mosaik_docker.cli.get_sim_results:main',
            'get_sim_ids = mosaik_docker.cli.get_sim_ids:main',
            'delete_sim_setup = mosaik_docker.cli.delete_sim_setup:main',
        ]
    },
    description = 'Add-on package for the Docker-based execution of the mosaik co-simulation framework.',
    long_description = 'README.md',
    license = 'BSD 2-Clause License',
    keywords = [
        'mosaik',
        'Docker',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
)
