from machine import Pin, I2C


class i2c_ifce:
    def __init__(self, ifce=0, scl=5, sda=4, freq=100000):
        self.ifce = ifce
        self.scl = scl
        self.sda = sda
        self.freq = freq

        self.i2c = I2C(
            self.ifce,
            scl=Pin(self.scl),
            sda=Pin(self.sda),
            freq=self.freq,
        )

    def write_byte_data(self, addr, reg, data):
        self.i2c.writeto_mem(
            addr,
            reg,
            bytes([data & 0xFF]),
        )

    def write_byte(self, addr, data):
        self.i2c.writeto(
            addr,
            bytes([data & 0xFF]),
        )

    def read_byte_data(self, addr, reg):
        return self.i2c.readfrom_mem(
            addr,
            reg,
            1,
        )[0]

    def read_byte(self, addr):
        return self.i2c.readfrom(
            addr,
            1,
        )[0]

    def read_bytes(self, addr, reg, length):
        return self.i2c.readfrom_mem(
            addr,
            reg,
            length,
        )

    def write_bytes(self, addr, reg, data):
        self.i2c.writeto_mem(
            addr,
            reg,
            bytes(data),
        )

    def i2c_scan(self):
        return self.i2c.scan()


class lis3dsh(i2c_ifce):
    # ============================================================
    # I2C address
    # ============================================================

    ADDRESS_SEL_HIGH = 0x1D
    ADDRESS_SEL_LOW = 0x1E

    # ============================================================
    # Registers
    # ============================================================

    OUT_T = 0x0C
    INFO1 = 0x0D
    INFO2 = 0x0E
    WHO_AM_I = 0x0F

    OFF_X = 0x10
    OFF_Y = 0x11
    OFF_Z = 0x12

    CS_X = 0x13
    CS_Y = 0x14
    CS_Z = 0x15

    LC_L = 0x16
    LC_H = 0x17

    STAT = 0x18

    PEAK1 = 0x19

    VFC_1 = 0x1B
    VFC_2 = 0x1C
    VFC_3 = 0x1D
    VFC_4 = 0x1E

    THRS3 = 0x1F

    CTRL_REG4 = 0x20
    CTRL_REG1 = 0x21
    CTRL_REG2 = 0x22
    CTRL_REG3 = 0x23
    CTRL_REG5 = 0x24
    CTRL_REG6 = 0x25

    STATUS = 0x27

    OUT_X_L = 0x28
    OUT_X_H = 0x29
    OUT_Y_L = 0x2A
    OUT_Y_H = 0x2B
    OUT_Z_L = 0x2C
    OUT_Z_H = 0x2D

    FIFO_CTRL = 0x2E
    FIFO_SRC = 0x2F

    # ============================================================
    # State Machine 1
    # ============================================================

    SM1_PROGRAM = 0x40  # 0x40 ~ 0x4F

    SM1_TIM4 = 0x50
    SM1_TIM3 = 0x51

    SM1_TIM2_L = 0x52
    SM1_TIM2_H = 0x53

    SM1_TIM1_L = 0x54
    SM1_TIM1_H = 0x55

    SM1_THRS2 = 0x56
    SM1_THRS1 = 0x57

    SM1_MASK_B = 0x59
    SM1_MASK_A = 0x5A
    SM1_SETT = 0x5B
    SM1_PR = 0x5C

    SM1_TC_L = 0x5D
    SM1_TC_H = 0x5E

    SM1_OUTS = 0x5F

    # ============================================================
    # State Machine 2
    # ============================================================

    SM2_PROGRAM = 0x60  # 0x60 ~ 0x6F

    SM2_TIM4 = 0x70
    SM2_TIM3 = 0x71

    SM2_TIM2_L = 0x72
    SM2_TIM2_H = 0x73

    SM2_TIM1_L = 0x74
    SM2_TIM1_H = 0x75

    SM2_THRS2 = 0x76
    SM2_THRS1 = 0x77

    SM2_DES = 0x78

    SM2_MASK_B = 0x79
    SM2_MASK_A = 0x7A
    SM2_SETT = 0x7B
    SM2_PR = 0x7C

    SM2_TC_L = 0x7D
    SM2_TC_H = 0x7E

    SM2_OUTS = 0x7F

    # ============================================================
    # WHO_AM_I
    # ============================================================

    WHO_AM_I_VALUE = 0x3F

    # ============================================================
    # ODR
    # ============================================================

    ODR_POWER_DOWN = 0
    ODR_3_125HZ = 1
    ODR_6_25HZ = 2
    ODR_12_5HZ = 3
    ODR_25HZ = 4
    ODR_50HZ = 5
    ODR_100HZ = 6
    ODR_400HZ = 7
    ODR_800HZ = 8
    ODR_1600HZ = 9

    ODR_TABLE = {
        0: 0,
        1: 3.125,
        2: 6.25,
        3: 12.5,
        4: 25,
        5: 50,
        6: 100,
        7: 400,
        8: 800,
        9: 1600,
    }

    # ============================================================
    # Full scale
    # ============================================================

    RANGE_2G = 2
    RANGE_4G = 4
    RANGE_6G = 6
    RANGE_8G = 8
    RANGE_16G = 16

    RANGE_BITS = {
        2: 0b000,
        4: 0b001,
        6: 0b010,
        8: 0b011,
        16: 0b100,
    }

    # mg / digit
    SENSITIVITY = {
        2: 0.06,
        4: 0.12,
        6: 0.18,
        8: 0.24,
        16: 0.73,
    }

    # ============================================================
    # FIFO modes
    # ============================================================

    FIFO_BYPASS = 0
    FIFO_MODE = 1
    FIFO_STREAM = 2
    FIFO_STREAM_TO_FIFO = 3

    FIFO_BYPASS_TO_STREAM = 4
    FIFO_BYPASS_TO_FIFO = 7

    # ============================================================
    # CTRL_REG6 bits
    # ============================================================

    CTRL6_BOOT = 0x80
    CTRL6_FIFO_EN = 0x40
    CTRL6_WTM_EN = 0x20
    CTRL6_ADD_INC = 0x10

    CTRL6_INT1_EMPTY = 0x08
    CTRL6_INT1_WTM = 0x04
    CTRL6_INT1_OVERRUN = 0x02
    CTRL6_INT2_BOOT = 0x01

    # ============================================================
    # CTRL_REG3 bits
    # ============================================================

    CTRL3_DR_EN = 0x80
    CTRL3_IEA = 0x40
    CTRL3_IEL = 0x20
    CTRL3_INT2_EN = 0x08
    CTRL3_INT1_EN = 0x04
    CTRL3_VFILT = 0x02
    CTRL3_STRT = 0x01

    # ============================================================
    # STATUS bits
    # ============================================================

    STATUS_ZYXOR = 0x80
    STATUS_ZOR = 0x40
    STATUS_YOR = 0x20
    STATUS_XOR = 0x10

    STATUS_ZYXDA = 0x08
    STATUS_ZDA = 0x04
    STATUS_YDA = 0x02
    STATUS_XDA = 0x01

    # ============================================================
    # STAT bits
    # ============================================================

    STAT_LONG = 0x80
    STAT_SYNCW = 0x40
    STAT_SYNC1 = 0x20
    STAT_SYNC2 = 0x10
    STAT_INT_SM1 = 0x08
    STAT_INT_SM2 = 0x04
    STAT_DOR = 0x02
    STAT_DRDY = 0x01

    # ============================================================
    # Constructor
    # ============================================================

    def __init__(
            self,
            ifce=0,
            scl=5,
            sda=4,
            freq=100000,
            addr=0x1D,
    ):
        super().__init__(
            ifce,
            scl,
            sda,
            freq,
        )

        self.addr = addr

        self._range = 2
        self._odr = self.ODR_100HZ

        self._check_device()

        # Enable automatic register address increment.
        self.set_add_increment(True)

        # BDU + XYZ enable + 100 Hz
        self.set_bdu(True)
        self.set_range(2)
        self.set_odr(self.ODR_100HZ)

    # ============================================================
    # Generic register access
    # ============================================================

    def read_reg(self, reg):
        return self.read_byte_data(
            self.addr,
            reg,
        )

    def write_reg(self, reg, value):
        self.write_byte_data(
            self.addr,
            reg,
            value,
        )

    def read_regs(self, reg, length):
        return self.read_bytes(
            self.addr,
            reg,
            length,
        )

    def write_regs(self, reg, data):
        self.write_bytes(
            self.addr,
            reg,
            data,
        )

    def update_reg(self, reg, mask, value):
        old = self.read_reg(reg)

        new = (
                      old & ~mask
              ) | (
                      value & mask
              )

        if new != old:
            self.write_reg(
                reg,
                new,
            )

        return new

    # ============================================================
    # Device
    # ============================================================

    def _check_device(self):
        value = self.who_am_i()

        if value != self.WHO_AM_I_VALUE:
            raise RuntimeError(
                "LIS3DSH not found: "
                "WHO_AM_I=0x{:02X}".format(value)
            )

    def who_am_i(self):
        return self.read_reg(
            self.WHO_AM_I
        )

    def info1(self):
        return self.read_reg(
            self.INFO1
        )

    def info2(self):
        return self.read_reg(
            self.INFO2
        )

    # ============================================================
    # Software reset
    # ============================================================

    def reset(self):
        # CTRL_REG3 STRT bit
        self.update_reg(
            self.CTRL_REG3,
            self.CTRL3_STRT,
            self.CTRL3_STRT,
        )

    # ============================================================
    # Address increment
    # ============================================================

    def set_add_increment(self, enable=True):
        value = self.read_reg(
            self.CTRL_REG6
        )

        if enable:
            value |= self.CTRL6_ADD_INC
        else:
            value &= ~self.CTRL6_ADD_INC

        self.write_reg(
            self.CTRL_REG6,
            value,
        )

    # ============================================================
    # BDU
    # ============================================================

    def set_bdu(self, enable=True):
        value = self.read_reg(
            self.CTRL_REG4
        )

        if enable:
            value |= 0x08
        else:
            value &= ~0x08

        self.write_reg(
            self.CTRL_REG4,
            value,
        )

    # ============================================================
    # ODR
    # ============================================================

    def set_odr(self, odr):
        if odr not in self.ODR_TABLE:
            raise ValueError(
                "Invalid ODR"
            )

        value = self.read_reg(
            self.CTRL_REG4
        )

        # ODR[3:0] = bit 7:4
        value &= 0x0F
        value |= (odr << 4)

        # Enable X/Y/Z
        value |= 0x07

        self.write_reg(
            self.CTRL_REG4,
            value,
        )

        self._odr = odr

    def get_odr(self):
        value = self.read_reg(
            self.CTRL_REG4
        )

        return (value >> 4) & 0x0F

    def get_odr_hz(self):
        return self.ODR_TABLE[
            self.get_odr()
        ]

    # ============================================================
    # Axis enable
    # ============================================================

    def set_axes(
            self,
            x=True,
            y=True,
            z=True,
    ):
        value = self.read_reg(
            self.CTRL_REG4
        )

        value &= ~0x07

        if x:
            value |= 0x01

        if y:
            value |= 0x02

        if z:
            value |= 0x04

        self.write_reg(
            self.CTRL_REG4,
            value,
        )

    # ============================================================
    # Full scale
    # ============================================================

    def set_range(self, g_range):
        if g_range not in self.RANGE_BITS:
            raise ValueError(
                "Range must be 2, 4, 6, 8 or 16"
            )

        value = self.read_reg(
            self.CTRL_REG5
        )

        # FSCALE[2:0] = bit 5:3
        value &= ~(0x07 << 3)

        value |= (
                self.RANGE_BITS[g_range] << 3
        )

        self.write_reg(
            self.CTRL_REG5,
            value,
        )

        self._range = g_range

    def get_range(self):
        value = self.read_reg(
            self.CTRL_REG5
        )

        fs = (
                     value >> 3
             ) & 0x07

        for g_range, bits in self.RANGE_BITS.items():
            if bits == fs:
                return g_range

        return None

    # ============================================================
    # Anti-aliasing filter
    # ============================================================

    def set_bandwidth(self, bandwidth):
        """
        bandwidth:
            800
            200
            400
            50
        """

        bits = {
            800: 0b00,
            200: 0b01,
            400: 0b10,
            50: 0b11,
        }

        if bandwidth not in bits:
            raise ValueError(
                "Bandwidth must be 800, 400, 200 or 50 Hz"
            )

        value = self.read_reg(
            self.CTRL_REG5
        )

        # BW2:BW1 = bit 7:6
        value &= ~(0x03 << 6)
        value |= bits[bandwidth] << 6

        self.write_reg(
            self.CTRL_REG5,
            value,
        )

    # ============================================================
    # Raw acceleration
    # ============================================================

    @staticmethod
    def _to_int16(value):
        if value & 0x8000:
            value -= 0x10000

        return value

    @staticmethod
    def _to_int8(value):
        if value & 0x80:
            value -= 0x100

        return value

    def _read_axis(self, reg):
        data = self.read_regs(
            reg,
            2,
        )

        raw = (
                data[0]
                | (data[1] << 8)
        )

        return self._to_int16(
            raw
        )

    def read_raw(self):
        data = self.read_regs(
            self.OUT_X_L,
            6,
        )

        x = self._to_int16(
            data[0]
            | (data[1] << 8)
        )

        y = self._to_int16(
            data[2]
            | (data[3] << 8)
        )

        z = self._to_int16(
            data[4]
            | (data[5] << 8)
        )

        return x, y, z

    # ============================================================
    # Acceleration in g
    # ============================================================

    def _raw_to_g(self, raw):
        sensitivity = self.SENSITIVITY[
            self._range
        ]

        return (
                raw * sensitivity / 1000.0
        )

    def acceleration(self):
        x, y, z = self.read_raw()

        return (
            self._raw_to_g(x),
            self._raw_to_g(y),
            self._raw_to_g(z),
        )

    @property
    def x(self):
        return self._raw_to_g(
            self._read_axis(
                self.OUT_X_L
            )
        )

    @property
    def y(self):
        return self._raw_to_g(
            self._read_axis(
                self.OUT_Y_L
            )
        )

    @property
    def z(self):
        return self._raw_to_g(
            self._read_axis(
                self.OUT_Z_L
            )
        )

    # ============================================================
    # Temperature
    # ============================================================

    def temperature_raw(self):
        """
        Return signed temperature sensor value.

        0x00 corresponds to 25 degC.
        Resolution = 1 degC / LSB.
        """

        value = self.read_reg(
            self.OUT_T
        )

        return self._to_int8(
            value
        )

    def temperature(self):
        """
        Return approximate temperature in degC.
        """

        return 25 + self.temperature_raw()

    # ============================================================
    # Status / Data Ready
    # ============================================================

    def status(self):
        return self.read_reg(
            self.STATUS
        )

    def data_ready(self):
        return bool(
            self.status()
            & self.STATUS_ZYXDA
        )

    def x_ready(self):
        return bool(
            self.status()
            & self.STATUS_XDA
        )

    def y_ready(self):
        return bool(
            self.status()
            & self.STATUS_YDA
        )

    def z_ready(self):
        return bool(
            self.status()
            & self.STATUS_ZDA
        )

    def data_overrun(self):
        return bool(
            self.status()
            & self.STATUS_ZYXOR
        )

    # ============================================================
    # STAT register
    # ============================================================

    def stat(self):
        return self.read_reg(
            self.STAT
        )

    def stat_data_ready(self):
        return bool(
            self.stat()
            & self.STAT_DRDY
        )

    def stat_sm1_interrupt(self):
        return bool(
            self.stat()
            & self.STAT_INT_SM1
        )

    def stat_sm2_interrupt(self):
        return bool(
            self.stat()
            & self.STAT_INT_SM2
        )

    # ============================================================
    # Interrupt configuration
    # ============================================================

    def enable_data_ready_interrupt(
            self,
            enable=True,
            active_high=True,
            latched=False,
            pin=1,
    ):
        """
        Enable DRDY interrupt.

        pin:
            1 -> INT1
            2 -> INT2
        """

        value = self.read_reg(
            self.CTRL_REG3
        )

        # DR_EN
        if enable:
            value |= self.CTRL3_DR_EN
        else:
            value &= ~self.CTRL3_DR_EN

        # IEA
        if active_high:
            value |= self.CTRL3_IEA
        else:
            value &= ~self.CTRL3_IEA

        # IEL
        if latched:
            value &= ~self.CTRL3_IEL
        else:
            value |= self.CTRL3_IEL

        # Enable selected interrupt output
        if pin == 1:
            if enable:
                value |= self.CTRL3_INT1_EN
            else:
                value &= ~self.CTRL3_INT1_EN

        elif pin == 2:
            if enable:
                value |= self.CTRL3_INT2_EN
            else:
                value &= ~self.CTRL3_INT2_EN

        else:
            raise ValueError(
                "pin must be 1 or 2"
            )

        self.write_reg(
            self.CTRL_REG3,
            value,
        )

    # ============================================================
    # FIFO
    # ============================================================

    def fifo_enable(self, enable=True):
        value = self.read_reg(
            self.CTRL_REG6
        )

        if enable:
            value |= self.CTRL6_FIFO_EN
        else:
            value &= ~self.CTRL6_FIFO_EN

        self.write_reg(
            self.CTRL_REG6,
            value,
        )

    def fifo_set_mode(
            self,
            mode=FIFO_BYPASS,
            watermark=0,
    ):
        if mode < 0 or mode > 7:
            raise ValueError(
                "Invalid FIFO mode"
            )

        if watermark < 0 or watermark > 31:
            raise ValueError(
                "Watermark must be 0..31"
            )

        value = (
                (mode << 5)
                | (watermark & 0x1F)
        )

        self.write_reg(
            self.FIFO_CTRL,
            value,
        )

    def fifo_config(
            self,
            mode=FIFO_STREAM,
            watermark=16,
    ):
        """
        Configure and enable FIFO.

        mode:
            FIFO_BYPASS
            FIFO_MODE
            FIFO_STREAM
            FIFO_STREAM_TO_FIFO
            FIFO_BYPASS_TO_STREAM
            FIFO_BYPASS_TO_FIFO
        """

        self.fifo_set_mode(
            mode,
            watermark,
        )

        self.fifo_enable(
            True
        )

    def fifo_disable(self):
        self.fifo_enable(
            False
        )

        self.fifo_set_mode(
            self.FIFO_BYPASS,
            0,
        )

    def fifo_status(self):
        value = self.read_reg(
            self.FIFO_SRC
        )

        return {
            "watermark": bool(
                value & 0x80
            ),
            "overrun": bool(
                value & 0x40
            ),
            "empty": bool(
                value & 0x20
            ),
            "samples": value & 0x1F,
        }

    def fifo_level(self):
        return (
                self.read_reg(
                    self.FIFO_SRC
                ) & 0x1F
        )

    def fifo_empty(self):
        return bool(
            self.read_reg(
                self.FIFO_SRC
            ) & 0x20
        )

    def fifo_overrun(self):
        return bool(
            self.read_reg(
                self.FIFO_SRC
            ) & 0x40
        )

    def fifo_watermark(self):
        return bool(
            self.read_reg(
                self.FIFO_SRC
            ) & 0x80
        )

    def fifo_read_sample(self):
        """
        Read one 6-byte XYZ sample from FIFO/output registers.
        """

        return self.read_raw()

    def fifo_read_samples(self, count=None):
        """
        Read multiple FIFO samples.

        If count is None, read all currently available samples.
        """

        if count is None:
            count = self.fifo_level()

        if count <= 0:
            return []

        samples = []

        for _ in range(count):
            samples.append(
                self.read_raw()
            )

        return samples

    def fifo_read_acceleration(
            self,
            count=None,
    ):
        raw_samples = self.fifo_read_samples(
            count
        )

        result = []

        for x, y, z in raw_samples:
            result.append(
                (
                    self._raw_to_g(x),
                    self._raw_to_g(y),
                    self._raw_to_g(z),
                )
            )

        return result

    def fifo_enable_interrupts(
            self,
            watermark=False,
            overrun=False,
            empty=False,
    ):
        value = self.read_reg(
            self.CTRL_REG6
        )

        if watermark:
            value |= self.CTRL6_INT1_WTM
        else:
            value &= ~self.CTRL6_INT1_WTM

        if overrun:
            value |= self.CTRL6_INT1_OVERRUN
        else:
            value &= ~self.CTRL6_INT1_OVERRUN

        if empty:
            value |= self.CTRL6_INT1_EMPTY
        else:
            value &= ~self.CTRL6_INT1_EMPTY

        self.write_reg(
            self.CTRL_REG6,
            value,
        )

    # ============================================================
    # Offset
    # ============================================================

    def set_offset(
            self,
            x=0,
            y=0,
            z=0,
    ):
        for value in (x, y, z):
            if value < -128 or value > 127:
                raise ValueError(
                    "Offset must be -128..127"
                )

        self.write_reg(
            self.OFF_X,
            x & 0xFF,
        )

        self.write_reg(
            self.OFF_Y,
            y & 0xFF,
        )

        self.write_reg(
            self.OFF_Z,
            z & 0xFF,
        )

    def get_offset(self):
        return (
            self._to_int8(
                self.read_reg(
                    self.OFF_X
                )
            ),
            self._to_int8(
                self.read_reg(
                    self.OFF_Y
                )
            ),
            self._to_int8(
                self.read_reg(
                    self.OFF_Z
                )
            ),
        )

    # ============================================================
    # Long counter
    # ============================================================

    def set_long_counter(self, value):
        if value < 0 or value > 0xFFFF:
            raise ValueError(
                "Long counter must be 0..65535"
            )

        self.write_reg(
            self.LC_L,
            value & 0xFF,
        )

        self.write_reg(
            self.LC_H,
            (value >> 8) & 0xFF,
        )

    def get_long_counter(self):
        data = self.read_regs(
            self.LC_L,
            2,
        )

        return (
                data[0]
                | (data[1] << 8)
        )

    # ============================================================
    # State Machine generic helpers
    # ============================================================

    def _sm_base(self, sm):
        if sm == 1:
            return {
                "program": self.SM1_PROGRAM,
                "tim4": self.SM1_TIM4,
                "tim3": self.SM1_TIM3,
                "tim2": self.SM1_TIM2_L,
                "tim1": self.SM1_TIM1_L,
                "thrs2": self.SM1_THRS2,
                "thrs1": self.SM1_THRS1,
                "mask_b": self.SM1_MASK_B,
                "mask_a": self.SM1_MASK_A,
                "sett": self.SM1_SETT,
                "pr": self.SM1_PR,
                "tc": self.SM1_TC_L,
                "outs": self.SM1_OUTS,
            }

        if sm == 2:
            return {
                "program": self.SM2_PROGRAM,
                "tim4": self.SM2_TIM4,
                "tim3": self.SM2_TIM3,
                "tim2": self.SM2_TIM2_L,
                "tim1": self.SM2_TIM1_L,
                "thrs2": self.SM2_THRS2,
                "thrs1": self.SM2_THRS1,
                "mask_b": self.SM2_MASK_B,
                "mask_a": self.SM2_MASK_A,
                "sett": self.SM2_SETT,
                "pr": self.SM2_PR,
                "tc": self.SM2_TC_L,
                "outs": self.SM2_OUTS,
            }

        raise ValueError(
            "State machine must be 1 or 2"
        )

    # ============================================================
    # State Machine program
    # ============================================================

    def sm_load_program(
            self,
            sm,
            program,
    ):
        """
        Upload up to 16 bytes of state-machine program.

        The bytes are the actual LIS3DSH opcodes.
        """

        if len(program) > 16:
            raise ValueError(
                "State machine program "
                "must be <= 16 bytes"
            )

        base = self._sm_base(
            sm
        )["program"]

        self.write_regs(
            base,
            program,
        )

    def sm_read_program(self, sm):
        base = self._sm_base(
            sm
        )["program"]

        return self.read_regs(
            base,
            16,
        )

    # ============================================================
    # State Machine timers
    # ============================================================

    def sm_set_timer4(
            self,
            sm,
            value,
    ):
        if value < 0 or value > 0xFF:
            raise ValueError(
                "Timer4 must be 0..255"
            )

        self.write_reg(
            self._sm_base(sm)["tim4"],
            value,
        )

    def sm_set_timer3(
            self,
            sm,
            value,
    ):
        if value < 0 or value > 0xFF:
            raise ValueError(
                "Timer3 must be 0..255"
            )

        self.write_reg(
            self._sm_base(sm)["tim3"],
            value,
        )

    def sm_set_timer2(
            self,
            sm,
            value,
    ):
        self._write_u16(
            self._sm_base(sm)["tim2"],
            value,
        )

    def sm_set_timer1(
            self,
            sm,
            value,
    ):
        self._write_u16(
            self._sm_base(sm)["tim1"],
            value,
        )

    # ============================================================
    # State Machine threshold
    # ============================================================

    def sm_set_thresholds(
            self,
            sm,
            thrs1=0,
            thrs2=0,
    ):
        self.write_reg(
            self._sm_base(sm)["thrs1"],
            thrs1 & 0xFF,
        )

        self.write_reg(
            self._sm_base(sm)["thrs2"],
            thrs2 & 0xFF,
        )

    # ============================================================
    # State Machine axis/sign masks
    # ============================================================

    @staticmethod
    def make_axis_mask(
            xp=False,
            xn=False,
            yp=False,
            yn=False,
            zp=False,
            zn=False,
            vp=False,
            vn=False,
    ):
        value = 0

        if xp:
            value |= 1 << 7

        if xn:
            value |= 1 << 6

        if yp:
            value |= 1 << 5

        if yn:
            value |= 1 << 4

        if zp:
            value |= 1 << 3

        if zn:
            value |= 1 << 2

        if vp:
            value |= 1 << 1

        if vn:
            value |= 1 << 0

        return value

    def sm_set_masks(
            self,
            sm,
            mask_a,
            mask_b,
    ):
        base = self._sm_base(sm)

        self.write_reg(
            base["mask_a"],
            mask_a & 0xFF,
        )

        self.write_reg(
            base["mask_b"],
            mask_b & 0xFF,
        )

    # ============================================================
    # State Machine SETT
    # ============================================================

    def sm_set_sett(
            self,
            sm,
            value,
    ):
        self.write_reg(
            self._sm_base(sm)["sett"],
            value & 0xFF,
        )

    def sm_get_sett(self, sm):
        return self.read_reg(
            self._sm_base(sm)["sett"]
        )

    # ============================================================
    # State Machine program/reset pointer
    # ============================================================

    def sm_set_pointer(
            self,
            sm,
            program_pointer=0,
            reset_pointer=0,
    ):
        if not 0 <= program_pointer <= 15:
            raise ValueError(
                "program_pointer must be 0..15"
            )

        if not 0 <= reset_pointer <= 15:
            raise ValueError(
                "reset_pointer must be 0..15"
            )

        value = (
                (program_pointer << 4)
                | reset_pointer
        )

        self.write_reg(
            self._sm_base(sm)["pr"],
            value,
        )

    # ============================================================
    # State Machine enable
    # ============================================================

    def sm_enable(
            self,
            sm,
            enable=True,
            pin=1,
            hysteresis=0,
    ):
        if hysteresis < 0 or hysteresis > 7:
            raise ValueError(
                "hysteresis must be 0..7"
            )

        if pin not in (1, 2):
            raise ValueError(
                "pin must be 1 or 2"
            )

        if sm == 1:
            reg = self.CTRL_REG1
        elif sm == 2:
            reg = self.CTRL_REG2
        else:
            raise ValueError(
                "State machine must be 1 or 2"
            )

        value = self.read_reg(
            reg
        )

        # HYST[2:0]
        value &= ~0xE0
        value |= (
                hysteresis << 5
        )

        # SM_PIN
        if pin == 2:
            value |= 0x10
        else:
            value &= ~0x10

        # SM_EN
        if enable:
            value |= 0x01
        else:
            value &= ~0x01

        self.write_reg(
            reg,
            value,
        )

    # ============================================================
    # State Machine output
    # ============================================================

    def sm_output(self, sm):
        return self.read_reg(
            self._sm_base(sm)["outs"]
        )

    def sm_interrupt(self, sm):
        if sm == 1:
            return bool(
                self.stat()
                & self.STAT_INT_SM1
            )

        if sm == 2:
            return bool(
                self.stat()
                & self.STAT_INT_SM2
            )

        raise ValueError(
            "State machine must be 1 or 2"
        )

    # ============================================================
    # Helpers
    # ============================================================

    def _write_u16(self, reg, value):
        if value < 0 or value > 0xFFFF:
            raise ValueError(
                "value must be 0..65535"
            )

        self.write_reg(
            reg,
            value & 0xFF,
        )

        self.write_reg(
            reg + 1,
            (value >> 8) & 0xFF,
        )

    def _read_u16(self, reg):
        data = self.read_regs(
            reg,
            2,
        )

        return (
                data[0]
                | (data[1] << 8)
        )

    # ============================================================
    # Debug
    # ============================================================

    def info(self):
        return {
            "address": hex(self.addr),
            "who_am_i": hex(
                self.who_am_i()
            ),
            "info1": hex(
                self.info1()
            ),
            "info2": hex(
                self.info2()
            ),
            "odr": self.get_odr_hz(),
            "range": self.get_range(),
            "data_ready": self.data_ready(),
            "temperature": self.temperature(),
            "fifo": self.fifo_status(),
        }


