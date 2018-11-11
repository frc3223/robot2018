class TrapezoidalProfile:
    def __init__(self, cruise_v: float, a: float, target_pos: float, tolerance: float, current_target_v=0):
        assert cruise_v > 0
        self._cruise_v = cruise_v
        self.a = a
        self.current_target_v = current_target_v
        self.current_a = 0
        self.target_pos = target_pos
        self.tolerance = tolerance
        self.cruise_v_scale = 1
        self.do_print = False
        self.adist = 0
        self.err = 0

    @property
    def cruise_v(self):
        return self._cruise_v * self.cruise_v_scale

    def setCruiseVelocityScale(self, scale):
        assert scale > 0
        self.cruise_v_scale = scale

    def _print(self, s):
        if self.do_print:
            print("%s: v=%f, a=%f" % (s, self.current_target_v, self.current_a))

    def calculate_new_velocity(self, current_pos, dt):
        assert self.cruise_v > 0
        a = self.a
        v = self.current_target_v
        okerr = self.tolerance

        if a == 0:
            adist = v * 100 * self.tolerance
        else:
            adist = 0.5 * v ** 2 / a

        self.adist = adist

        err = self.target_pos - current_pos

        self.err = err
        self.current_a = 0

        def inc():
            nonlocal v, dt, a
            if v + dt * a > self.cruise_v:
                self.current_a = (self.cruise_v - v) / dt
                v = self.cruise_v
            else:
                v += dt * a
                self.current_a = a

        def dec():
            nonlocal v, dt, a
            if v - dt * a < -self.cruise_v:
                self.current_a = (-self.cruise_v - v) / dt
                v = -self.cruise_v
            else:
                v -= dt * a
                self.current_a = -a

        def dec_to_zero():
            nonlocal v, dt, a
            if v < dt * a:
                v = 0
                self.current_a = -v / dt
            else:
                v -= dt * a
                self.current_a = -a

        if abs(err) < okerr:
            if v > 0:
                self._print ('pro1')
                dec_to_zero()
            elif v < 0:
                self._print ('pro2')
                inc()
        elif okerr <= err < adist and v > 0:
            self._print ('pro3')
            dec()
        elif okerr <= err < adist and v < 0:
            self._print ('pro4')
            inc()
        elif -okerr >= err > -adist and v < 0:
            self._print ('pro5')
            inc()
            self.current_a = +a
        elif -okerr >= err > -adist and v > 0:
            self._print ('pro6')
            dec()
        elif err > adist and v >= 0:
            if v < self.cruise_v:
                self._print ('pro7')
                inc()
            elif v > self.cruise_v:
                self._print ('pro8')
                dec()
        elif err < -adist and v <= 0:
            if v > -self.cruise_v:
                self._print ('pro9')
                dec()
            elif v < -self.cruise_v:
                self._print ('pro10')
                inc()
        elif err > adist and v < 0:
            self._print ('pro11')
            inc()
        elif err < -adist and v > 0:
            self._print ('pro12')
            dec()

        self._print('post')
        self.current_target_v = v

    def isFinished(self, current_pos):
        err = self.target_pos - current_pos
        return abs(err) < self.tolerance and self.current_target_v == 0

