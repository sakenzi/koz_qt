import time


def update_reverse_timer(window):
    elapsed = int(time.time() - window.start_time)
    remaining_time = window.total_time - elapsed
    if remaining_time >= 0:
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        window.reverse_timer_label.setText(f"Тайминг: {minutes}:{seconds:02d}")
    else:
        window.reverse_timer_label.setText("Тайминг: 0:00")
        window.timer.stop()
