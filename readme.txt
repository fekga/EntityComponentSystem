Q. How to make examples work?
A. You need to be in the root directory and use this command:
~ EntityComponentSystem> python -m examples.0_simple_example

Q. How to install packages required for testing?
A. You need to install the tests\requirements.txt with pip, like this:
~ EntityComponentSystem\entitycomponentsystem\tests> pip install -r requirements.txt

Q. How to run a test?
A. You need to be in the root directory and use this command:
~ EntityComponentSystem> python -m entitycomponentsystem.tests.test_component

Q. How to run all tests?
A. You need to be in the root directory and use this command:
~ EntityComponentSystem> nosetests