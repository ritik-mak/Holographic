import logging
import argparse
import sys
import time
import src.config
from src.tracker import FaceTracker
from src.scene import IllusionScene


def parse_args():
    parser = argparse.ArgumentParser(description="Holographic demo")
    parser.add_argument("--camera", type=int, default=src.config.CAMERA_ID, help="Camera device id")
    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    log = logging.getLogger("holo")

    tracker = FaceTracker(camera_id=args.camera)
    scene = IllusionScene()

    running = True
    user_x, user_y, user_z = 0.0, 0.0, src.config.DEFAULT_VIEWER_Z_CM

    log.info("Starting holographic window. Press 'C' to calibrate, ESC to quit.")

    try:
        clock = __import__("pygame").time.Clock()
        while running:
            for event in __import__("pygame").event.get():
                if event.type == __import__("pygame").QUIT:
                    running = False
                if event.type == __import__("pygame").KEYDOWN:
                    if event.key == __import__("pygame").K_ESCAPE:
                        running = False
                    if event.key == __import__("pygame").K_c:
                        raw_pos = tracker.get_eye_position()
                        if raw_pos:
                            tracker.calibrate(raw_pos)

            raw_pos = tracker.get_eye_position()

            if raw_pos and tracker.calibrated:
                MOVEMENT_GAIN = 100.0
                dx = (raw_pos[0] - tracker.base_x) * -MOVEMENT_GAIN
                dy = (raw_pos[1] - tracker.base_y) * MOVEMENT_GAIN

                dz_ratio = (1.0 / raw_pos[2]) / (1.0 / tracker.base_depth_scale)
                dz = src.config.DEFAULT_VIEWER_Z_CM * (1.0 / dz_ratio)

                alpha = 0.15
                user_x = user_x * (1 - alpha) + dx * alpha
                user_y = user_y * (1 - alpha) + dy * alpha
                user_z = user_z * (1 - alpha) + dz * alpha

            elif not tracker.calibrated:
                user_x, user_y, user_z = 0.0, 0.0, src.config.DEFAULT_VIEWER_Z_CM

            scene.set_off_axis_frustum(user_x, user_y, user_z)
            scene.draw_scene()
            clock.tick(60)

    except Exception as exc:
        log.exception("Unhandled error in main loop: %s", exc)

    finally:
        try:
            tracker.cleanup()
        except Exception:
            pass
        try:
            __import__("pygame").quit()
        except Exception:
            pass


if __name__ == "__main__":
    main()