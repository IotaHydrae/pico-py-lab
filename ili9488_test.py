# init

import usys as sys
sys.path.append('') # See: https://github.com/micropython/micropython/issues/6419

import lvgl as lv
import lv_utils

lv.init()

class driver:
    def init_gui(self):
        import ili9488 as tft
        import ft6236 as tp

        hres = 480
        vres = 320
        color_format = lv.COLOR_FORMAT.RGB565

        # Register display driver
        event_loop = lv_utils.event_loop()
        tft.deinit()
        tft.init()
        tp.init()

        buf1 = tft.framebuffer(1)
        buf2 = tft.framebuffer(2)

        self.disp_drv = lv.display_create(hres, vres)
        self.disp_drv.set_flush_cb(tft.flush)
        self.disp_drv.set_color_format(color_format)
        self.disp_drv.set_buffers(buf1, buf2, len(buf1), lv.DISPLAY_RENDER_MODE.PARTIAL)

        # disp_drv.gpu_blend_cb = lcd.gpu_blend
        # disp_drv.gpu_fill_cb = lcd.gpu_fill

        # Register touch driver
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.indev_drv.set_read_cb(tp.ts_read)

if not lv_utils.event_loop.is_running():
    drv = driver()
    drv.init_gui()

scr = lv.obj()
btn = lv.button(scr)
btn.align(lv.ALIGN.CENTER, 0, 0)
label = lv.label(btn)
label.set_text('Hello World!')

lbl = lv.label(scr)
lbl.set_text("Present by embeddedboys")
lbl.align(lv.ALIGN.BOTTOM_MID, 0, -20)

lv.screen_load(scr)