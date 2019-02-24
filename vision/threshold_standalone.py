enable_lens_corr = False # turn on for straighter lines...

import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

min_degree = 80
max_degree = 100
thresh_buffer = list()
threshold_height = 60

while(True):
    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    threshold_list = list()
    for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree):
            threshold_h = (l.y1() + l.y2()) >> 1
            sample_pixel = img.get_pixel(79, threshold_h + 5)   # pixel from below middle of line
            if sample_pixel is not None and sample_pixel >= (235, 235, 235):
                # img.draw_line(l.line(), color = (255, 0, 0))  # DEBUG
                threshold_list.append(threshold_h)
    if len(threshold_list) != 0:
        min_thresh = min(iter(threshold_list))
        if len(thresh_buffer) < 3:      # fill buffer when not full
            thresh_buffer.append(min_thresh)
        else:                           # update buffer if new threshold value is reasonable
            thresh_buffer_avg = sum(thresh_buffer) / 3
            if abs(thresh_buffer_avg - min_thresh) < 30:
                thresh_buffer.pop(0)
                thresh_buffer.append(min_thresh)
            threshold_height = thresh_buffer[2]

    # print(threshold_height)   # DEBUG
