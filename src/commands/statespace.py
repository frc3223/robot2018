import numpy
from wpilib import Timer, Notifier
from wpilib.command import Command

from subsystems import Drivetrain


class StateSpaceController:
    def __init__(self, A, Ainv, B, C, D, K, Kff, L):
        self.A = A
        self.Ainv = Ainv
        self.B = B
        self.C = C
        self.D = D
        self.K = K
        self.Kff = Kff
        self.L = L
        self.u_min = -12
        self.u_max = 12
        self.u = numpy.zeros((self.B.shape[1], 1))
        self.u_offset = numpy.zeros(shape=self.u.shape)
        self.y = numpy.zeros((self.C.shape[0], 1))
        self.r = numpy.zeros((self.A.shape[0], 1))
        self.x_hat = numpy.zeros((self.A.shape[0], 1))
        self.reset()

    def reset(self):
        self.u = numpy.zeros((self.B.shape[1], 1))
        self.y = numpy.zeros((self.C.shape[0], 1))
        self.r = numpy.zeros((self.A.shape[0], 1))
        self.x_hat = numpy.zeros((self.A.shape[0], 1))

    default_r = numpy.zeros(shape=(1,1))

    def update_input(self, next_r=default_r):
        self.u = self.K @ (self.r - self.x_hat)
        if next_r is not self.default_r:
            uff = self.Kff @ (next_r  - self.A @ self.r)
            self.r = next_r
        else:
            uff = self.Kff @ (self.r - self.A @ self.r)
        self.u = numpy.clip(self.u + uff - self.u_offset, self.u_min, self.u_max)

    def predict(self):
        self.x_hat = self.A @ self.x_hat + self.B @ self.u

    def correct(self):
        self.x_hat += self.Ainv @ self.L @ (self.y - self.C @ self.x_hat - self.D @ self.u)

    def check_shape(self, matrix_name, shape):
        m = getattr(self, matrix_name)
        assert m.shape == shape, "%s shape expected %s, was %s" % (matrix_name, shape, m.shape)


class StateSpaceDriveController(StateSpaceController):
    def __init__(self, drivetrain: Drivetrain):
        """
        x: (left position (m), left velocity (m/s), right position (m), right velocity (m/s).T
        y: (left position (m), right position (m)).T

        :param drivetrain:
        """
        from numpy import array as matrix
        derpymodel = True
        if derpymodel:
            self.u_offset = matrix([[1.29], [1.32]])
            A = matrix([[1., 0.01954524, 0., 0.],
                        [0., 0.95487116, 0., 0.],
                        [0., 0., 1., 0.01953105],
                        [0., 0., 0., 0.95347481]])

            B = matrix([[0.00016013, 0.],
                        [0.01589044, 0.],
                        [0., 0.00016005],
                        [0., 0.01587891]])

            C = matrix([[1, 0, 0, 0],
                        [0, 0, 1, 0]])

            D = matrix([[0., 0.],
                        [0., 0.]])

            K = matrix([[8.70337746e+01, 1.54364232e+01, 1.64506224e-13,
                         6.89196592e-15],
                        [-2.48568085e-14, 5.01719083e-15, 8.70882843e+01,
                         1.53690171e+01]])

            Kff = matrix([[778.96386513, 1.93253647, 0., 0.],
                          [0., 0., 778.71561076, 1.93145314]])

            L = matrix([[1.28456071e+00, 4.48179733e-17],
                        [1.39021836e+01, 2.18957546e-15],
                        [-3.61345038e-17, 1.28327788e+00],
                        [-1.76400902e-15, 1.38293101e+01]])

            Ainv = matrix([[1., -0.02046898, 0., 0.],
                           [0., 1.04726171, 0., 0.],
                           [0., 0., 1., -0.02048408],
                           [0., 0., 0., 1.04879541]])
        else:
            A = matrix([[1., 0.01631643, 0., 0.00238268],
                        [0., 0.66737266, 0., 0.20542149],
                        [0., 0.00238268, 1., 0.01631643],
                        [0., 0.20542149, 0., 0.66737266]])

            B = matrix([[0.00123499, -0.00079884],
                        [0.11152021, -0.06887181],
                        [-0.00079884, 0.00123499],
                        [-0.06887181, 0.11152021]])

            C = matrix([[1, 0, 0, 0],
                        [0, 0, 1, 0]])

            D = matrix([[0, 0],
                        [0, 0]])

            K = matrix([[56.82612189, 6.03969859, 18.60045886, 3.51953103],
                        [18.60045886, 3.51953103, 56.82612189, 6.03969859]])

            Kff = matrix([[731.26285269, 1.74253981, 334.3110478, 0.86234499],
                          [334.3110478, 0.86234499, 731.26285269, 1.74253981]])

            L = matrix([[1.12809912, 0.08747579],
                        [5.70458841, 4.3576656],
                        [0.08747579, 1.12809912],
                        [4.3576656, 5.70458841]])

            Ainv = matrix([[1., -0.02579361, 0., 0.0043692],
                           [0., 1.65523823, 0., -0.5094927],
                           [0., 0.0043692, 1., -0.02579361],
                           [0., -0.5094927, 0., 1.65523823]])
        super().__init__( A=A, Ainv=Ainv, B=B, C=C, D=D, K=K, Kff=Kff, L=L )
        self.drivetrain = drivetrain
        self.period = Command.getRobot().getPeriod()
        self._at_reference = False

    def make_reference_m(self, left_pos_m, left_vel_mps, right_pos_m, right_vel_mps):
        return numpy.array([[left_pos_m, left_vel_mps, right_pos_m, right_vel_mps]]).T

    def make_reference_ft(self, left_pos_ft, right_pos_ft, left_vel_fps, right_vel_fps):
        return self.make_reference_m(left_pos_ft, right_pos_ft, left_vel_fps, right_vel_fps) / 3.28

    def update(self, left_pos_m, right_pos_m, left_vel_mps, right_vel_mps):
        self.check_shape("A", (4,4))
        self.check_shape("B", (4,2))
        self.check_shape("C", (2,4))
        self.check_shape("D", (2,2))
        self.check_shape("r", (4,1))
        self.check_shape("x_hat", (4,1))
        self.check_shape("y", (2,1))
        self.check_shape("u", (2,1))
        self.check_shape("Kff", (2,4))
        self.check_shape("K", (2,4))
        self.check_shape("L", (4,2))
        self.correct()
        self.update_input(self.make_reference_m(left_pos_m, left_vel_mps, right_pos_m, right_vel_mps))
        self._send_input()
        self.update_measurements()
        self.predict()

    def _send_input(self):
        voltage = self.drivetrain.getVoltage()
        vpl = self.u[0,0] / voltage
        vpr = self.u[1,0] / voltage
        self.drivetrain.setLeftMotor(vpl)
        self.drivetrain.setRightMotor(vpr)
        self.drivetrain.feed()

    def update_measurements(self):
        pos_l_ft = self.drivetrain.getLeftEncoder() / self.drivetrain.ratio
        pos_r_ft = self.drivetrain.getRightEncoder() / self.drivetrain.ratio
        self.y[0,0] = pos_l_ft / 3.28 # meter
        self.y[1,0] = pos_r_ft / 3.28 # meter


