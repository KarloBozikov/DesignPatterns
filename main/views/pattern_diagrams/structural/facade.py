import os
import pygame
from ..PatternAnimation import PatternAnimation

class FacadeAnimation(PatternAnimation):
    """Facade pattern animation drawn directly into DiagramView."""

    def __init__(self, view: "DiagramView"):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.normpath(
            os.path.join(current_dir, "../../../../main/resources/diagrams/structural_patterns/facade/")
        )
        self.traveler_img = pygame.image.load(os.path.join(base_path, "traveler.png"))
        self.service_img = pygame.image.load(os.path.join(base_path, "travelSservice.png"))
        self.flight_img = pygame.image.load(os.path.join(base_path, "FlightBooking.png"))
        self.car_img = pygame.image.load(os.path.join(base_path, "carRental.png"))
        self.hotel_img = pygame.image.load(os.path.join(base_path, "hotelBooking.png"))

        # Initialize
        self.reset_positions()
        self.frame_count = 0
        self.paused = False

    # ---------------- Helpers ----------------

    def reset_positions(self):
        w, h = self.view.width(), self.view.height()
        sx, sy = self.scale_factor()

        # Traveler on the left
        self.traveler_pos = (int(w * 0.05), int(h * 0.4))

        # Service (facade) in a center
        self.service_pos = (int(w * 0.4), int(h * 0.35))

        # Subsystems to the right
        self.flight_pos = (int(w * 0.7), int(h * 0.2))
        self.car_pos = (int(w * 0.7), int(h * 0.45))
        self.hotel_pos = (int(w * 0.7), int(h * 0.7))

    def scale_elements(self):
        traveler = self.scale_image(self.traveler_img, 100, 120)
        service = self.scale_image(self.service_img, 150, 150)
        flight = self.scale_image(self.flight_img, 120, 120)
        car = self.scale_image(self.car_img, 120, 120)
        hotel = self.scale_image(self.hotel_img, 120, 120)
        return traveler, service, flight, car, hotel

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        traveler, service, flight, car, hotel = self.scale_elements()

        # Draw base icons
        surface.blit(traveler, self.traveler_pos)
        surface.blit(service, self.service_pos)
        surface.blit(flight, self.flight_pos)
        surface.blit(car, self.car_pos)
        surface.blit(hotel, self.hotel_pos)

        # Centers
        traveler_center = self.get_anchor(self.traveler_pos, traveler, "midright")
        service_center  = self.get_anchor(self.service_pos, service, "midleft")
        service_right   = self.get_anchor(self.service_pos, service, "midright")
        flight_center   = self.get_anchor(self.flight_pos, flight, "midleft")
        car_center      = self.get_anchor(self.car_pos, car, "midleft")
        hotel_center    = self.get_anchor(self.hotel_pos, hotel, "midleft")

        # Animate arrows
        self.frame_count += 1
        arrow_growth_speed = 15

        # Traveler -> Service
        self.draw_growing_arrow(surface, traveler_center, service_center,
                                self.frame_count * arrow_growth_speed)

        # Service -> subsystems
        if self.frame_count > 30:
            self.draw_growing_arrow(surface, service_right, flight_center,
                                    (self.frame_count - 30) * arrow_growth_speed)
        if self.frame_count > 60:
            self.draw_growing_arrow(surface, service_right, car_center,
                                    (self.frame_count - 60) * arrow_growth_speed)
        if self.frame_count > 90:
            self.draw_growing_arrow(surface, service_right, hotel_center,
                                    (self.frame_count - 90) * arrow_growth_speed)

        # Labels
        surface.blit(self.font.render("Traveler books trip", True, (255, 255, 0)),
                     (self.traveler_pos[0], self.traveler_pos[1] - 30))
        surface.blit(self.font.render("TravelService", True, (0, 255, 255)),
                     (self.service_pos[0], self.service_pos[1] - 40))
        surface.blit(self.font.render("FlightBooking.book()", True, (255, 255, 255)),
                     (self.flight_pos[0], self.flight_pos[1] - 30))
        surface.blit(self.font.render("CarRental.reserve()", True, (255, 255, 255)),
                     (self.car_pos[0], self.car_pos[1] - 30))
        surface.blit(self.font.render("HotelBooking.book()", True, (255, 255, 255)),
                     (self.hotel_pos[0], self.hotel_pos[1] - 30))

        # Loop
        if self.frame_count > 200:
            self.frame_count = 0

        # Finalize
        self.finalize_frame(surface)
