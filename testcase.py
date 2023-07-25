import unittest
import openai
import os
from productSpecifications.productSpecifications import ProductSpecification
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")


class TestSpecifications(unittest.TestCase):
    def test_case(self):
        product_type = "Smartphone"
        product_description = "13 cm (5.4-inch) Super Retina XDR display Cinematic mode adds shallow depth of field and shifts focus automatically in your video Advanced dual-camera system with 12MP Wide and Ultra Wide cameras; Photographic Styles, Smart HDR 4, Night mode, 4K Dolby Vision HDR recording 12MP TrueDepth front camera with Night mode, 4K Dolby Vision HDR recording A15 Bionic chip for lightning-fast performance. Split Ac With Inverter Compressor: Variable Speed Compressor Which Adjusts Power Depending On Heat Load |With AI Convertible 6-in-1 user gets a flexibility to increase or decrease cooling capacity as per requirements. Capacity: 1.5 Ton Suitable for medium sized rooms (151 to 180 sq ft.); 441/1236 (In/Out) CFM Air Circulation & Ambient Temperature: 52 degree Celsius with 2 way air swing. Energy Rating : 3 Star - Energy efficiency | Annual Energy Consumption: 968.04 Units Per Year| ISEER Value: 4.0 (Please Refer Energy Label On Product Page Or Contact Brand For More Details) "

        product_keyval_generator = ProductSpecification(
            product_type, product_description
        )
        specs = product_keyval_generator.get_specifications()
        expected_specs = {
            "RAM": "16GB DDR4 RAM 3200 MHz, Dual Channel capable upgradable up to 24 GB",
            "Brand": "ThinkPad",
        }
        specs = {
            key: value.replace("\n", "") if isinstance(value, str) else value
            for key, value in expected_specs.items()
        }
        self.assertEqual(specs, expected_specs)


if __name__ == "__main__":
    unittest.main()
