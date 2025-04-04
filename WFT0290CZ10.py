import time

import machine
from machine import Pin, SPI

EPD_WIDTH = 128
EPD_HEIGHT = 296

IMAGE_DATA = [ 0X00,0X01,0XF0,0X00,0X67,0X00,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XF8,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X00,0X00,0X00,0X00,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X00,0X00,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X00,0X00,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X00,0X38,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X01,0XF8,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X0F,0XF8,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X7F,0XF8,0X03,0XF0,0X1F,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X03,0XFF,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X1F,0XFF,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFF,0XF0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFF,0X80,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFC,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XF8,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X3F,0XFE,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X07,0XFF,0XC0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0XFF,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X1F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X1F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X7F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X03,0XFF,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X1F,0XFF,0XE0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFF,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFC,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XF0,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XFC,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X1F,0XFF,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X03,0XFF,0XE0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0XFF,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X3F,0XFF,0X80,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X07,0XFF,0XC0,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X00,0X01,0XFF,0XE0,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7C,0X00,0X7F,0XF0,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0X00,0X0F,0XF8,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XC0,0X07,0XFC,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XE0,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X7F,0XF8,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X3F,0XFE,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X07,0XFF,0XC0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X00,0X01,0XFF,0XF0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X83,0XFF,0X00,0X7F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X81,0XFE,0X00,0X1F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0XFF,0X00,0X1F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X7F,0XC0,0X7F,0XF8,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0X80,0X3F,0XF9,0XFF,0XF0,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0X1F,0XFF,0XFF,0X80,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X0B,0XFF,0XFE,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X00,0XFF,0XF8,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X00,0X3F,0XE0,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X00,0X0F,0X80,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X00,0X02,0X00,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X3F,0X00,0X00,0X00,0X00,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X18,0XFF,0XFF,0XFE,0X7F,0XF9,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0XF8,0XFF,0XFF,0XF8,0X1F,0XF0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X3F,0XF8,0XFF,0XFF,0XE0,0X0F,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XE0,0XFF,0XFF,0XE0,0X07,0X80,0X7F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0X00,0XFF,0XFF,0XF0,0X03,0XC0,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XFF,0XFF,0XF8,0X00,0XE0,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X3F,0XF0,0XC0,0X00,0X00,0X00,0X70,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X03,0XF8,0XC0,0X00,0X00,0X00,0X18,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X07,0XF8,0XC0,0X00,0X00,0X00,0X04,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0XE0,0XC0,0X00,0X00,0X00,0X06,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XC0,0X00,0X00,0X00,0X07,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0X00,0XFF,0XFF,0XFF,0XFC,0X07,0XC3,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XE0,0XF8,0XFF,0XFF,0XFE,0X0F,0XE3,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1F,0XF8,0XF8,0X3F,0XFF,0X06,0X00,0X13,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0XF8,0XE0,0X03,0XFF,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X18,0XE0,0X00,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X00,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X70,0X00,0XF8,0X00,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XF9,0X80,0XFE,0X00,0X01,0X06,0X0F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XF9,0XC0,0XFF,0XC0,0X01,0X06,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XFF,0XFF,0XC1,0X06,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XFF,0XFF,0XC1,0X06,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XFF,0X8F,0XC1,0X06,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XFC,0X00,0X01,0X06,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XFE,0X00,0X01,0X06,0X0F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFE,0X00,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X40,0XFD,0X00,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X03,0XC0,0XF8,0X80,0X01,0X06,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1F,0XC0,0XE0,0X40,0XFF,0X02,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XC0,0X40,0XFF,0X00,0X00,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0X00,0XC0,0X20,0X7E,0X00,0X0F,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0X00,0XE0,0X00,0X7E,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XF0,0X07,0XF0,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1F,0XC0,0XF8,0X03,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X03,0XC0,0XFC,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X40,0XFE,0X00,0X00,0X01,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XFF,0X00,0X00,0X7F,0X80,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0X00,0X00,0X7F,0X83,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFC,0X00,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XED,0XC0,0XF8,0X00,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XF0,0X03,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XE0,0X07,0XE0,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0XC0,0XE0,0X1F,0XFC,0X00,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0X80,0XE0,0X3F,0XFF,0XE0,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X0E,0X00,0XF8,0X7F,0XFF,0XFF,0X83,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFC,0XFF,0XFF,0XFF,0X83,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X43,0X00,0XFE,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC7,0X80,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0XC0,0XFF,0XFF,0XFF,0XE0,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X78,0XC0,0XFF,0XFF,0XFF,0XE0,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X30,0X40,0XFF,0XFF,0XFF,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X7F,0XFF,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XF0,0X7F,0X83,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XF0,0X60,0X83,0XFF,0XE0,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X70,0X00,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XF9,0X80,0XF0,0X60,0X83,0XFF,0XE0,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XF9,0XC0,0XF0,0X60,0X83,0XFF,0XE0,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X60,0X83,0X00,0X00,0X03,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X60,0X83,0XFF,0XE0,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF0,0X60,0X83,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XC0,0X00,0X03,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XC0,0X00,0X03,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XC0,0X00,0X03,0X84,0X20,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XED,0XC0,0XC0,0X00,0X03,0XFF,0XE0,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XC0,0X00,0X03,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XC0,0X00,0X03,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0XC0,0XFF,0XFF,0XFF,0XE0,0X00,0X83,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0X80,0XFF,0XFF,0XFF,0XE0,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X0E,0X00,0XFF,0XFF,0XFF,0XE0,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XE0,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XF8,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XF8,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XF8,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC3,0X18,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC3,0X18,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC3,0X18,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC3,0X18,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0X18,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XF0,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XFC,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFE,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XED,0XC0,0XFF,0XFE,0X07,0X03,0XC0,0X7F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XFC,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XF8,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0XC0,0XF0,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0X80,0XE0,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X0E,0X00,0XE0,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X00,0X00,0X00,0X00,0X01,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XE0,0X3E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XE1,0XC0,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X40,0XC0,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X7E,0X07,0X83,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XE0,0X7E,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0XF0,0XE0,0X7E,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XF0,0XE0,0X7E,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XF0,0XE0,0X3E,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XE0,0X02,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XE0,0X00,0X00,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X01,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF0,0X01,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XF8,0X01,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XFE,0X03,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0XC0,0XFF,0XC3,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XE1,0XC0,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XE1,0XC0,0XFF,0XFF,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0XC0,0XFF,0XFF,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFF,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XFF,0XFF,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XFC,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XE0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XC0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X01,0X80,0XC0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XC0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0XC0,0XC0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XC0,0XC0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X80,0XE0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0X00,0XE0,0X7F,0XF8,0X1F,0XFC,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X00,0X00,0X00,0X3C,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XE0,0X00,0X00,0X00,0X3C,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XD8,0XE0,0X00,0X00,0X00,0X1C,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XD8,0XF0,0X00,0X00,0X00,0X1C,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFF,0XD8,0XF0,0X00,0X00,0X00,0X0C,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XF8,0X00,0X00,0X00,0X04,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XF8,0X1C,0X04,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X1E,0X00,0XFF,0XFF,0XF8,0X1E,0X00,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFF,0XF8,0X1E,0X00,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X7F,0X80,0XFF,0XFF,0XF8,0X1F,0X00,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XE1,0XC0,0XFF,0XFF,0XF8,0X1F,0X00,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XFF,0XFF,0XF8,0X1F,0X80,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XFF,0XFF,0XF8,0X1F,0XC0,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC0,0XC0,0XFF,0XFF,0XF8,0X1F,0XC0,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X40,0XC0,0XFF,0XFF,0XF8,0X1F,0XE0,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XF8,0X1F,0XF0,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X43,0X00,0XFF,0XFF,0XF8,0X1F,0XF8,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XC7,0X80,0XFF,0XFF,0XF8,0X1F,0XF8,0X07,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCF,0XC0,0XFF,0XFF,0XF8,0X1F,0XFC,0X0F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XCC,0XC0,0XFF,0XFF,0XF8,0X1F,0XFE,0X1F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0XFC,0XC0,0XFF,0XFF,0XF8,0X1F,0XFF,0X3F,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X78,0XC0,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X30,0X40,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XF8,0X1F,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XF0,0X00,0X00,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,
0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF,0XFF]

