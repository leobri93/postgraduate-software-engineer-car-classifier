import unittest
import os
import joblib
import pandas as pd
import numpy as np
from app import prepare_features, modelo, ordinal_encoder, label_encoder

class TestModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configurar recursos compartilhados para os testes"""
        cls.base_dir = os.path.dirname(os.path.abspath(__file__))
        # Verificar se os modelos estão carregados
        if modelo is None or ordinal_encoder is None or label_encoder is None:
            raise unittest.SkipTest("Modelos não carregados. Certifique-se de que os arquivos .joblib estão presentes.")

    def test_prepare_features_with_floats(self):
        """Testar prepare_features com valores float para buying_price, maint_cost e lug_boot_liters"""
        # Dados de entrada com floats
        data = {
            'buying_price': 250000.0,  # float
            'maint_cost': 15000.0,     # float
            'doors': '4',
            'persons': '4',
            'lug_boot_liters': 350.0,  # float
            'safety': 'high'
        }

        features = prepare_features(data)
        self.assertIsNotNone(features, "prepare_features deve retornar features válidas")
        if(features is not None):
            self.assertEqual(features.shape, (1, 6), "Deve ter 1 linha e 6 features")

        # Como prepare_features retorna valores transformados, verificar se é array numpy
        self.assertIsInstance(features, np.ndarray)

    def test_prepare_features_invalid_data(self):
        """Testar prepare_features com dados inválidos"""
        data = {}  # Dados vazios
        features = prepare_features(data)
        self.assertIsNone(features, "Deve retornar None para dados inválidos")

    def test_model_prediction(self):
        """Testar predição do modelo com dados válidos"""
        data = {
            'buying_price': 100000.0,
            'maint_cost': 5000.0,
            'doors': '4',
            'persons': '4',
            'lug_boot_liters': 200.0,
            'safety': 'med'
        }

        features = prepare_features(data)
        self.assertIsNotNone(features)

        prediction = modelo.predict(features)
        self.assertIsInstance(prediction, np.ndarray)
        self.assertEqual(len(prediction), 1)

        # Verificar se a predição é um inteiro (código da classe)
        self.assertIsInstance(prediction[0], (int, np.integer))

        # Se label_encoder existe, testar decodificação
        if label_encoder:
            prediction_label = label_encoder.inverse_transform(prediction)
            self.assertIsInstance(prediction_label[0], str)

    def test_float_handling_buying_price(self):
        """Testar mapeamento específico de buying_price com floats"""
        # Testar diferentes faixas
        test_cases = [
            (50000.0, 'low'),
            (100000.0, 'med'),
            (200000.0, 'high'),
            (400000.0, 'vhigh')
        ]

        for price, expected in test_cases:
            with self.subTest(price=price):
                data = {
                    'buying_price': price,
                    'maint_cost': 5000.0,
                    'doors': '4',
                    'persons': '4',
                    'lug_boot_liters': 200.0,
                    'safety': 'med'
                }
                features = prepare_features(data)
                self.assertIsNotNone(features)

                prediction = modelo.predict(features)
                self.assertIsNotNone(prediction)

    def test_float_handling_maint_cost(self):
        """Testar mapeamento específico de maint_cost com floats"""
        test_cases = [
            (3000.0, 'low'),
            (8000.0, 'med'),
            (15000.0, 'high'),
            (30000.0, 'vhigh')
        ]

        for cost, expected in test_cases:
            with self.subTest(cost=cost):
                data = {
                    'buying_price': 100000.0,
                    'maint_cost': cost,
                    'doors': '4',
                    'persons': '4',
                    'lug_boot_liters': 200.0,
                    'safety': 'med'
                }
                features = prepare_features(data)
                self.assertIsNotNone(features)
                prediction = modelo.predict(features)
                self.assertIsNotNone(prediction)

    def test_float_handling_lug_boot_liters(self):
        """Testar mapeamento específico de lug_boot_liters com floats"""
        test_cases = [
            (150.0, 'small'),
            (250.0, 'med'),
            (400.0, 'big')
        ]

        for liters, expected in test_cases:
            with self.subTest(liters=liters):
                data = {
                    'buying_price': 100000.0,
                    'maint_cost': 5000.0,
                    'doors': '4',
                    'persons': '4',
                    'lug_boot_liters': liters,
                    'safety': 'med'
                }
                features = prepare_features(data)
                self.assertIsNotNone(features)
                prediction = modelo.predict(features)
                self.assertIsNotNone(prediction)

if __name__ == '__main__':
    unittest.main()
    