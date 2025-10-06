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
                    "ana_printer = NetworkPrinter()\n"
                    "tony_printer = NetworkPrinter()\n"
                    "\n"
                    "ana_printer.add_job('Report.pdf')\n"
                    "tony_printer.add_job('Presentation.pptx')\n"
                    "\n"
                    "print(f\"Are both users using the same printer instance? {ana_printer is tony_printer}\")\n"
                    "print(f\"Printer queue: {ana_printer.print_jobs}\")\n"
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
            },

            # Structural
            # Adapter
            "Adapter": {
                "name": "Adapter",
                "type": "Structural",
                "classes": ["USPlug", "EUSocket", "PlugAdapter"],
                "relationships": [
                    ("USPlug", "PlugAdapter"),
                    ("PlugAdapter", "EUSocket")
                ],
                "code": (
                    "# Target: the EU Socket (what client expects)\n"
                    "class EUSocket:\n"
                    "    def plug_in(self):\n"
                    "        return \"Powering device with EU socket voltage (230V)\"\n\n"
                    "# Adaptee: US Plug (incompatible interface)\n"
                    "class USPlug:\n"
                    "    def connect(self):\n"
                    "        return \"Using US plug with voltage (120V)\"\n\n"
                    "# Adapter: makes USPlug work with EUSocket\n"
                    "class PlugAdapter(EUSocket):\n"
                    "    def __init__(self, us_plug):\n"
                    "        self.us_plug = us_plug\n\n"
                    "    def plug_in(self):\n"
                    "        # Adapt the connect() method to plug_in()\n"
                    "        return f\"Adapter converts -> {self.us_plug.connect()} to EU standard\"\n\n"
                    "# Example usage\n"
                    "us_plug = USPlug()\n"
                    "adapter = PlugAdapter(us_plug)\n"
                    "print(adapter.plug_in())\n"
                )
            },

            # Bridge
            "Bridge": {
                "name": "Bridge",
                "type": "Structural",
                "classes": ["Color", "Red", "Blue", "Shape", "Circle", "Square"],
                "relationships": [
                    ("Color", "Red"),
                    ("Color", "Blue"),
                    ("Shape", "Circle"),
                    ("Shape", "Square"),
                    ("Shape", "Color")  # bridge connection
                ],
                "code": (
                    "# Implementor: Color\n"
                    "class Color:\n"
                    "    def apply_color(self):\n"
                    "        raise NotImplementedError\n\n"
                    "# Concrete Implementors\n"
                    "class Red(Color):\n"
                    "    def apply_color(self):\n"
                    "        return \"red\"\n\n"
                    "class Blue(Color):\n"
                    "    def apply_color(self):\n"
                    "        return \"blue\"\n\n"
                    "# Abstraction: Shape\n"
                    "class Shape:\n"
                    "    def __init__(self, color: Color):\n"
                    "        self.color = color\n\n"
                    "    def draw(self):\n"
                    "        raise NotImplementedError\n\n"
                    "# Refined Abstractions\n"
                    "class Circle(Shape):\n"
                    "    def draw(self):\n"
                    "        return f\"Drawing a {self.color.apply_color()} circle\"\n\n"
                    "class Square(Shape):\n"
                    "    def draw(self):\n"
                    "        return f\"Drawing a {self.color.apply_color()} square\"\n\n"
                    "# Example usage\n"
                    "red_circle = Circle(Red())\n"
                    "blue_square = Square(Blue())\n"
                    "print(red_circle.draw())\n"
                    "print(blue_square.draw())\n"
                )
            },

            # Composite
            "Composite": {
                "name": "Composite",
                "type": "Structural",
                "classes": ["OrderComponent", "Product", "Package"],
                "relationships": [
                    ("OrderComponent", "Product"),
                    ("OrderComponent", "Package"),
                    ("Package", "OrderComponent")  # composite contains components
                ],
                "code": (
                    "# Component: abstract order item\n"
                    "class OrderComponent:\n"
                    "    def get_price(self):\n"
                    "        raise NotImplementedError\n"
                    "    def show_details(self, indent=0):\n"
                    "        raise NotImplementedError\n\n"
                    "# Leaf: single product\n"
                    "class Product(OrderComponent):\n"
                    "    def __init__(self, name, price):\n"
                    "        self.name = name\n"
                    "        self.price = price\n\n"
                    "    def get_price(self):\n"
                    "        return self.price\n\n"
                    "    def show_details(self, indent=0):\n"
                    "        return ' ' * indent + f\"Product: {self.name} (${self.price})\"\n\n"
                    "# Composite: package of products or sub-packages\n"
                    "class Package(OrderComponent):\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n"
                    "        self.items = []\n\n"
                    "    def add(self, component: OrderComponent):\n"
                    "        self.items.append(component)\n\n"
                    "    def get_price(self):\n"
                    "        return sum(item.get_price() for item in self.items)\n\n"
                    "    def show_details(self, indent=0):\n"
                    "        details = ' ' * indent + f\"Package: {self.name}\\n\"\n"
                    "        for item in self.items:\n"
                    "            details += item.show_details(indent + 2) + \"\\n\"\n"
                    "        return details.rstrip()\n\n"
                    "# Example usage\n"
                    "laptop = Product(\"Laptop\", 1200)\n"
                    "mouse = Product(\"Mouse\", 25)\n"
                    "keyboard = Product(\"Keyboard\", 75)\n\n"
                    "bundle = Package(\"Workstation Bundle\")\n"
                    "bundle.add(laptop)\n"
                    "bundle.add(mouse)\n"
                    "bundle.add(keyboard)\n\n"
                    "gift = Package(\"Gift Package\")\n"
                    "gift.add(Product(\"Headphones\", 100))\n"
                    "gift.add(bundle)\n\n"
                    "print(gift.show_details())\n"
                    "print(f\"Total price: ${gift.get_price()}\")\n"
                )
            },

            # Decorator
            "Decorator": {
                "name": "Decorator",
                "type": "Structural",
                "classes": ["IceCream", "PlainIceCream", "ToppingDecorator", "ChocolateTopping", "NutsTopping"],
                "relationships": [
                    ("IceCream", "PlainIceCream"),
                    ("IceCream", "ToppingDecorator"),
                    ("ToppingDecorator", "ChocolateTopping"),
                    ("ToppingDecorator", "NutsTopping"),
                    ("ToppingDecorator", "IceCream")  # wraps another ice cream
                ],
                "code": (
                    "# Component: IceCream interface\n"
                    "class IceCream:\n"
                    "    def get_description(self):\n"
                    "        raise NotImplementedError\n"
                    "    def get_cost(self):\n"
                    "        raise NotImplementedError\n\n"
                    "# Concrete Component: plain ice cream\n"
                    "class PlainIceCream(IceCream):\n"
                    "    def get_description(self):\n"
                    "        return \"Plain ice cream\"\n\n"
                    "    def get_cost(self):\n"
                    "        return 2.0\n\n"
                    "# Decorator: base class for toppings\n"
                    "class ToppingDecorator(IceCream):\n"
                    "    def __init__(self, ice_cream: IceCream):\n"
                    "        self.ice_cream = ice_cream\n\n"
                    "    def get_description(self):\n"
                    "        return self.ice_cream.get_description()\n\n"
                    "    def get_cost(self):\n"
                    "        return self.ice_cream.get_cost()\n\n"
                    "# Concrete Decorators\n"
                    "class ChocolateTopping(ToppingDecorator):\n"
                    "    def get_description(self):\n"
                    "        return self.ice_cream.get_description() + \", chocolate\"\n\n"
                    "    def get_cost(self):\n"
                    "        return self.ice_cream.get_cost() + 0.5\n\n"
                    "class NutsTopping(ToppingDecorator):\n"
                    "    def get_description(self):\n"
                    "        return self.ice_cream.get_description() + \", nuts\"\n\n"
                    "    def get_cost(self):\n"
                    "        return self.ice_cream.get_cost() + 0.7\n\n"
                    "# Example usage\n"
                    "icecream = PlainIceCream()\n"
                    "print(icecream.get_description(), \"- $\", icecream.get_cost())\n\n"
                    "choco_icecream = ChocolateTopping(PlainIceCream())\n"
                    "print(choco_icecream.get_description(), \"- $\", choco_icecream.get_cost())\n\n"
                    "deluxe_icecream = NutsTopping(ChocolateTopping(PlainIceCream()))\n"
                    "print(deluxe_icecream.get_description(), \"- $\", deluxe_icecream.get_cost())\n"
                )
            },

            # Facade
            "Facade": {
                "name": "Facade",
                "type": "Structural",
                "classes": ["FlightBooking", "HotelBooking", "CarRental", "TravelFacade"],
                "relationships": [
                    ("TravelFacade", "FlightBooking"),
                    ("TravelFacade", "HotelBooking"),
                    ("TravelFacade", "CarRental")
                ],
                "code": (
                    "# Subsystem: Flight booking\n"
                    "class FlightBooking:\n"
                    "    def book_flight(self, destination):\n"
                    "        return f\"Flight booked to {destination}\"\n\n"
                    "# Subsystem: Hotel booking\n"
                    "class HotelBooking:\n"
                    "    def book_hotel(self, destination):\n"
                    "        return f\"Hotel booked in {destination}\"\n\n"
                    "# Subsystem: Car rental\n"
                    "class CarRental:\n"
                    "    def rent_car(self, destination):\n"
                    "        return f\"Car rented in {destination}\"\n\n"
                    "# Facade: simplifies the travel booking process\n"
                    "class TravelFacade:\n"
                    "    def __init__(self):\n"
                    "        self.flight = FlightBooking()\n"
                    "        self.hotel = HotelBooking()\n"
                    "        self.car = CarRental()\n\n"
                    "    def book_trip(self, destination):\n"
                    "        results = []\n"
                    "        results.append(self.flight.book_flight(destination))\n"
                    "        results.append(self.hotel.book_hotel(destination))\n"
                    "        results.append(self.car.rent_car(destination))\n"
                    "        return \"\\n\".join(results)\n\n"
                    "# Example usage\n"
                    "travel_agency = TravelFacade()\n"
                    "print(travel_agency.book_trip(\"Paris\"))\n"
                )
            },

            # Flyweight
            "Flyweight": {
                "name": "Flyweight",
                "type": "Structural",
                "classes": ["Font", "FontFactory", "Character"],
                "relationships": [
                    ("FontFactory", "Font"),
                    ("Character", "Font")
                ],
                "code": (
                    "# Flyweight: Font object (intrinsic state)\n"
                    "class Font:\n"
                    "    def __init__(self, family, size, style):\n"
                    "        self.family = family\n"
                    "        self.size = size\n"
                    "        self.style = style\n\n"
                    "    def __str__(self):\n"
                    "        return f\"Font({self.family}, {self.size}pt, {self.style})\"\n\n"
                    "# Flyweight Factory: manages shared fonts\n"
                    "class FontFactory:\n"
                    "    _fonts = {}\n\n"
                    "    @classmethod\n"
                    "    def get_font(cls, family, size, style):\n"
                    "        key = (family, size, style)\n"
                    "        if key not in cls._fonts:\n"
                    "            cls._fonts[key] = Font(family, size, style)\n"
                    "        return cls._fonts[key]\n\n"
                    "# Context: character that uses a shared font\n"
                    "class Character:\n"
                    "    def __init__(self, char, font: Font):\n"
                    "        self.char = char\n"
                    "        self.font = font  # shared flyweight\n\n"
                    "    def render(self):\n"
                    "        return f\"Character '{self.char}' in {self.font}\"\n\n"
                    "# Example usage\n"
                    "factory = FontFactory()\n"
                    "font1 = factory.get_font(\"Arial\", 12, \"Regular\")\n"
                    "font2 = factory.get_font(\"Arial\", 12, \"Regular\")\n"
                    "font3 = factory.get_font(\"Arial\", 12, \"Bold\")\n\n"
                    "# Characters share the same font instance if attributes match\n"
                    "c1 = Character('H', font1)\n"
                    "c2 = Character('i', font2)\n"
                    "c3 = Character('!', font3)\n\n"
                    "print(c1.render())\n"
                    "print(c2.render())\n"
                    "print(c3.render())\n\n"
                    "print(\"font1 is font2:\", font1 is font2)  # True (shared)\n"
                    "print(\"font1 is font3:\", font1 is font3)  # False (different style)\n"
                )
            },

            # Proxy
            "Proxy": {
                "name": "Proxy",
                "type": "Structural",
                "classes": ["Resource", "RealResource", "SecurityProxy"],
                "relationships": [
                    ("Resource", "RealResource"),
                    ("Resource", "SecurityProxy"),
                    ("SecurityProxy", "RealResource")
                ],
                "code": (
                    "# Subject interface\n"
                    "class Resource:\n"
                    "    def access(self):\n"
                    "        raise NotImplementedError\n\n"
                    "# Real Subject: the actual resource\n"
                    "class RealResource(Resource):\n"
                    "    def access(self):\n"
                    "        return \"Accessing sensitive resource\"\n\n"
                    "# Proxy: checks permissions before delegating to RealResource\n"
                    "class SecurityProxy(Resource):\n"
                    "    def __init__(self, user_role):\n"
                    "        self.user_role = user_role\n"
                    "        self.real_resource = RealResource()\n\n"
                    "    def access(self):\n"
                    "        if self.user_role == \"admin\":\n"
                    "            return self.real_resource.access()\n"
                    "        else:\n"
                    "            return \"Access denied: insufficient permissions\"\n\n"
                    "# Example usage\n"
                    "admin_proxy = SecurityProxy(\"admin\")\n"
                    "guest_proxy = SecurityProxy(\"guest\")\n\n"
                    "print(admin_proxy.access())\n"
                    "print(guest_proxy.access())\n"
                )
            },

            # Behavioral Patterns
            # Chain of Responsibility
            "Chain of Responsibility": {
                "name": "Chain of Responsibility",
                "type": "Behavioral",
                "classes": ["SupportHandler", "Level1Support", "Level2Support", "Level3Support"],
                "relationships": [
                    ("SupportHandler", "Level1Support"),
                    ("SupportHandler", "Level2Support"),
                    ("SupportHandler", "Level3Support"),
                    ("Level1Support", "SupportHandler"),
                    ("Level2Support", "SupportHandler"),
                    ("Level3Support", "SupportHandler")
                ],
                "code": (
                    "# Handler interface\n"
                    "class SupportHandler:\n"
                    "    def __init__(self):\n"
                    "        self.next_handler = None\n\n"
                    "    def set_next(self, handler):\n"
                    "        self.next_handler = handler\n"
                    "        return handler  # allow chaining\n\n"
                    "    def handle(self, issue):\n"
                    "        if self.next_handler:\n"
                    "            return self.next_handler.handle(issue)\n"
                    "        return \"No one could resolve the issue.\"\n\n"
                    "# Concrete Handlers\n"
                    "class Level1Support(SupportHandler):\n"
                    "    def handle(self, issue):\n"
                    "        if issue == \"password reset\":\n"
                    "            return \"Level 1: Resolved password reset.\"\n"
                    "        else:\n"
                    "            return super().handle(issue)\n\n"
                    "class Level2Support(SupportHandler):\n"
                    "    def handle(self, issue):\n"
                    "        if issue == \"software installation\":\n"
                    "            return \"Level 2: Resolved software installation.\"\n"
                    "        else:\n"
                    "            return super().handle(issue)\n\n"
                    "class Level3Support(SupportHandler):\n"
                    "    def handle(self, issue):\n"
                    "        if issue == \"network outage\":\n"
                    "            return \"Level 3: Resolved network outage.\"\n"
                    "        else:\n"
                    "            return super().handle(issue)\n\n"
                    "# Example usage\n"
                    "l1 = Level1Support()\n"
                    "l2 = Level2Support()\n"
                    "l3 = Level3Support()\n\n"
                    "l1.set_next(l2).set_next(l3)\n\n"
                    "print(l1.handle(\"password reset\"))\n"
                    "print(l1.handle(\"software installation\"))\n"
                    "print(l1.handle(\"network outage\"))\n"
                    "print(l1.handle(\"unknown issue\"))\n"
                )
            },

            # Command
            "Command": {
                "name": "Command",
                "type": "Behavioral",
                "classes": ["Command", "OrderCommand", "Kitchen", "Waiter"],
                "relationships": [
                    ("Command", "OrderCommand"),
                    ("OrderCommand", "Kitchen"),
                    ("Waiter", "OrderCommand")
                ],
                "code": (
                    "# Command interface\n"
                    "class Command:\n"
                    "    def execute(self):\n"
                    "        raise NotImplementedError\n\n"
                    "# Receiver: Kitchen\n"
                    "class Kitchen:\n"
                    "    def prepare_dish(self, dish):\n"
                    "        return f\"Kitchen: Preparing {dish}\"\n\n"
                    "# Concrete Command: OrderCommand\n"
                    "class OrderCommand(Command):\n"
                    "    def __init__(self, kitchen, dish):\n"
                    "        self.kitchen = kitchen\n"
                    "        self.dish = dish\n\n"
                    "    def execute(self):\n"
                    "        return self.kitchen.prepare_dish(self.dish)\n\n"
                    "# Invoker: Waiter\n"
                    "class Waiter:\n"
                    "    def __init__(self):\n"
                    "        self.orders = []\n\n"
                    "    def take_order(self, command: Command):\n"
                    "        self.orders.append(command)\n\n"
                    "    def send_orders(self):\n"
                    "        results = []\n"
                    "        for order in self.orders:\n"
                    "            results.append(order.execute())\n"
                    "        self.orders.clear()\n"
                    "        return results\n\n"
                    "# Example usage\n"
                    "kitchen = Kitchen()\n"
                    "waiter = Waiter()\n\n"
                    "# Guests place orders via waiter\n"
                    "order1 = OrderCommand(kitchen, \"Pasta\")\n"
                    "order2 = OrderCommand(kitchen, \"Pizza\")\n\n"
                    "waiter.take_order(order1)\n"
                    "waiter.take_order(order2)\n\n"
                    "for result in waiter.send_orders():\n"
                    "    print(result)\n"
                )
            },

            # Mediator
            "Mediator": {
                "name": "Mediator",
                "type": "Behavioral",
                "classes": ["AirTrafficControl", "Plane"],
                "relationships": [
                    ("AirTrafficControl", "Plane"),
                    ("Plane", "AirTrafficControl")
                ],
                "code": (
                    "# Mediator: Air Traffic Control (ATC)\n"
                    "class AirTrafficControl:\n"
                    "    def __init__(self):\n"
                    "        self.planes = []\n\n"
                    "    def register_plane(self, plane):\n"
                    "        self.planes.append(plane)\n\n"
                    "    def show_message(self, sender, message):\n"
                    "        results = []\n"
                    "        for plane in self.planes:\n"
                    "            if plane != sender:\n"
                    "                results.append(f\"{sender.name} to {plane.name}: {message}\")\n"
                    "        return results\n\n"
                    "# Colleague: Plane\n"
                    "class Plane:\n"
                    "    def __init__(self, name, atc: AirTrafficControl):\n"
                    "        self.name = name\n"
                    "        self.atc = atc\n"
                    "        atc.register_plane(self)\n\n"
                    "    def send(self, message):\n"
                    "        return self.atc.show_message(self, message)\n\n"
                    "# Example usage\n"
                    "atc = AirTrafficControl()\n\n"
                    "plane1 = Plane(\"Flight A123\", atc)\n"
                    "plane2 = Plane(\"Flight B456\", atc)\n"
                    "plane3 = Plane(\"Flight C789\", atc)\n\n"
                    "for msg in plane1.send(\"Requesting landing clearance\"):\n"
                    "    print(msg)\n\n"
                    "for msg in plane2.send(\"Taking off now\"):\n"
                    "    print(msg)\n"
                )
            },

            # Memento
            "Memento": {
                "name": "Memento",
                "type": "Behavioral",
                "classes": ["TextEditor", "TextMemento", "History"],
                "relationships": [
                    ("TextEditor", "TextMemento"),
                    ("History", "TextMemento")
                ],
                "code": (
                    "# Memento: stores the state of the text editor\n"
                    "class TextMemento:\n"
                    "    def __init__(self, text):\n"
                    "        self._text = text\n\n"
                    "    def get_text(self):\n"
                    "        return self._text\n\n"
                    "# Originator: the Text Editor\n"
                    "class TextEditor:\n"
                    "    def __init__(self):\n"
                    "        self._text = \"\"\n\n"
                    "    def type_text(self, words):\n"
                    "        self._text += words + \" \"\n\n"
                    "    def show_text(self):\n"
                    "        return self._text.strip()\n\n"
                    "    def save(self):\n"
                    "        return TextMemento(self._text)\n\n"
                    "    def restore(self, memento: TextMemento):\n"
                    "        self._text = memento.get_text()\n\n"
                    "# Caretaker: History of mementos\n"
                    "class History:\n"
                    "    def __init__(self):\n"
                    "        self._mementos = []\n\n"
                    "    def save(self, memento: TextMemento):\n"
                    "        self._mementos.append(memento)\n\n"
                    "    def undo(self):\n"
                    "        if self._mementos:\n"
                    "            return self._mementos.pop()\n"
                    "        return None\n\n"
                    "# Example usage\n"
                    "editor = TextEditor()\n"
                    "history = History()\n\n"
                    "editor.type_text('Hello')\n"
                    "editor.type_text('world!')\n"
                    "print('Text:', editor.show_text())\n\n"
                    "# Save current state\n"
                    "history.save(editor.save())\n\n"
                    "editor.type_text('This will be removed.')\n"
                    "print('Text after typing more:', editor.show_text())\n\n"
                    "# Undo\n"
                    "memento = history.undo()\n"
                    "if memento:\n"
                    "    editor.restore(memento)\n"
                    "print('After undo:', editor.show_text())\n"
                )
            },

            # Strategy
            "Strategy": {
                "name": "Strategy",
                "type": "Behavioral",
                "classes": ["PaymentStrategy", "CreditCardPayment", "PayPalPayment", "BitcoinPayment", "ShoppingCart"],
                "relationships": [
                    ("PaymentStrategy", "CreditCardPayment"),
                    ("PaymentStrategy", "PayPalPayment"),
                    ("PaymentStrategy", "BitcoinPayment"),
                    ("ShoppingCart", "PaymentStrategy")
                ],
                "code": (
                    "from abc import ABC, abstractmethod\n\n"
                    "# Strategy interface\n"
                    "class PaymentStrategy(ABC):\n"
                    "    @abstractmethod\n"
                    "    def pay(self, amount):\n"
                    "        pass\n\n"
                    "# Concrete Strategy: Credit Card\n"
                    "class CreditCardPayment(PaymentStrategy):\n"
                    "    def __init__(self, card_number):\n"
                    "        self.card_number = card_number\n\n"
                    "    def pay(self, amount):\n"
                    "        return f'Paid ${amount} using Credit Card {self.card_number[-4:]}'\n\n"
                    "# Concrete Strategy: PayPal\n"
                    "class PayPalPayment(PaymentStrategy):\n"
                    "    def __init__(self, email):\n"
                    "        self.email = email\n\n"
                    "    def pay(self, amount):\n"
                    "        return f'Paid ${amount} using PayPal account {self.email}'\n\n"
                    "# Concrete Strategy: Bitcoin\n"
                    "class BitcoinPayment(PaymentStrategy):\n"
                    "    def __init__(self, wallet):\n"
                    "        self.wallet = wallet\n\n"
                    "    def pay(self, amount):\n"
                    "        return f'Paid ${amount} using Bitcoin wallet {self.wallet[:6]}...'\n\n"
                    "# Context: Shopping Cart\n"
                    "class ShoppingCart:\n"
                    "    def __init__(self):\n"
                    "        self.items = []\n"
                    "        self.payment_strategy = None\n\n"
                    "    def add_item(self, item, price):\n"
                    "        self.items.append((item, price))\n\n"
                    "    def set_payment_strategy(self, strategy: PaymentStrategy):\n"
                    "        self.payment_strategy = strategy\n\n"
                    "    def checkout(self):\n"
                    "        if not self.payment_strategy:\n"
                    "            return 'No payment method selected!'\n"
                    "        total = sum(price for _, price in self.items)\n"
                    "        return self.payment_strategy.pay(total)\n\n"
                    "# Example usage\n"
                    "cart = ShoppingCart()\n"
                    "cart.add_item('Book', 20)\n"
                    "cart.add_item('Pen', 5)\n\n"
                    "cart.set_payment_strategy(CreditCardPayment('1234-5678-9876-5432'))\n"
                    "print(cart.checkout())\n\n"
                    "cart.set_payment_strategy(PayPalPayment('user@example.com'))\n"
                    "print(cart.checkout())\n\n"
                    "cart.set_payment_strategy(BitcoinPayment('1ABCDxyzWallet'))\n"
                    "print(cart.checkout())\n"
                )
            },

            # Observer
            "Observer": {
                "name": "Observer",
                "type": "Behavioral",
                "classes": ["Item", "Customer"],
                "relationships": [
                    ("Item", "Customer")
                ],
                "code": (
                    "# Subject (Observable)\n"
                    "class Item:\n"
                    "    def __init__(self, name, price):\n"
                    "        self.name = name\n"
                    "        self.price = price\n"
                    "        self.observers = []  # list of customers watching this item\n\n"
                    "    def add_observer(self, customer):\n"
                    "        self.observers.append(customer)\n\n"
                    "    def remove_observer(self, customer):\n"
                    "        self.observers.remove(customer)\n\n"
                    "    def set_price(self, new_price):\n"
                    "        if new_price < self.price:\n"
                    "            self.price = new_price\n"
                    "            self.notify_observers()\n"
                    "        else:\n"
                    "            self.price = new_price\n\n"
                    "    def notify_observers(self):\n"
                    "        for customer in self.observers:\n"
                    "            customer.update(self)\n\n"
                    "# Observer\n"
                    "class Customer:\n"
                    "    def __init__(self, name):\n"
                    "        self.name = name\n\n"
                    "    def update(self, item: Item):\n"
                    "        print(f'{self.name} notified: Price drop! {item.name} is now ${item.price}')\n\n"
                    "# Example usage\n"
                    "laptop = Item('Gaming Laptop', 1500)\n"
                    "alice = Customer('Alice')\n"
                    "bob = Customer('Bob')\n\n"
                    "laptop.add_observer(alice)\n"
                    "laptop.add_observer(bob)\n\n"
                    "print('Initial price set.')\n"
                    "laptop.set_price(1500)\n\n"
                    "print('\\nPrice drops...')\n"
                    "laptop.set_price(1200)\n"
                )
            },

            # State
            "State": {
                "name": "State",
                "type": "Behavioral",
                "classes": ["TrafficLight", "TrafficLightState", "RedState", "GreenState", "YellowState"],
                "relationships": [
                    ("TrafficLight", "TrafficLightState"),
                    ("TrafficLightState", "RedState"),
                    ("TrafficLightState", "GreenState"),
                    ("TrafficLightState", "YellowState")
                ],
                "code": (
                    "from abc import ABC, abstractmethod\n\n"
                    "# State interface\n"
                    "class TrafficLightState(ABC):\n"
                    "    @abstractmethod\n"
                    "    def switch(self, light):\n"
                    "        pass\n\n"
                    "# Concrete States\n"
                    "class RedState(TrafficLightState):\n"
                    "    def switch(self, light):\n"
                    "        print('Red → Stop. Next: Yellow')\n"
                    "        light.set_state(YellowState())\n\n"
                    "class YellowState(TrafficLightState):\n"
                    "    def switch(self, light):\n"
                    "        print('Yellow → Caution. Next: Green')\n"
                    "        light.set_state(GreenState())\n\n"
                    "class GreenState(TrafficLightState):\n"
                    "    def switch(self, light):\n"
                    "        print('Green → Go. Next: Red')\n"
                    "        light.set_state(RedState())\n\n"
                    "# Context\n"
                    "class TrafficLight:\n"
                    "    def __init__(self):\n"
                    "        self.state = RedState()  # initial state\n\n"
                    "    def set_state(self, state: TrafficLightState):\n"
                    "        self.state = state\n\n"
                    "    def change(self):\n"
                    "        self.state.switch(self)\n\n"
                    "# Example usage\n"
                    "light = TrafficLight()\n"
                    "for _ in range(5):\n"
                    "    light.change()\n"
                )
            }

        }

    def get_pattern(self, name):
        return self.patterns.get(name, None)

    def get_patterns_by_type(self, pattern_type):
        return [name for name, data in self.patterns.items() if data['type'] == pattern_type]
