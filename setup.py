from setuptools import setup, find_packages

setup(
    name='EnviroChlor- Water Disinfection with Chlorine based on DO, Temperature, and NTU', 
    author='Valdrin Beluli',  
    author_email='valdrinengineer@gmail.com',  
    description='An engineering tool for measurements and analyzes the necessary chlorine level for disinfecting water, depending on measured values for DO, temperature, and NTU.',  
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',  
    url='https://github.com/username/water_quality_monitoring_tool',  # URL e projektit në GitHub ose në ndonjë platformë tjetër
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License', 
        'Operating System :: OS Independent',  
    ],
    python_requires='>=3.6',  
    install_requires=[  
        'matplotlib',
        'numpy',
        'tkinter',  
    ],
)