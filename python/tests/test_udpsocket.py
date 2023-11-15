import pytest
from src.udpsocket import updsocket
from unittest.mock import MagicMock, patch


class TestUpdSocket:
    def setup_method(self):
        self.mock_socket = MagicMock()
        self.patcher = patch('socket.socket', return_value=self.mock_socket)
        self.patcher.start()

        # Créer une instance de updsocket avec des paramètres fictifs
        self.updsocket_instance = updsocket("127.0.0.1", 8000, 8001)

    def teardown_method(self):
        self.patcher.stop()

    def test_constructor(self):
        # Vérifier si le socket a été créé et lié
        self.mock_socket.bind.assert_called_with(("127.0.0.1", 8001))

    def test_send_data(self):
        # Simuler l'envoi de données
        self.updsocket_instance.SendData("test message")
        self.mock_socket.sendto.assert_called()

    def test_receive_data_disabled_rx(self):
        # Tester la réception de données lorsque RX est désactivé
        self.updsocket_instance.enableRX = False
        with pytest.raises(ValueError):
            self.updsocket_instance.ReceiveData()

    def test_close_socket(self):
        self.updsocket_instance.CloseSocket()
        self.mock_socket.close.assert_called_once()

    def test_receive_data_error_handling(self):
        # Simuler une exception lors de la réception des données
        self.mock_socket.recvfrom.side_effect = ValueError("Erreur de test")
        self.updsocket_instance.enableRX = True

        with pytest.raises(ValueError):
            self.updsocket_instance.ReceiveData()

    def test_read_received_data(self):
        self.updsocket_instance.dataRX = "Test Data"
        self.updsocket_instance.isDataReceived = True

        data = self.updsocket_instance.ReadReceivedData()
        assert data == "Test Data"
        assert not self.updsocket_instance.isDataReceived
        assert self.updsocket_instance.dataRX is None
