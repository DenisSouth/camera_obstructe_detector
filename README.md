### Camera Visibility Obstruction Detector

The process primarily involves analyzing the spectral 
domain to discern the ratio of high frequencies. 
This ratio is then juxtaposed against a predetermined
threshold value between 0.0 - 1.0. If the resulting 
value falls below this threshold, the function 
`is_camera_obstructed` returns `True`, thereby indicating 
that the camera's visibility is indeed obstructed. 
If not, it returns `False`.

In debug mode (`debug=True`), the original frame and the 
spectral domain are displayed on the screen, along with 
the high-frequency ratio.

This approach to video stream analysis facilitates
camera obstruction detection not just based 
on the frame's brightness level, but also by 
analyzing the frequency spectrum (greater image
details lead to higher frequencies). This methodology 
proves to be effective in situations where the camera 
is obscured by a transparent material, such as paper, 
fabric, or a finger.
