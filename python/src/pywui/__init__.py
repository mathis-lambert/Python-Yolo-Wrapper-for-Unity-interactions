def test():
    import pytest
    return pytest.main()


def main():
    import pywui.main as pywui
    pywui.main().start()
