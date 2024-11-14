from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    requirment_list:List[str]=[]
    try:
        with open('requirment.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirment=line.strip()
                if requirment and requirment!='-e .':
                    requirment_list.append(requirment)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirment_list

setup(
    name='Network security',
    version='0.0.1',
    author='jain abhishek',
    author_email='abhijain0410@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)
