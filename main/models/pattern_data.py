class PatternData:
    def __init__(self):
        self.patterns = {
            # Creational patterns
            # Singleton
            "Singleton": {
                "name": "Singleton",
                "type": "Creational",
                "classes": ["Singleton"],
                "relationships": [],
                "code": (
                    "class NetworkPrinter:\n"
                    "    _instance = None  # only one printer in the office\n\n"
                    "    def __new__(cls):\n"
                    "        if cls._instance is None:\n"
                    "            cls._instance = super().__new__(cls)\n"
                    "        return cls._instance\n\n"
                    "    def __init__(self):\n"
                    "        if not hasattr(self, 'initialized'):\n"
                    "            self.print_jobs = []  # queue of print jobs\n"
                    "            self.initialized = True\n\n"
                    "    def add_job(self, job_name):\n"
                    "        self.print_jobs.append(job_name)\n"
                    "        print(f\"Job '{job_name}' added to the printer queue\")\n\n"
                    "# Example usage: multiple users share the same printer\n"
                    "alice_printer = NetworkPrinter()\n"
                    "bob_printer = NetworkPrinter()\n"
                    "\n"
                    "alice_printer.add_job('Report.pdf')\n"
                    "bob_printer.add_job('Presentation.pptx')\n"
                    "\n"
                    "print(f\"Are both users using the same printer instance? {alice_printer is bob_printer}\")\n"
                    "print(f\"Printer queue: {alice_printer.print_jobs}\")\n"
                )
            },

            # Factory Method
            "Factory Method": {
                "name": "Factory Method",
                "type": "Creational",
                "classes": ["DrawingApp", "PencilApp", "PenApp", "BrushApp", "Tool", "Pencil", "Pen", "Brush"],
                "relationships": [
                    ("DrawingApp", "PencilApp"),
                    ("DrawingApp", "PenApp"),
                    ("DrawingApp", "BrushApp"),
                    ("Tool", "Pencil"),
                    ("Tool", "Pen"),
                    ("Tool", "Brush")
                ],
                "code": (
                    "from abc import ABC, abstractmethod\n\n"
                    "# Product interface: a drawing tool\n"
                    "class Tool(ABC):\n"
                    "    @abstractmethod\n"
                    "    def draw(self):\n"
                    "        pass\n\n"
                    "# Concrete Products: ways to draw\n"
                    "class Pencil(Tool):\n"
                    "    def draw(self):\n"
                    "        return 'Drawing with a pencil'\n\n"
                    "class Pen(Tool):\n"
                    "    def draw(self):\n"
                    "        return 'Drawing with a pen'\n\n"
                    "class Brush(Tool):\n"
                    "    def draw(self):\n"
                    "        return 'Drawing with a brush'\n\n"
                    "# Creator defines the factory method\n"
                    "class DrawingApp(ABC):\n"
                    "    @abstractmethod\n"
                    "    def create_tool(self) -> Tool:\n"
                    "        pass\n\n"
                    "    def render_drawing(self):\n"
                    "        tool = self.create_tool()\n"
                    "        return f'DrawingApp uses: {tool.draw()}'\n\n"
                    "# Concrete Creators override the factory method\n"
                    "class PencilApp(DrawingApp):\n"
                    "    def create_tool(self):\n"
                    "        return Pencil()\n\n"
                    "class PenApp(DrawingApp):\n"
                    "    def create_tool(self):\n"
                    "        return Pen()\n\n"
                    "class BrushApp(DrawingApp):\n"
                    "    def create_tool(self):\n"
                    "        return Brush()\n\n"
                    "# Example usage: simulate a user drawing with different tools\n"
                    "apps = [PencilApp(), PenApp(), BrushApp()]\n"
                    "for app in apps:\n"
                    "    print(app.render_drawing())\n"
                )
            },

            # Abstract Factory
            "Abstract Factory": {
                "name": "Abstract Factory",
                "type": "Creational",
                "classes": [
                    "FurnitureFactory", "ModernFurnitureFactory", "VictorianFurnitureFactory",
                    "Chair", "Sofa", "ModernChair", "ModernSofa", "VictorianChair", "VictorianSofa"
                ],
                "relationships": [
                    ("FurnitureFactory", "ModernFurnitureFactory"),
                    ("FurnitureFactory", "VictorianFurnitureFactory"),
                    ("Chair", "ModernChair"),
                    ("Chair", "VictorianChair"),
                    ("Sofa", "ModernSofa"),
                    ("Sofa", "VictorianSofa")
                ],
                "code": (
                    "from abc import ABC, abstractmethod\n\n"
                    "# Abstract Products\n"
                    "class Chair(ABC):\n"
                    "    @abstractmethod\n"
                    "    def sit_on(self):\n"
                    "        pass\n\n"
                    "class Sofa(ABC):\n"
                    "    @abstractmethod\n"
                    "    def lie_on(self):\n"
                    "        pass\n\n"
                    "# Concrete Products - Modern style\n"
                    "class ModernChair(Chair):\n"
                    "    def sit_on(self):\n"
                    "        return 'Sitting on a modern chair'\n\n"
                    "class ModernSofa(Sofa):\n"
                    "    def lie_on(self):\n"
                    "        return 'Lying on a modern sofa'\n\n"
                    "# Concrete Products - Victorian style\n"
                    "class VictorianChair(Chair):\n"
                    "    def sit_on(self):\n"
                    "        return 'Sitting on a Victorian chair'\n\n"
                    "class VictorianSofa(Sofa):\n"
                    "    def lie_on(self):\n"
                    "        return 'Lying on a Victorian sofa'\n\n"
                    "# Abstract Factory\n"
                    "class FurnitureFactory(ABC):\n"
                    "    @abstractmethod\n"
                    "    def create_chair(self) -> Chair:\n"
                    "        pass\n\n"
                    "    @abstractmethod\n"
                    "    def create_sofa(self) -> Sofa:\n"
                    "        pass\n\n"
                    "# Concrete Factories\n"
                    "class ModernFurnitureFactory(FurnitureFactory):\n"
                    "    def create_chair(self):\n"
                    "        return ModernChair()\n\n"
                    "    def create_sofa(self):\n"
                    "        return ModernSofa()\n\n"
                    "class VictorianFurnitureFactory(FurnitureFactory):\n"
                    "    def create_chair(self):\n"
                    "        return VictorianChair()\n\n"
                    "    def create_sofa(self):\n"
                    "        return VictorianSofa()\n\n"
                    "# Example usage: create two furniture sets\n"
                    "def client(factory: FurnitureFactory):\n"
                    "    chair = factory.create_chair()\n"
                    "    sofa = factory.create_sofa()\n"
                    "    print(chair.sit_on())\n"
                    "    print(sofa.lie_on())\n\n"
                    "print('Modern furniture set:')\n"
                    "client(ModernFurnitureFactory())\n\n"
                    "print('\\nVictorian furniture set:')\n"
                    "client(VictorianFurnitureFactory())\n"
                )
            },

            # Prototype
            "Prototype": {
                "name": "Prototype",
                "type": "Creational",
                "classes": ["Key", "KeyPrototype"],
                "relationships": [],
                "code": (
                    "import copy\n\n"
                    "# Prototype class: a keyboard key\n"
                    "class Key:\n"
                    "    def __init__(self, label, color='white'):\n"
                    "        self.label = label\n"
                    "        self.color = color\n\n"
                    "    def clone(self):\n"
                    "        # Return a copy of this key\n"
                    "        return copy.deepcopy(self)\n\n"
                    "    def __str__(self):\n"
                    "        return f'Key(label={self.label}, color={self.color})'\n\n"
                    "# Example usage: cloning keys\n"
                    "original_key = Key('A', 'blue')\n"
                    "print(f'Original: {original_key}')\n\n"
                    "cloned_key1 = original_key.clone()\n"
                    "cloned_key2 = original_key.clone()\n"
                    "\n"
                    "# Modify one clone without affecting the original\n"
                    "cloned_key1.color = 'red'\n\n"
                    "print(f'Cloned key 1: {cloned_key1}')\n"
                    "print(f'Cloned key 2: {cloned_key2}')\n"
                    "print(f'Original after cloning: {original_key}')\n"
                )
            },

            # Builder
            "Builder": {
                "name": "Builder",
                "type": "Creational",
                "classes": ["House", "HouseBuilder", "ModernHouseBuilder", "VictorianHouseBuilder", "Director"],
                "relationships": [
                    ("HouseBuilder", "ModernHouseBuilder"),
                    ("HouseBuilder", "VictorianHouseBuilder")
                ],
                "code": (
                    "# Product: the House\n"
                    "class House:\n"
                    "    def __init__(self):\n"
                    "        self.parts = []\n\n"
                    "    def add(self, part):\n"
                    "        self.parts.append(part)\n\n"
                    "    def __str__(self):\n"
                    "        return f'House with: {', '.join(self.parts)}'\n\n"
                    "# Abstract Builder\n"
                    "class HouseBuilder:\n"
                    "    def __init__(self):\n"
                    "        self.house = House()\n\n"
                    "    def build_walls(self): pass\n"
                    "    def build_roof(self): pass\n"
                    "    def build_garden(self): pass\n\n"
                    "    def get_house(self):\n"
                    "        return self.house\n\n"
                    "# Concrete Builder: Modern House\n"
                    "class ModernHouseBuilder(HouseBuilder):\n"
                    "    def build_walls(self):\n"
                    "        self.house.add('glass walls')\n"
                    "    def build_roof(self):\n"
                    "        self.house.add('flat roof')\n"
                    "    def build_garden(self):\n"
                    "        self.house.add('minimalist garden')\n\n"
                    "# Concrete Builder: Victorian House\n"
                    "class VictorianHouseBuilder(HouseBuilder):\n"
                    "    def build_walls(self):\n"
                    "        self.house.add('brick walls')\n"
                    "    def build_roof(self):\n"
                    "        self.house.add('sloped roof')\n"
                    "    def build_garden(self):\n"
                    "        self.house.add('flower garden')\n\n"
                    "# Director controls the building process\n"
                    "class Director:\n"
                    "    def __init__(self, builder):\n"
                    "        self.builder = builder\n\n"
                    "    def construct_house(self):\n"
                    "        self.builder.build_walls()\n"
                    "        self.builder.build_roof()\n"
                    "        self.builder.build_garden()\n"
                    "        return self.builder.get_house()\n\n"
                    "# Example usage\n"
                    "modern_builder = ModernHouseBuilder()\n"
                    "victorian_builder = VictorianHouseBuilder()\n\n"
                    "director = Director(modern_builder)\n"
                    "modern_house = director.construct_house()\n"
                    "print(modern_house)\n\n"
                    "director = Director(victorian_builder)\n"
                    "victorian_house = director.construct_house()\n"
                    "print(victorian_house)\n"
                )
            }

        }

    def get_pattern(self, name):
        return self.patterns.get(name, None)

    def get_patterns_by_type(self, pattern_type):
        return [name for name, data in self.patterns.items() if data['type'] == pattern_type]
