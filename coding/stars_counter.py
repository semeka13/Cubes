def star_counter(hp, score, timer, level_time):
    stars = 0
    if hp == 3:
        stars += 1
    if score == 3:
        stars += 1
    if timer <= level_time:
        stars += 1
    return stars



