############################
# @Author: Mathis LAMBERT
# @Date: Janvier 2024
############################

def test():
    import pytest
    return pytest.main()


def main():
    import pywui.main as pywui
    pywui.main().start()
