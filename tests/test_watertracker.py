from services.water_tracker import WaterTracker


def test_add_water(valid_user, profile):
    valid_user.profiles = [profile]

    tracker = WaterTracker()
    tracker.add_water(500)
    assert tracker.current_intake == 500
    assert tracker.get_progress() == 12.5