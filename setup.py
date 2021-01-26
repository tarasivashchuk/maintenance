 from distutils.core import setup

with open("README.md", "w") as readme_file:
    long_description = readme_file.read()

setup(
    name='PyClean',
    version='1.0.0',
    packages=['pyclean'],
    scripts=['scripts/pyclean'],
    script_args=[''],
    install_requires=['alive-progress'],
    url='https://github.com/tarasivashchuk/pyclean',
    license='MIT',
    author='Taras',
    author_email='taras@tarasivashchuk.com',
    description='A simple CLI tool for cleaning up your system recursively using glob patterns, originally intended for cleaning up cache files from your projects',
    long_description=long_description,
    long_description_content_type="text/markdown"
)
