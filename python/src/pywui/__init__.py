############################
# @Author: Mathis LAMBERT
# @Date: Janvier 2024
############################

def test():
    """
    Run pytest on the project.
    """
    import pytest
    return pytest.main()


def main():
    """
    Run the main program.
    """
    import pywui.main as pywui
    pywui.main().start()
