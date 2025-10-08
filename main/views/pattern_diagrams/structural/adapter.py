import os
import pygame
from ..PatternAnimation import PatternAnimation

class AdapterAnimation(PatternAnimation):
    """Adapter pattern animation: US plug -> Adapter -> EU socket."""

    def __init__(self, view):
        super().__init__(view)

        # Load resources
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.join(
            current_dir, "../../../../main/resources/diagrams/structural_patterns/adapter/"
        )

        self.imgs = {
            "adapter": pygame.image.load(os.path.join(base_path, "adapter.png")),
            "socket": pygame.image.load(os.path.join(base_path, "eu_socket.png")),
            "plug": pygame.image.load(os.path.join(base_path, "us_plug.png")),
        }

        self.reset_positions()

    # ---------------- Helpers ----------------

    def reset_positions(self):
        """Initial positions for plug, adapter, and socket."""
        w, h = self.view.width(), self.view.height()

        self.us_pos = (int(w * 0.15), int(h * 0.5 - 50))
        self.adapter_pos = (int(w * 0.45), int(h * 0.5 - 60))
        self.eu_pos = (int(w * 0.75), int(h * 0.5 - 60))

    def scale_elements(self):
        """Return scaled images for plug, adapter, and socket."""
        plug = self.scale_image(self.imgs["plug"], 120, 100)
        adapter = self.scale_image(self.imgs["adapter"], 140, 120)
        socket = self.scale_image(self.imgs["socket"], 140, 120)
        return plug, adapter, socket

    # ---------------- Frame Update ----------------

    def update_frame(self):
        if self.paused:
            return

        surface = self.create_surface()
        plug_img, adapter_img, socket_img = self.scale_elements()

        # Always draw socket
        surface.blit(socket_img, self.eu_pos)

        if self.phase == 0:
            # Phase 0: US plug directly into EU socket -> fails
            plug_pos = self.move_linear(
                self.us_pos, self.frame_count,
                speed=4, max_frames=60,
                final_offset=(self.eu_pos[0] - self.us_pos[0] - plug_img.get_width() + 15, 0),
            )
            surface.blit(plug_img, plug_pos)

            self.draw_labels(surface, {
                "US Plug": (plug_pos[0], plug_pos[1] - 30),
                "EU Socket": (self.eu_pos[0], self.eu_pos[1] - 30),
            })

            if self.frame_count > 100:
                self.draw_message(
                    surface, "Connection not recognized!", (255, 0, 0),
                    (*self.eu_pos, socket_img.get_width(), socket_img.get_height())
                )

        else:
            # Phase 1: Plug goes into Adapter -> Adapter into EU socket
            adapter_pos = self.move_linear(
                self.adapter_pos, self.frame_count,
                speed=3, max_frames=40,
                final_offset=(self.eu_pos[0] - self.adapter_pos[0] - adapter_img.get_width() + 30, 0),
            )
            surface.blit(adapter_img, adapter_pos)

            labels = {
                "Adapter": (adapter_pos[0], adapter_pos[1] - 30),
                "EU Socket": (self.eu_pos[0], self.eu_pos[1] - 30),
            }

            if self.frame_count > 40:
                plug_pos = self.move_linear(
                    self.us_pos, self.frame_count - 40,
                    speed=4, max_frames=60,
                    final_offset=(adapter_pos[0] - self.us_pos[0] - plug_img.get_width() + 15, 0),
                                 )
                surface.blit(plug_img, plug_pos)
                labels["US Plug"] = (plug_pos[0], plug_pos[1] - 30)

                if self.frame_count > 120:
                    self.draw_message(
                        surface, "Power Connected!", (0, 255, 0),
                        (*self.eu_pos, socket_img.get_width(), socket_img.get_height())
                    )

            self.draw_labels(surface, labels)

        # Frame & phase control
        self.frame_count += 1
        if self.frame_count > 200:
            self.frame_count, self.phase = 0, 1 - self.phase  # switch fail/success

        self.finalize_frame(surface)