def main():
    print("LIS3DSH test")

    dev = lis3dsh(
        ifce=0,
        scl=5,
        sda=4,
        freq=400000,
        addr=0x1D,
    )

    print(
        "I2C:",
        [hex(x) for x in dev.i2c_scan()]
    )

    print(
        "WHO_AM_I:",
        hex(dev.who_am_i())
    )

    print(
        "INFO1:",
        hex(dev.info1())
    )

    print(
        "INFO2:",
        hex(dev.info2())
    )

    print(
        "Temperature:",
        dev.temperature(),
        "C"
    )

    print(
        "ODR:",
        dev.get_odr_hz(),
        "Hz"
    )

    print(
        "Range:",
        dev.get_range(),
        "g"
    )

    print("Start sampling...")

    while True:

        if dev.data_ready():
            x, y, z = dev.acceleration()

            temperature = dev.temperature()

            print(
                "X={:+.3f}g "
                "Y={:+.3f}g "
                "Z={:+.3f}g "
                "T={:+d}C".format(
                    x,
                    y,
                    z,
                    temperature,
                )
            )

        # time.sleep_ms(5)


def test_temp():
    dev = lis3dsh(
        ifce=0,
        scl=5,
        sda=4,
        freq=400000,
        addr=0x1D,
    )
    print("Temperature raw:", hex(dev.read_reg(dev.OUT_T)))
    print("Temperature signed:", dev.temperature_raw())


if __name__ == "__main__":
    main()