class WFT0290CZ10(object):
    def __init__(self):
        self.spi = SPI(0, baudrate=62500000, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

        self.busy = Pin(12, mode=Pin.IN)
        self.rst = Pin(15, mode=Pin.OUT, value=1)
        self.dc = Pin(14, mode=Pin.OUT, value=1)
        self.cs = Pin(13, mode=Pin.OUT, value=1)

    def spi_write8(self, b):
        self.spi.write(bytearray([b]))
        # print(b)

    def write_cmd(self, cmd):
        self.dc.low()
        self.cs.low()
        self.spi_write8(cmd)
        self.cs.high()

    def write_data(self, data):
        self.dc.high()
        self.cs.low()
        self.spi_write8(data)
        self.cs.high()

    def write_data_buffered(self, buf):
        self.dc.high()
        self.cs.low()
        for val in buf:
            self.spi_write8(val)
        self.cs.high()

    def write_reg(self, *opts):
        reg = opts[0]
        # print("reg: ", reg)
        self.write_cmd(reg)

        if len(opts) == 1:
            return

        opts = opts[1:]
        for val in opts:
            # print("val: ", val)
            self.write_data(val)

    def wait_busy(self):
        #self.write_reg(0x71)
        while not self.busy.value():
            continue

    def init_display(self):
        self.reset()

        self.write_reg(0x04)
        self.wait_busy()
        
        self.write_reg(0x30, 0x3C)
        
        self.write_reg(0x00, 0x0f, 0x89)
        
        self.write_reg(0x61, 0x80, 0x01, 0x28)
        
        self.write_reg(0x50, 0x77)

    def turn_on_display(self):
        self.write_reg(0x12)
        self.wait_busy()

    def reset(self):
        self.rst.high()
        time.sleep_ms(200)
        self.rst.low()
        time.sleep_ms(2)
        self.rst.high()
        time.sleep_ms(200)

    def fill(self, color: bool):
        pass

    def clear(self):
        #self.write_reg(0x10)
        #for i in range(4736):
        #    self.write_data(0xff)
        
        self.write_reg(0x13)
        for i in range(4736):
            self.write_data(0x00)
        
        self.write_reg(0x12)
        self.wait_busy()
        pass

    def show_img(self, data):
        width = EPD_WIDTH / 8
        height = EPD_HEIGHT
        
        #self.write_reg(0x10)
        #for j in range(height):
        #    for i in range(width):
        #        self.write_data(data[int(i + (j * width))])
        #self.write_reg(0x92)
        
        self.write_reg(0x13)
        for j in range(height):
            for i in range(width):
                self.write_data(data[int(i + (j * width))])
        #self.write_reg(0x92)

        self.write_reg(0x12)
        self.wait_busy()

    def sleep(self):
        self.write_reg(0x02)
        self.wait_busy()
        self.write_reg(0x07, 0xa5)

if __name__ == "__main__":
    machine.freq(240000000)  # set the CPU frequency to 240 MHz
    print("CPU freq : ", machine.freq() / 1000000, "MHz")

    dev = WFT0290CZ10()
    dev.init_display()

    print("cleaning screen ...")
    dev.clear()
    
    print("showing image...")
    dev.show_img(IMAGE_DATA)

    print("going to sleep mode ...")
    dev.sleep() # voltage on pin PREVGH will drop from 20V to 3.3V

